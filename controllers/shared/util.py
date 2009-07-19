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
import re
import sys
import urllib2

from google.appengine.api import memcache
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.api.labs import taskqueue

import django
from django import http
from django import shortcuts
from django.template import loader, Context

from django.template import add_to_builtins
add_to_builtins('custom_filters')

from settings import *

from models.result import *
from models.user_agent import *
from models import result_ranker
from controllers import all_test_sets
from controllers.shared import decorators


#@decorators.trusted_tester_required
def Render(request, template, params={}, category=None):
  """Wrapper function to render templates with global and category vars."""

  params['app_title'] = APP_TITLE
  params['app_categories'] = []
  params['is_admin'] = users.is_current_user_admin()
  #http://code.google.com/appengine/docs/python/users/userclass.html#User_user_id
  current_user = users.get_current_user()
  if current_user:
    params['user_id'] = current_user.user_id()
    params['is_elsigh'] = current_user.nickname() == 'elsigh'
  else:
    params['is_elsigh'] = False
    params['user_id'] = None
  params['sign_in'] = users.create_login_url(request.get_full_path())
  params['sign_out'] = users.create_logout_url('/')

  # Creates a list of tuples categories and their ui names.
  for i, test_set in enumerate(all_test_sets.GetTestSets()):
    params['app_categories'].append([test_set.category, test_set.category_name])
    # Select the current page's category.
    if category and category == test_set.category:
      params['app_category'] = test_set.category
      params['app_category_index'] = i
  return shortcuts.render_to_response(template, params)


def GetServer(request):
  """A utility function for getting the server and port."""
  server = request.META['SERVER_NAME']
  server_port = request.META['SERVER_PORT']
  if server_port != '80':
    server = server + ':' + server_port
  return server


def ParseResults(results_string):
  """Parses a results string.
  Args:
    raw_results: a string like 'test1=time1,test2=time2,[...]'.
  Returns:
    [(test1, time1), (test2, time2)]
  """
  return [x.split('=') for x in results_string.split(',')]


# These are things which do not get urlquoted in Javascript, however do
# get quoted by urllib2.quote. We need to undo that.
# TODO(elsigh): More research on this - are there others? lame.
PARSE_PARAMS_JS_EXCEPTIONS = {
  '*': '%2A'
}
def ParamsListToDict(params, unquote=True, quote=False, return_order=False):
  """Turns a params list into an dict."""
  parsed_params = {}
  order = []
  for param in params:
    split = param.split('=')
    # if it's not key=val, then don't put it in the parsed_params.
    if len(split) != 2:
      parsed_params[param] = ''
      order.append(param)
      continue

    name = split[0]
    val = split[1]
    order.append(name)

    if unquote:
      val = urllib2.unquote(val)
    if quote:
      val = urllib2.quote(val)
      for orig, quoted in PARSE_PARAMS_JS_EXCEPTIONS.items():
        val = re.sub(quoted, orig, val)
    parsed_params[name] = val

  if return_order:
    return parsed_params, order
  else:
    return parsed_params


def ParamsStringToList(params):
  """Converts a string of params into a list."""
  raw_params_list = params.split(',')
  parsed_params, order = ParamsListToDict(raw_params_list, quote=True,
                                          return_order=True)
  params = []
  # Adds back in all the cruft so things match. Ugh.
  for key in order:
    if parsed_params[key]:
      params.append('%s=%s' % (key, parsed_params[key]))
    else:
      params.append(key)
  return params


RECENT_TESTS_MEMCACHE_KEY = 'recent_tests'
def Home(request):
  """Our Home page."""

  # If we don't find anything in memcache, we just won't show the recent
  # tests on the homepage. Should happen VERY rarely.
  recent_tests = memcache.get(key=RECENT_TESTS_MEMCACHE_KEY)
  if not recent_tests:
    ScheduleRecentTestsUpdate()

  stats_tables = {}
  intro_text = {}
  for test_set in all_test_sets.GetTestSets():
    stats_tables[test_set.category] = GetStats(request, test_set, output='html')
    intro_text[test_set.category] = test_set.home_intro

  message = request.GET.get('message')

  params = {
    'page_title': 'Home',
    'stats_tables': stats_tables,
    'intro_text': intro_text,
    'recent_tests': recent_tests,
    'message': message
  }
  return Render(request, 'home.html', params)


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


