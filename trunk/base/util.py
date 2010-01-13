#!/usr/bin/python2.4
#
# Copyright 2009 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Shared utility functions."""

__author__ = 'elsigh@google.com (Lindsey Simon)'

import hashlib
import logging
import random
import os
import pickle
import re
import sys
import time
import urllib

from google.appengine.api import memcache
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.api.labs import taskqueue
from google.appengine.api import urlfetch

import django
from django import http
from django import shortcuts
from django.template import loader, Context

from django.template import add_to_builtins
add_to_builtins('base.custom_filters')

import settings

from models.result import *
from models.user_agent import *
from categories import all_test_sets
from categories import test_set_params
from base import decorators
from base import manage_dirty
from base import summary_test_set
from base import custom_filters

from third_party.gviz import gviz_api


MULTI_TEST_DRIVER_TEST_PAGE = '/multi_test_frameset'

ABOUT_TPL = 'about.html'
TEST_DRIVER_TPL = 'test_driver.html'
MULTI_TEST_FRAMESET_TPL = 'multi_test_frameset.html'
MULTI_TEST_DRIVER_TPL = 'multi_test_driver.html'

BETA_PARAMS = 'beta'

#@decorators.trusted_tester_required
def Render(request, template, params={}, category=None):
  """Wrapper function to render templates with global and category vars."""
  params['app_title'] = settings.APP_TITLE
  params['version_id'] = os.environ['CURRENT_VERSION_ID']
  params['build'] = settings.BUILD
  params['resource_version'] = custom_filters.get_resource_version()
  params['epoch'] = int(time.time())
  # we never want o=xhr in our request_path, right?
  params['request_path'] = request.get_full_path().replace('&o=xhr', '')
  params['request_path_lastbit'] = re.sub('^.+\/([^\/]+$)', '\\1', request.path)
  params['current_ua_string'] = request.META['HTTP_USER_AGENT']
  params['current_ua'] = UserAgent.factory(params['current_ua_string']).pretty()
  params['chromeframe_enabled'] = request.COOKIES.get(
      'browserscope-chromeframe-enabled', '0')
  params['app_categories'] = []
  params['is_admin'] = users.is_current_user_admin()

  current_user = users.get_current_user()
  if current_user:
    params['user_id'] = current_user.user_id()
    params['is_elsigh'] = current_user.nickname() == 'elsigh'
  else:
    params['user_id'] = None
    params['is_elsigh'] = False
  params['user'] = current_user

  params['sign_in'] = users.create_login_url(request.get_full_path())
  params['sign_out'] = users.create_logout_url('/')

  # Creates a list of tuples categories and their ui names.
  for i, test_set in enumerate(all_test_sets.GetTestSetsIncludingBetas()):
    # This way we can show beta categories in local dev.
    if (settings.BUILD == 'development' or
        (test_set.category in settings.CATEGORIES and
         test_set.category not in settings.CATEGORIES_INVISIBLE) or
        (params.has_key('stats_table_category') and
         test_set.category == params['stats_table_category'])):
      params['app_categories'].append([test_set.category,
                                       test_set.category_name])
    # Select the current page's category.
    if category and category == test_set.category:
      params['app_category'] = test_set.category
      params['app_category_name'] = test_set.category_name
      params['app_category_index'] = i

  if (category != None
      and template not in (TEST_DRIVER_TPL, MULTI_TEST_DRIVER_TPL,
                           MULTI_TEST_FRAMESET_TPL, ABOUT_TPL)):
    template = '%s/%s' % (category, template)

  return shortcuts.render_to_response(template, params)



def CategoryTest(request):
  """Loads the test frameset for a category."""
  category = re.sub('\/test.*', '', request.path)[1:]
  test_set = all_test_sets.GetTestSet(category)

  testurl = ''
  test_key = request.GET.get('test_key')
  if test_key:
    test = test_set.GetTest(test_key)
    testurl = test.url

  params = {
    'category': test_set.category,
    'page_title': '%s - Tests' % test_set.category_name,
    'continue': request.GET.get('continue', ''),
    'autorun': request.GET.get('autorun', ''),
    'testurl': testurl,
    'test_page': test_set.test_page
  }
  #return shortcuts.render_to_response('test_frameset.html', params)
  return Render(request, 'test_frameset.html', params)


@decorators.provide_csrf
def CategoryTestDriver(request):
  """Loads the test driver for a category."""
  category = request.GET.get('category')
  test_set = all_test_sets.GetTestSet(category)
  params = {
    'category': test_set.category,
    'page_title': '%s - Test Driver' % test_set.category_name,
    'continue': request.GET.get('continue', ''),
    'autorun': request.GET.get('autorun', ''),
    'test_page': test_set.test_page,
    'testurl': request.GET.get('testurl', ''),
    'csrf_token': request.session.get('csrf_token'),
    'hide_footer': True
  }
  return Render(request, TEST_DRIVER_TPL, params, category)


def MultiTestFrameset(request):
  """Multi-Page Test Frameset - frames the multi-page test driver and the
current test page"""
  category = request.GET.get('category', '')
  params = {
    'page_title': 'Multi-Test Frameset',
    'autorun': request.GET.get('autorun', 1),
    'testurl': request.GET.get('testurl', ''),
    'category': category
  }
  return Render(request, MULTI_TEST_FRAMESET_TPL, params, category)


def MultiTestDriver(request):
  """Multi-Page Test Driver - runs each of multiple tests in sequence in a
single category"""
  category = request.GET.get('category', '')
  tests = all_test_sets.GetTestSet(category).tests
  params = {
    'page_title': 'Multi-Test Driver',
    'tests': tests,
    'autorun': request.GET.get('autorun'),
    'testurl': request.GET.get('testurl'),
    'category': category
  }
  return Render(request, MULTI_TEST_DRIVER_TPL, params, category)


def About(request, category, category_title=None, overview='',
          show_hidden=True, show_test_urls=False):
  """Generic 'About' page."""
  if None == category_title:
    category_title = category.title()

  if show_hidden:
    tests = all_test_sets.GetTestSet(category).tests
  else:
    tests = GetVisibleTests(all_test_sets.GetTestSet(category).tests)

  params = {
    'page_title': "What are the %s Tests?" % (category_title),
    'overview': overview,
    'tests': tests,
    'show_test_urls': show_test_urls
  }
  return Render(request, ABOUT_TPL, params, category)


def GetVisibleTests(tests):
  return [test for test in tests
          if not hasattr(test, 'is_hidden_stat') or not test.is_hidden_stat]


def GetServer(request):
  """A utility function for getting the server and port."""
  server = request.META['SERVER_NAME']
  server_port = request.META['SERVER_PORT']
  if server_port != '80':
    server = server + ':' + server_port
  return server

STATIC_MESSAGE = ('<em class="rt-static">This is a recent snapshot '
                  'of the results - '
                  'it will be refreshed every hour.</em>')
RECENT_TESTS_MEMCACHE_KEY = 'recent_tests'
def Home(request):
  """Our Home page."""

  recent_tests = memcache.get(key=RECENT_TESTS_MEMCACHE_KEY)
  if not recent_tests:
    ScheduleRecentTestsUpdate()

  results_params = []
  for category in (settings.CATEGORIES + settings.CATEGORIES_INVISIBLE +
                   settings.CATEGORIES_BETA):
    results_uri_string = request.GET.get('%s_results' % category)
    if results_uri_string:
      results_params.append('%s_results=%s' % (category, results_uri_string))

  stats_tables = {}
  test_set = None
  category = request.GET.get('category')

  if category == 'summary':
    test_set = summary_test_set.TEST_SET
  elif category:
    test_set = all_test_sets.GetTestSet(category)
  else:
    if len(results_params) > 0:
      for category in (settings.CATEGORIES + settings.CATEGORIES_INVISIBLE +
                       settings.CATEGORIES_BETA):
        if request.GET.get('%s_results' % category):
          test_set = all_test_sets.GetTestSet(category)
          break

  # If we still got no test_set, take the first one in settings.CATEGORIES
  if not test_set:
    category = settings.CATEGORIES[0]
    test_set = all_test_sets.GetTestSet(category)

  # Tell GetStats what to output.
  output = request.GET.get('o', 'html')
  if output not in ['html', 'pickle', 'xhr', 'csv', 'gviz', 'gviz_data']:
    return http.HttpResponse('Invalid output specified')
  stats_table = GetStats(request, test_set, output)

  # Show a static message above the table.
  if category in settings.STATIC_CATEGORIES and output in ['xhr', 'html']:
    stats_table = '%s%s' % (STATIC_MESSAGE, stats_table)

  if output in ['xhr', 'pickle', 'csv', 'gviz', 'gviz_data']:
    return http.HttpResponse(stats_table)
  else:
    params = {
      'page_title': 'Home',
      'results_params': '&'.join(results_params),
      'v': request.GET.get('v', 'top'),
      'output': output,
      'ua_params': request.GET.get('ua', ''),
      'stats_table_category': test_set.category,
      'stats_table': stats_table,
      'recent_tests': recent_tests,
      'message': request.GET.get('message'),
    }
    return Render(request, 'home.html', params)


def BrowseResults(request):
  ua = request.GET.get('ua')
  bookmark = request.GET.get('bookmark')
  limit = int(request.GET.get('limit', 100))
  order = request.GET.get('order', 'desc')
  query = pager.PagerQuery(ResultParent, keys_only=True)
  #query.filter()
  if order == 'desc':
    query.order('-created')
  else:
    query.order('created')

  prev_bookmark, results, next_bookmark = query.fetch(fetch_limit, bookmark)

  params = {
    'prev_bookmark': prev_bookmark,
    'next_bookmark': next_bookmark,
    'results': results
  }
  return ''