def CheckThrottleIpAddress(ip):
  """Will check for over-zealous beacon abusers and bots."""
  return True


@decorators.admin_required
def ClearMemcache(request):
  message = []

  continue_url = request.GET.get('continue')

  recent = request.GET.get('recent')
  if recent:
    memcache.delete(key=RECENT_TESTS_MEMCACHE_KEY, seconds=0)
    message.append('Cleared memcache for recent tests')

  category = request.GET.get('category')
  if category:
    categories = category.split(',')
  else:
    categories = CATEGORIES

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
      memcache_ua_key = '%s_%s' % (category, user_agent)
      memcache.delete(key=memcache_ua_key, seconds=0,
                      namespace=STATS_MEMCACHE_UA_ROW_NS)
      logging.info('Deleting %s in memcache' % memcache_ua_key)

  message.append('Cleared memcache for categories: %s and '
                 'user_agent_strings: %s' % (categories, user_agent_strings))

  if continue_url:
    if not re.search('\?', continue_url):
      continue_url += '?'
    continue_url += '&message=' + urllib2.quote(' '.join(message))
    return http.HttpResponseRedirect(continue_url)
  else:
   return http.HttpResponse('<br>'.join(message))


def ScheduleDirtyUpdate():
  try:
    taskqueue.Task(method='GET').add(queue_name='update-dirty')
  except:
    logging.info('Cannot add task: %s:%s' % (sys.exc_type, sys.exc_value))


def ScheduleRecentTestsUpdate():
  try:
    taskqueue.Task(method='GET').add(queue_name='recent-tests')
  except:
    logging.info('Cannot add task: %s:%s' % (sys.exc_type, sys.exc_value))