def Faq(request):
  """FAQ"""

  params = {
    'page_title': 'FAQ',
    'section_urls': ''
  }
  return Render(request, 'faq.html', params)


def AllTests(request):
  """All Tests"""
  params = {
    'page_title': 'All Tests',
    'section_urls': ''
  }
  return Render(request, 'alltests.html', params)


def Results(request):
  """Results"""
  params = {
    'page_title': 'Results',
    'section_urls': ''
  }
  return Render(request, 'results.html', params)


def Contribute(request):
  """Contribute"""
  params = {
    'page_title': 'Contribute',
    'section_urls': ''
  }
  return Render(request, 'contribute.html', params)


IP_THROTTLE_NS = 'IPTHROTTLE'
def CheckThrottleIpAddress(ip, user_agent_string):
  """Prevent beacon abuse.
  This throttle allows you to "RunAllTests" 10 times per day per IP and
  major browser. i.e. the key is something like 1.1.1.1_Opera 10

  We only use memcache here, so if we allow some extras in b/c of that, phooey.

  Args:
    ip: A masked IP address string.
    user_agent_string: A user agent string.
  Returns:
    A Boolean, True if things are aok, False otherwise.
  """

  key = '%s_%s' % (ip, user_agent_string)
  timeout = 86400 # 60 * 60 * 24
  runs_per_timeout = 10

  runs = memcache.get(key, IP_THROTTLE_NS)
  #logging.info('CheckThrottleIpAddress runs: %s' % runs)
  if runs is None:
    memcache.set(key=key, value=1, time=60, namespace=IP_THROTTLE_NS)
  elif runs <= runs_per_timeout:
    memcache.incr(key=key, delta=1,namespace=IP_THROTTLE_NS)
  else:
    return False
  return True


@decorators.admin_required
def ShowMemcache(request):
  stats = memcache.get_stats()
  response = '<h1>Memcache Stats</h1>'
  for key, val in stats.items():
    response += '<h2>%s: %s</h2>' % (key, val)
  return http.HttpResponse(response)


@decorators.admin_required
def ClearMemcache(request):
  message = []
  continue_url = request.GET.get('continue')

  # KABOOM
  if request.GET.get('all'):
    memcache.flush_all()
    message.append('Cleared memcache for all keys.')

  # Piecemeal cleanups
  else:
    recent = request.GET.get('recent')
    if recent:
      memcache.delete(key=RECENT_TESTS_MEMCACHE_KEY, seconds=0)
      message.append('Cleared memcache for recent tests.')

    category = request.GET.get('category')
    if category:
      categories = category.split(',')
    else:
      categories = settings.CATEGORIES

    ua = request.GET.get('ua')
    version_level = request.GET.get('v')
    if ua:
      user_agent_strings = ua.split(',')
    elif version_level:
      user_agent_strings = UserAgentGroup.GetStrings(version_level)
    else:
      return http.HttpResponse('Either pass in ua= or v=')

    logging.info('categories are: %s' % categories)
    logging.info('user_agent_strings are: %s' % user_agent_strings)
    for category in categories:
      for user_agent in user_agent_strings:
        memcache_ua_key = ResultParent.GetMemcacheKey(category, user_agent)
        memcache.delete(key=memcache_ua_key, seconds=0,
                        namespace=settings.STATS_MEMCACHE_UA_ROW_NS)
        logging.info('Deleting %s in memcache' % memcache_ua_key)

    message.append('Cleared memcache for categories: %s and '
                   'user_agent_strings: %s' % (categories, user_agent_strings))

  # All done.
  if continue_url:
    if not re.search('\?', continue_url):
      continue_url += '?'
    continue_url += '&message=' + urllib.quote(' '.join(message))
    return http.HttpResponseRedirect(continue_url)
  else:
   return http.HttpResponse('<br>'.join(message))


def ScheduleRecentTestsUpdate():
  try:
    taskqueue.Task(method='GET').add(queue_name='recent-tests')
    #logging.info('ScheduleRecentTestsUpdate made a task')
  except:
    logging.info('Cannot add task: %s:%s' % (sys.exc_type, sys.exc_value))


BAD_BEACON_MSG = 'Error in Beacon: '
BEACON_COMPLETE_CB_RESPONSE = 'BEACON_COMPLETE = 1;'
@decorators.check_csrf
def Beacon(request):
  """Records result times in the datastore.
  This is the handler for after a test is done.
  ex: /beacon?category=reflow&csrf_token=number&results=tes1=150,test2=300
  """
  # First make sure this IP is not being an overachiever ;)
  ip = request.META.get('REMOTE_ADDR')
  ip_hash = hashlib.md5(ip).hexdigest()

  user_agent_string = request.META.get('HTTP_USER_AGENT')
  if not CheckThrottleIpAddress(ip_hash, user_agent_string):
    return http.HttpResponseServerError(BAD_BEACON_MSG + 'IP')

  js_user_agent_string = request.REQUEST.get('js_ua')

  callback = request.REQUEST.get('callback')
  category = request.REQUEST.get('category')
  results_str = request.REQUEST.get('results')
  params_str = request.REQUEST.get('params')

  if not category or not results_str:
    logging.info('Got no category or results.')
    return http.HttpResponse(BAD_BEACON_MSG + 'Category/Results')
  if (settings.BUILD == 'production'
      and category not in settings.CATEGORIES + settings.CATEGORIES_BETA):
    # Allows local developers to try out category beaconing.
    logging.info('Got a bogus category (%s).' % category)
    return http.HttpResponse(BAD_BEACON_MSG + 'Category in Production')
  if not all_test_sets.HasTestSet(category):
    logging.info('Could not get a test_set for category: %s' % category)
    return http.HttpResponse(BAD_BEACON_MSG + 'TestSet')

  test_set = all_test_sets.GetTestSet(category)
  logging.info('Beacon category: %s\nresults_str: %s' % (category, results_str))

  # Allow beta categories to save their data with a magic params string.
  if category in settings.CATEGORIES_BETA:
    logging.info('BETA %s is geting BETA_PARAMS' % category)
    params_str = BETA_PARAMS

  if params_str:
    params_str = urllib.unquote(params_str)
  result_parent = ResultParent.AddResult(
      test_set, ip_hash, user_agent_string, results_str, params_str=params_str,
      js_user_agent_string=js_user_agent_string)
  if not result_parent:
    return http.HttpResponse(BAD_BEACON_MSG + 'ResultParent')

  manage_dirty.ScheduleDirtyUpdate()
  ScheduleRecentTestsUpdate()

  if callback:
    return http.HttpResponse(BEACON_COMPLETE_CB_RESPONSE)
  else:
    # Return a successful, empty 204.
    return http.HttpResponse('', status=204)


@decorators.dev_appserver_only
@decorators.provide_csrf
def GetCsrf(request):
  """A get request to return a CSRF token."""
  csrf_token = request.session['csrf_token']
  return_csrf = request.GET.get('return_csrf', True)
  if return_csrf != '0':
    msg = csrf_token
  else:
    if csrf_token:
      msg = 'True'
    else:
      msg = 'False'
  return http.HttpResponse(msg)