BEACON_COMPLETE_CB_RESPONSE = 'BEACON_COMPLETE = 1;'
@decorators.check_csrf
def Beacon(request):
  """Records result times in the datastore.
  This is the handler for after a test is done.
  ex: /beacon?category=reflow&csrf_token=number&results=tes1=150,test2=300
  """
  callback = request.GET.get('callback', None)
  category = request.GET.get('category', None)
  results_string = request.GET.get('results', None)
  if category is None or results_string is None:
    return http.HttpResponse(BAD_BEACON_MSG)
  results = ParseResults(results_string)
  logging.info('Beacon results: %s' % results)

  ip = request.META.get('REMOTE_ADDR')
  ip_ok = CheckThrottleIpAddress(ip)
  if not ip_ok:
    return http.HttpResponseServerError(BAD_BEACON_MSG)

  # hash ip address
  ip = hashlib.md5(ip).hexdigest()

  user_agent_string = request.META.get('HTTP_USER_AGENT')
  user = users.get_current_user()

  params = request.GET.get('params', [])
  if params and params != '':
    params = ParamsStringToList(params)
  logging.info('Beacon params: %s' % params)

  result_parent = ResultParent.AddResult(category, ip, user_agent_string,
                                         results, params=params, user=user)
  ScheduleDirtyUpdate()
  ScheduleRecentTestsUpdate()

  if callback:
    return http.HttpResponse(BEACON_COMPLETE_CB_RESPONSE)
  else:
    # Return a successful empty 204.
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
    output: Output type html or else you get a dict of params.
    opt_tests: list of tests.
    use_memcache: Use memcache or not.
  """
  version_level = request.GET.get('v', 'top')
  user_agent_group_strings = UserAgentGroup.GetStrings(version_level)

  tests = [test for test in opt_tests or test_set.tests
           if not hasattr(test, 'is_hidden_stat') or not test.is_hidden_stat]
  stats = GetStatsData(test_set.category, tests, user_agent_group_strings,
                       test_set.default_params, use_memcache, version_level)

  # Looks for a category_results=test1=X,test2=X url GET param.
  results = None
  for category in CATEGORIES:
    results_val = request.GET.get('%s_results' % category)
    if results_val and category == test_set.category:
      results = dict(ParseResults(results_val))

  current_ua_string = None
  current_ua = UserAgent.factory(request.META['HTTP_USER_AGENT'])
  current_ua_list = current_ua.get_string_list()

  # Set the current_ua to a string matching one of the user agents.
  for group_string in user_agent_group_strings:
    #logging.info('testing %s vs %s' % (user_agent, current_ua_list))
    if group_string in current_ua_list:
      current_ua_string = group_string
      break

  if not current_ua_string:
    current_ua_string = current_ua.pretty()
    if results:
      user_agent_group_strings.append(current_ua_string)
      user_agent_group_strings.sort()

  if results:
    if not stats.has_key(current_ua_string):
      stats[current_ua_string] = {}
    stats[current_ua_string]['current_results'] = {}
    current_ua_score = 0
    for test in tests:
      stats[current_ua_string]['current_results'][test.key] = {}
      median = results[test.key]
      if median == None:
        median = ''
      stats[current_ua_string]['current_results'][test.key]['median'] = median
      score, display, ua_score = GetScoreAndDisplayValue(test, median)
      stats[current_ua_string]['current_results'][test.key]['score'] = score
      stats[current_ua_string]['current_results'][test.key]['display'] = display
      current_ua_score += ua_score

    stats[current_ua_string]['current_score'] = int(current_ua_score /
                                                    len(tests))

  params = {
    'category': test_set.category,
    'tests': tests,
    'v': version_level,
    'user_agents': user_agent_group_strings,
    'request_path': request.path,
    'current_user_agent': current_ua_string,
    'stats': stats,
    'params': test_set.default_params,
  }
  #logging.info("PARAMS: %s", str(params))
  if output is 'html':
    return GetStatsTableHtml(params)
  else:
    return params


def GetStatsData(category, tests, user_agents, params, use_memcache=True,
                 version_level='top'):
  stats = {}
  total_runs = {}

  for user_agent in user_agents:
    # Checks memcache for user agent row data.
    if use_memcache:
      memcache_ua_key = '%s_%s' % (category, user_agent)
      row = memcache.get(key=memcache_ua_key,
                         namespace=STATS_MEMCACHE_UA_ROW_NS)
      #logging.info('Memcache got %s for UA: %s' % (row, user_agent))
      if row:
        stats[user_agent] = row
        continue

    stats[user_agent] = {}
    stats[user_agent]['results'] = {}
    stats[user_agent]['score'] = 0
    stats['total_runs'] = 0

    user_agent_score = 0
    for test in tests:
      stats[user_agent]['results'][test.key] = {}

      ranker = result_ranker.Factory(category, test, user_agent, params)

      # Median and total
      if not stats[user_agent].has_key('total_runs'):
        median, total_runs = ranker.GetMedianAndNumScores()
        stats[user_agent]['total_runs'] = total_runs
        stats['total_runs'] += total_runs
      else:
        median = ranker.GetMedian(num_scores=stats[user_agent]['total_runs'])
      if median is None:
        median = ''
      stats[user_agent]['results'][test.key]['median'] = median

      score, display, ua_score = GetScoreAndDisplayValue(test, median)
      stats[user_agent]['results'][test.key]['score'] = score
      stats[user_agent]['results'][test.key]['display'] = display
      user_agent_score += ua_score

    stats[user_agent]['score'] = int(user_agent_score / len(tests))

    # Store the stats in memcache if we get here.
    if use_memcache:
      #logging.info('ok, putting %s into %s' % (stats[user_agent],
      #                                         memcache_ua_key))
      memcache.set(key=memcache_ua_key, value=stats[user_agent],
                   time=STATS_MEMCACHE_TIMEOUT,
                   namespace=STATS_MEMCACHE_UA_ROW_NS)

  # If we're not on the top browsers page and we have 0 total runs, then
  # remove from the list.
  if stats[user_agent]['total_runs'] == 0 and version_level != 'top':
    del stats[user_agent]

  return stats


def GetScoreAndDisplayValue(test, median):
  # Score for the template classnames is a value of 0-10.
  if test.score_type == 'boolean':
    # Boolean scores are 1 or 10.
    if median == 0:
      score = 1
      display = STATS_SCORE_FALSE
    else:
      score = 10
      display = STATS_SCORE_TRUE
  elif test.score_type == 'custom':
    # The custom_tests_function returns a score between 1-100 which we'll
    # turn into a 0-10 display.
    score, display = test.GetScoreAndDisplayValue(median)
    score = int(round(float('%s.0' % int(score)) / 10))
    #logging.info('got display:%s, score:%s for %s w/ median: %s' %
    #             (display, score, test.key, median))

  # Normalize very low scores per test for calculating an overall score for
  # the user agent.
  ua_score = score
  if ua_score < 5:
    ua_score = 5
  return score, display, ua_score


def GetStatsTableHtml(params):
  """Returns the HTML of the stats table.

  Args:
    params: Example:
            params = {
              'v': one of the keys in BROWSER_NAV,
              'current_user_agent': a user agent entity,
              'user_agents': list_of user agents,
              'tests': list of test names,
              'stats': dict - stats[test_name][user_agent],
              'total_runs': total_runs[test_name],
              'request_path': request.path,
              'params': result_parent.params, #optional
            }

  """
  params['browser_nav'] = BROWSER_NAV
  params['is_admin'] = users.is_current_user_admin()
  if not re.search('\?', params['request_path']):
    params['request_path'] = params['request_path'] + '?'
  t = loader.get_template('stats_table.html')
  html = t.render(Context(params))
  return html


@decorators.dev_appserver_only
@decorators.admin_required
def SeedDatastore(request):
  """Seed Datastore."""

  NUM_RECORDS = 3
  categories = CATEGORIES

  increment_counts = request.GET.get('increment_counts', True)
  if increment_counts == '0':
    increment_counts = False

  user_agents = []
  for ua_string in TOP_USER_AGENT_STRINGS:
    user_agent = UserAgent.factory(ua_string)
    user_agents.append(user_agent)

  keys = []
  for test_set in all_test_sets.GetTestSets():
    #logging.info('CATEGORY: %s' % test_set.category)
    params = test_set.default_params
    for user_agent in user_agents:
      #logging.info(' - USER AGENT: %s' % user_agent.pretty())
      user_agent_list = user_agent.get_string_list()
      for x in range(1, NUM_RECORDS + 1):
        #logging.info(' -- i: %s' % x)
        result_parent = ResultParent()
        result_parent.category = test_set.category
        result_parent.user_agent = user_agent
        result_parent.user_agent_list = user_agent_list
        result_parent.ip = '1.2.3.4'
        if params:
          result_parent.params = params
        result_parent.put()

        for test in test_set.tests:
          if test.score_type == 'boolean':
            score = random.randrange(0, 1)
          elif test.score_type == 'custom':
            score = random.randrange(5, 2000)
          result_time = ResultTime(parent=result_parent)
          result_time.test = test.key
          result_time.score = score
          result_time.put()
        #logging.info('--------------------')
        #logging.info(' -- PUT ResultParent & ResultTime')
        #logging.info('--------------------')
        if increment_counts:
          result_parent.increment_all_counts()
          #logging.info('--------------------')
          #logging.info(' -- INCREMENTED ALL COUNTS')
          #logging.info('--------------------')

        keys.append(str(result_parent.key()))
        #logging.info('--------------------')
        #logging.info('--------------------')
        #logging.info('--------------------')
        #logging.info('--------------------')

  return http.HttpResponseRedirect('?datastore_seeded')


def UpdateTx(test_time, user_agent):
  result_parent = ResultParent()
  result_parent.category = test_time.category
  result_parent.user_agent = user_agent
  result_parent.user_agent_pretty = test_time.user_agent_pretty
  result_parent.ip = test_time.ip
  result_parent.created = test_time.created
  result_parent.params = test_time.params
  result_parent.put()

  result_time_entities = []
  for test in test_time.get_tests():
    if test == 'test_type':
      continue
    result_time = ResultTime(parent=result_parent)
    result_time.test = test
    result_time.score = int(getattr(test_time, test))
    result_time_entities.append(result_time)
    result_time.dirty = False
  db.put(result_time_entities)


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