def GetStats(request, test_set, output='html', opt_tests=None,
             use_memcache=True):
  """Returns the stats table.
  Args:
    request: a request object.
    test_set: a TestSet instance.
    output: Output type html or pickle or else you get a dict of params.
    opt_tests: list of tests.
    use_memcache: Use memcache or not.
  """
  logging.info('GetStats for %s' % test_set.category)
  version_level = request.GET.get('v', 'top')

  # Check for static mode here to enable other optimizations.
  override_static_mode = request.GET.get('sc') # sc for skip cache
  static_mode = False
  if (test_set.category in settings.STATIC_CATEGORIES and
      output in ['html', 'xhr'] and not override_static_mode):
    static_mode = True

  user_agent_strings = None
  user_agent_filter = None
  ua_by_param = request.GET.get('ua')
  if ua_by_param:
    user_agent_strings = ua_by_param.split(',')
    # Account for UA* - note that this allows only a single UA* at this time.
    if (len(user_agent_strings) == 1 and
        user_agent_strings[0].find('*') != -1):
      user_agent_filter = user_agent_strings[0].replace('*', '')
      if not static_mode:
        user_agent_strings = UserAgentGroup.GetStrings(version_level,
                                                       user_agent_filter)
  elif not static_mode:
    user_agent_strings = UserAgentGroup.GetStrings(version_level)
  #logging.info('GetStats: v: %s, uas: %s' % (version_level,
  #             user_agent_strings))

  tests = opt_tests or test_set.tests
  params_str = None
  # Store beta data with a magic params_str.
  if test_set.category in settings.CATEGORIES_BETA:
    params_str = BETA_PARAMS
    if test_set.default_params:
      params_str += '_%s' % str(test_set.default_params)
  elif test_set.default_params:
    params_str = str(test_set.default_params)


  # Enables a "static" pickle mode so that we still run the data through
  # the template processor (enabling us to display a user's test results)
  # but read the datastore-heavy data part from a static, pickled file.
  if static_mode:
    if settings.STATIC_SRC == 'local':
      pickle_file = ('static_mode/%s_%s.py' % (test_set.category,
                                               version_level))
      f = open(pickle_file, 'r')
      stats_data = pickle.load(f)
      f.close()
    else:
      url = ('%s/%s_%s.py' % (settings.STATIC_SRC, test_set.category,
                              version_level))
      logging.info('Loading stats from url: %s' % url)
      result = urlfetch.fetch(url)
      pickled_data = result.content
      stats_data = pickle.loads(pickled_data)
    logging.info('Retrieved static_mode stats_data.')

    # If we got custom as a version level we only want matching keys.
    if ua_by_param:
      if user_agent_filter:
        stats_data_copy = stats_data.copy()
        stats_data = {}
        for key, val in stats_data_copy.items():
          if key.find(user_agent_filter) != -1:
            stats_data[key] = val
      elif user_agent_strings is not None:
        stats_data_copy = stats_data.copy()
        stats_data = {}
        for key, val in stats_data_copy.items():
          if key in user_agent_strings:
            stats_data[key] = val

    user_agent_strings = stats_data.keys()
    UserAgentGroup.SortUserAgentStrings(user_agent_strings)
    #logging.info('Pickled stats_data: %s' % stats_data)
    #logging.info('pickled ua_strings: %s' % user_agent_strings)

  elif test_set.category == 'summary':
    stats_data = GetSummaryData(user_agent_strings, version_level)

  else:
    stats_data = GetStatsData(test_set.category, tests, user_agent_strings,
                              ua_by_param, params_str, use_memcache,
                              version_level)
  #logging.info('GetStats got stats_data: %s' % stats_data)

  # If the output is pickle, we are done and need to return a string.
  if output == 'pickle':
    return pickle.dumps(stats_data)

  # Reset tests now to only be "visible" tests.
  tests = GetVisibleTests(tests)

  # Looks for a category_results=test1=X,test2=X url GET param.
  results = None
  results_str = request.GET.get('%s_results' % test_set.category, '')
  if results_str:
    results = dict((x['key'], x)
                   for x in test_set.ParseResults(results_str,
                       is_import_or_uri_results_str=True))

  # Set current_ua_string to one in user_agent_strings
  current_ua = UserAgent.factory(request.META['HTTP_USER_AGENT'])
  current_ua_string = current_ua.pretty()
  for ua_string in user_agent_strings:
    if current_ua_string.startswith(ua_string):
      current_ua_string = ua_string
      break
  else:
    # current_ua_string was not found in user_agent_strings.
    if results:
      user_agent_strings.append(current_ua_string)
      UserAgentGroup.SortUserAgentStrings(user_agent_strings)

  # Adds the current results into the stats_data dict.
  if results:
    stats_data.setdefault(current_ua_string, {})
    current_results = {}
    stats_data[current_ua_string]['current_results'] = current_results
    current_ua_score = 0
    medians = dict((test.key, results[test.key]['score']) for test in tests)
    for test in tests:
      if test.key in results:
        median = medians[test.key]
        score, display = GetScoreAndDisplayValue(
	    test, median, medians, is_uri_result=True)
        stats_data[current_ua_string]['current_results'][test.key] = {
            'median': median,
            'score': score,
            'display': display,
            'expando': results[test.key].get('expando', None),
            }
    current_score, current_display = test_set.GetRowScoreAndDisplayValue(
        current_results)
    current_score = Convert100to10Base(current_score)
    stats_data[current_ua_string]['current_score'] = current_score
    stats_data[current_ua_string]['current_display'] = current_display

  #logging.info('stats_data now: %s' % stats_data)
  #logging.info('user_agent_strings: %s' % user_agent_strings)
  params = {
    'category': test_set.category,
    'category_name': test_set.category_name,
    'tests': tests,
    'v': version_level,
    'output': output,
    'ua_by_param': ua_by_param,
    'user_agents': user_agent_strings,
    'request_path': request.get_full_path(),
    'current_user_agent': current_ua_string,
    'stats': stats_data,
    'params': test_set.default_params,
    'results_uri_string': results_str
  }
  #logging.info("GetStats got params: %s", str(params))
  if output in ['html', 'xhr']:
    return GetStatsDataTemplatized(params, 'table')
  elif output in ['csv', 'gviz']:
    return GetStatsDataTemplatized(params, output)
  elif output == 'gviz_data':
    return FormatStatsDataAsGviz(params, request)
  else:
    return params


def FormatStatsDataAsGviz(params, request):
  """Takes the output of GetStats and returns a GViz appropriate response.
  This makes use of the Python GViz API on Google Code.
  Copied roughly from:
    http://code.google.com/p/google-visualization-python/source/browse/trunk/examples/dynamic_example.py
  Args:
    params: The dict output from GetStats.
  Returns:
    A JSON string as content in a text/plain HttpResponse.
  """
  columns_order = ['user_agent',
                   'score',
                   #'total_runs'
                  ]
  take1 = False
  take2 = True
  if take1:
    description = {'user_agent': ('string', 'User Agent'),
                   'score': ('number', 'Score'),
                   #'total_runs': ('number', '# Tests')
                  }
  elif take2:
    description = [('user_agent', 'string'),
                   ('score', 'number')]

  with_tests = False
  if with_tests:
    for test in params['tests']:
      gviz_coltype = test.score_type
      if test.score_type == 'custom':
        gviz_coltype = 'number'
      description[test.key] = (gviz_coltype, test.name)
      columns_order.append(test.key)

  data = []
  stats = params['stats']
  for user_agent in params['user_agents']:
    # Munge user_agent in this case to get rid of things like (Namaroka) which
    # make for the charts pretty awful.
    splitted = user_agent.split(' ')
    v_bit = splitted[len(splitted) - 1]

    if (stats.has_key(user_agent) and
        stats[user_agent].has_key('results') and
        stats[user_agent]['score'] != 0):
      if take1:
        row_data = {}
        row_data['user_agent'] = v_bit
        row_data['score'] = stats[user_agent]['score']
      elif take2:
        row_data = [v_bit, stats[user_agent]['score']]

      if with_tests:
        row_data['total_runs'] = stats[user_agent]['total_runs']
        for test in params['tests']:
          row_data[test.key] = stats[user_agent]['results'][test.key]['median']
      data.append(row_data)

  data_table = gviz_api.DataTable(description)
  data_table.LoadData(data)

  return data_table.ToResponse(columns_order=columns_order,
                               order_by='user_agent',
                               tqx=request.GET.get('tqx', ''))


def GetSummaryData(user_agent_strings, version_level):
  """Returns a data dictionary for rendering a summary stats_table.html"""
  stats_data = {}
  for user_agent in user_agent_strings:
    ua_score_avg = 0
    total_runs = 0
    for test_set in all_test_sets.GetTestSets():
      if not stats_data.has_key(user_agent):
        stats_data[user_agent] = {
          'total_runs': 0,
          'results': {},
          'score': 0,
          'display': 0
          }
      memcache_ua_key = ResultParent.GetMemcacheKey(test_set.category,
                                                    user_agent)
      row_stats = memcache.get(key=memcache_ua_key,
          namespace=settings.STATS_MEMCACHE_UA_ROW_SCORE_NS)
      if not row_stats:
        row_stats = {'row_score': 0, 'row_display': '', 'total_runs': 0}
      stats_data[user_agent]['results'][test_set.category] = {
          'median': row_stats['row_score'],
          'score': Convert100to10Base(row_stats['row_score']),
          'display': row_stats['row_display'],
          'total_runs': row_stats['total_runs'],
          'expando': None,
          }
      ua_score_avg += int(row_stats['row_score'])
      total_runs += int(row_stats['total_runs'])

    avg_score = int(ua_score_avg / len(settings.CATEGORIES))
    stats_data[user_agent]['score'] = avg_score
    stats_data[user_agent]['display'] = avg_score
    stats_data[user_agent]['total_runs'] = total_runs
  return stats_data


def GetStatsData(category, tests, user_agents, ua_by_param,
                 params_str, use_memcache=True, version_level='top',
                 ignore_hidden_stats=True):
  """This is the meat and potatoes of the stats."""
  #logging.info('GetStatsData category:%s\n tests:%s\n user_agents:%s\n params:%s\nuse_memcache:%s\nversion_level:%s' % (category, tests, user_agents, params, use_memcache, version_level))
  stats = {'total_runs': 0}

  # Do a initial optimized-for-memcache-get_multi pass.
  memcache_stats_data = {}
  if use_memcache:
    memcache_ua_keys = []
    for user_agent in user_agents:
      memcache_ua_key = ResultParent.GetMemcacheKey(category, user_agent)
      memcache_ua_keys.append(memcache_ua_key)
    memcache_stats_data = memcache.get_multi(
          keys=memcache_ua_keys, namespace=settings.STATS_MEMCACHE_UA_ROW_NS)

  for user_agent in user_agents:
    user_agent_stats = None
    memcache_ua_key = ResultParent.GetMemcacheKey(category, user_agent)
    if memcache_stats_data.has_key(memcache_ua_key):
      user_agent_stats = memcache_stats_data[memcache_ua_key]

    # Just for logging
    if user_agent_stats is None:
      logging.info('Diving into the rankers for %s...' % user_agent)
    else:
      logging.info('GetStatsData from memcache ua: %s, len(uastats)stats:%s' %
                   (user_agent, len(user_agent_stats)))

    if user_agent_stats is None:
      medians = {}
      total_runs = None
      user_agent_results = {}
      user_agent_score = 0
      for test in tests:
        #logging.info('GetStatsData working on test: %s, ua: %s' %
        #             (test.key, user_agent))
        ranker = test.GetRanker(user_agent, params_str)

        if ranker:
          #start_time = time.time()
          median, total_runs = ranker.GetMedianAndNumScores()
          medians[test.key] = median
          #end_time = time.time()
          #logging.info('GetStatsData test: %s, delta: %s' %
          #              (test.key, (end_time - start_time)))
          #logging.info('Got median: %s, total_runs: %s' % (median, total_runs))

        # If total_runs is 0, or we find no ranker, then we should skip
        # trying to look for data, because this is a user agent that has not
        # run this test category.
        if total_runs == 0 or not ranker:
          if not ranker:
            logging.warn('GetStatsData: Ranker not found: %s, %s, %s, %s',
                         category, test.key, user_agent, params_str)
            medians[test.key] = None
          else:
            logging.info('test_runs was 0, so we can infer no tests '
                         'for this user_agent.')
            medians = None
            logging.info('Breaking out of the loop!')
            break

      # Reset tests now to only be the "visible" tests.
      if ignore_hidden_stats:
        visible_tests = GetVisibleTests(tests)
      else:
        visible_tests = tests

      # Now make a second pass with all the medians and call our formatter,
      # GetScoreAndDisplayValue.
      for test in visible_tests:
        #logging.info('user_agent: %s, total_runs: %s' % (user_agent, total_runs))
        if medians is None:
          user_agent_results[test.key] = {
            'median': None,
            'score': 0,
            'display': '',
          }
        else:
          score, display = GetScoreAndDisplayValue(test, medians[test.key],
                                                   medians,
                                                   is_uri_result=False)
          user_agent_results[test.key] = {
            'median': medians[test.key],
            'score': score,
            'display': display,
          }

      #logging.info('GetRowScoreAndDisplayValue for ua: %s' % user_agent)
      row_score, row_display = all_test_sets.GetTestSet(
          category).GetRowScoreAndDisplayValue(user_agent_results)
      user_agent_stats = {
        'total_runs': total_runs or 0,
        'results': user_agent_results,
        'score': Convert100to10Base(row_score),
        'display': row_display
      }
      if use_memcache:
        memcache.set(key=memcache_ua_key, value=user_agent_stats,
                     time=settings.STATS_MEMCACHE_TIMEOUT,
                     namespace=settings.STATS_MEMCACHE_UA_ROW_NS)
        logging.info('GetStatsData: added %s data to memcache' %
                     (memcache_ua_key))

        # Add row total scores for overall results display.
        # TODO(elsigh): this is simply to fix the acid3 case where we set the
        # row_display to '' because that's the only metric we're storing.
        if category == 'acid3':
          row_display = '%s/%s' % (row_score, '100')
        row_stats = {'row_score': row_score, 'row_display': row_display,
                     'total_runs': total_runs or 0}
        memcache.set(key=memcache_ua_key, value=row_stats, time=0,
                     namespace=settings.STATS_MEMCACHE_UA_ROW_SCORE_NS)

    # This adds the result dict to the output dict for this ua.
    # We check for version_level == 'top' b/c we always add every top ua
    # to the final dict. Same goes if ua_by_param.
    # Otherwise, we look and see if there are any
    # test runs (total_runs) for this ua, if not, we don't add them in.
    # Casting user_agent as str here prevents unicode errors when unpickling.
    if (version_level == 'top' or
        (ua_by_param and ua_by_param.find('*') == -1) or
        user_agent_stats['total_runs']):
      stats[user_agent] = user_agent_stats
      stats['total_runs'] += user_agent_stats['total_runs']

  #logging.info('GetStatsData done, stats: %s' % stats)
  return stats


def Convert100to10Base(value):
  """Converts some value 1-100 to some value 1-10
  Args:
    1_100_value: A number, 1-100
  Returns:
    A number 1-10
  """
  return int(round(float('%s.0' % int(value)) / 10))


def GetScoreAndDisplayValue(test, median, medians, is_uri_result=False):
  """For a test, get its score and display value.
  A basic version exists here to handle the common boolean case.
  TODO(slamm,elsigh): Should this be in the test_base?
  Args:
    test: A TestBase instance.
    median: A number, the score median.
    medians: All the medians in case we need to pass them for normalization.
    is_uri_result: Boolean, is this a result bit in the url instead of from
                   the datastore?
  Returns:
    (score, display)
    A tuple of (score, display)
    Where score is a value between 1-10.
    And display is the text for the cell.
  """
  if median is None:
    score = 0
    display = ''

  # Score for the template classnames is a value of 0-10.
  elif test.score_type == 'boolean':
    # Boolean scores are 1 or 10.
    if median == 0:
      score = 1
      display = settings.STATS_SCORE_FALSE
    else:
      score = 10
      display = settings.STATS_SCORE_TRUE
  elif test.score_type == 'custom':
    score, display = test.GetScoreAndDisplayValue(median, medians,
                                                  is_uri_result)
    #logging.info('test.url: %s, key: %s, score %s, display %s' %
    #             (test.url, test.key, score, display))

    # The custom_tests_function returns a score between 1-100 which we'll
    # turn into a 0-10 display.
    score = Convert100to10Base(score)

    #logging.info('got display:%s, score:%s for %s w/ median: %s' %
    #             (display, score, test.key, median))

  return score, display


def GetStatsDataTemplatized(params, template='table'):
  """Returns the stats table run through a template.

  Args:
    params: Example:
            params = {
              'v': one of the keys in user_agent.BROWSER_NAV,
              'current_user_agent': a user agent entity,
              'user_agents': list_of user agents,
              'tests': list of test names,
              'stats': dict - stats[test_name][user_agent],
              'total_runs': total_runs[test_name],
              'request_path': request.path,
              'params': result_parent.params, #optional
            }

  """
  params['browser_nav'] = BROWSER_NAV[:]
  params['is_admin'] = users.is_current_user_admin()
  if not re.search('\?', params['request_path']):
    params['request_path'] = params['request_path'] + '?'
  t = loader.get_template('stats_%s.html' % template)
  template_rendered = t.render(Context(params))
  return template_rendered


@decorators.dev_appserver_only
@decorators.admin_required
def SeedDatastore(request):
  """Seed Datastore."""

  NUM_RECORDS = 1
  category = request.GET.get('category')
  if category:
    categories = [category]
  else:
    categories = settings.CATEGORIES
  increment_counts = request.GET.get('increment_counts', True)
  if increment_counts == '0':
    increment_counts = False

  def _GetRandomScore(test):
    return random.randrange(test.min_value, test.max_value + 1)

  for user_agent_string in TOP_USER_AGENT_STRINGS:
    user_agent = UserAgent.factory(user_agent_string)
    user_agent.update_groups()
    logging.info(' - update_groups: %s', user_agent.pretty())
  for category in categories:
    test_set = all_test_sets.GetTestSet(category)
    logging.info(' -- category: %s', category)
    for user_agent_string in TOP_USER_AGENT_STRINGS:
      logging.info(' ---- browser: %s',
                   UserAgent.factory(user_agent_string).pretty())
      for i in range(NUM_RECORDS):
        results_str = ','.join(['%s=%s' % (test.key, _GetRandomScore(test))
                               for test in test_set.tests])
        params_str = None
        if test_set.default_params:
          params_str = str(test_set.default_params)
        result_parent = ResultParent.AddResult(
            test_set, '1.2.3.4', user_agent_string, results_str, params_str)
        logging.info(' ------ AddResult, %s of %s: %s',
                     i + 1, NUM_RECORDS, results_str)
        if increment_counts:
          result_parent.increment_all_counts()
          logging.info(' ------ INCREMENTED ALL COUNTS')

  memcache.flush_all()
  return http.HttpResponseRedirect('?message=Datastore got seeded.')


@decorators.admin_required
def UpdateDatastore(request):
  """Generic datastore munging routine."""

  # user_agent = UserAgent.factory(TOP_USER_AGENT_STRINGS[0])
  # query = db.Query(TestTime)
  # test_times = query.fetch(1000, 0)
  # for test_time in test_times:
  #   test_time.user_agent = user_agent
  #   test_time.put()
  # return http.HttpResponse('All Done')

  query = db.Query(UserAgent)
  key = request.GET.get('key')
  if key:
    query.filter('__key__ >', db.Key(key))
  query.order('__key__')
  record = query.get()
  if not record:
    return http.HttpResponse('All Done!')

  record.update_groups()

  params = {
    'next_url': '/update_datastore?key=%s' % record.key(),
    'current_name': record.get_string_list(),
    'next_name': 'nextosity'
  }
  return Render(request, 'update_datastore.html', params)


@decorators.admin_required
def ClearDatastore(request):
  """Clears data in the datastore, many at a time (for admins only)."""
  clear = (None, 'None')
  atatime = 10

  msg = ''
  query = db.Query(clear[0])
  rows = query.fetch(atatime)
  length = len(rows)
  if length is 0:
    msg += 'No more rows to delete<br>'
  else:
    msg += 'Deleting %s %s<br>' % (length, clear[1])
    db.delete(rows)
    query = db.Query(clear[0])
    more = query.fetch(1)
    if len(more) is not 0:
      msg += 'Now do it again!'
      msg += '<script>window.location.href="/reflows/clear_datastore";</script>'
  return http.HttpResponse(msg)


@decorators.dev_appserver_only
@decorators.check_csrf
def FakeCheckCsrf(request):
  return http.HttpResponse('yo')


def UserAgents(request):
  user_agents = UserAgent.all().fetch(1000)
  ua_csv = '\n'.join(
    ['%s,%s,"%s"' % (x.pretty(), x.key().id_or_name(), x.string)
     for x in user_agents])
  return http.HttpResponse(ua_csv, mimetype="text/csv")
