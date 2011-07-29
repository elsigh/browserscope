#!/usr/bin/python2.5
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

"""User handlers and functions."""

__author__ = 'elsigh@google.com (Lindsey Simon)'


import cgi
import hashlib
import logging
import random
import re
import time
import urllib
import urlparse

from google.appengine.api import users
from google.appengine.api import datastore_errors
from google.appengine.api import memcache
from google.appengine.api import urlfetch

from google.appengine.ext import db

import django
from django import http
from django import shortcuts
from django.template import loader, Context
from django.utils import simplejson

import models.user_test
from base import decorators
from base import util

from third_party.gviz import gviz_api
from third_party.gaefy.db import pager

from django.template import add_to_builtins
add_to_builtins('base.custom_filters')

import settings


def TestHowto(request):
  params = {
    'max_value': models.user_test.MAX_VALUE,
    'max_key_count': models.user_test.MAX_KEY_COUNT
  }
  return util.Render(request, 'user_test_howto.html', params)


@decorators.login_required
@decorators.provide_check_csrf
def Settings(request):
  if request.POST:
    current_user = users.get_current_user()
    u = models.user_test.User.get_or_insert(current_user.user_id())
    u.email = request.POST.get('email', current_user.email())
    u.save()
    return http.HttpResponseRedirect('/user/settings')

  # Regular GET.
  current_user = users.get_current_user()
  user = models.user_test.User.get_or_insert(
      current_user.user_id(),
      email=current_user.email())
  tests = db.Query(models.user_test.Test)
  tests.filter('user', user)
  # Only admins can see deleted tests.
  if not users.is_current_user_admin():
    tests.filter('deleted', False)
  tests.order('-created')
  if tests.count() == 0:
    tests = None

  params = {
    'api_key': user.key().name(),
    'tests': tests,
    'csrf_token': request.session.get('csrf_token')
  }
  return util.Render(request, 'user_settings.html', params)


# Decorators are inherited by TestEdit
def TestCreate(request):
  return TestEdit(request, None)


_MAX_SANDBOXID = 18446744073709551616L
_MAX_SANDBOXID_LEN = 15
def _get_random_sandboxid():
  # Use the system (hardware-based) random number generator if it exists.
  if hasattr(random, 'SystemRandom'):
    randrange = random.SystemRandom().randrange
  else:
    randrange = random.randrange
  sanboxid_md5 = hashlib.md5('%s' % (randrange(0, _MAX_SANDBOXID)))
  sanboxid = sanboxid_md5.hexdigest()[0:_MAX_SANDBOXID_LEN]
  return sanboxid


@decorators.api_key_override
@decorators.login_required
@decorators.provide_check_csrf
@decorators.api_key_override_tidy
def TestEdit(request, key):
  test = None
  error_msg = None
  current_user = users.get_current_user()
  api_key = request.REQUEST.get('api_key')

  # If a key was provided in the endpoint that means this is an edit.
  if key:
    test = models.user_test.Test.get_mem(key)
    meta = models.user_test.TestMeta.get_mem_by_test(test)
    if (test.user.key().name() != current_user.user_id() and not
        users.is_current_user_admin()):
      return http.HttpResponse('You can\'t play with tests you don\'t own')

  if api_key or request.POST:
    # api_key should map to a User.key()
    if api_key:
      user = models.user_test.User.get_by_key_name(api_key)
      if not user:
        return http.HttpResponse('No user was found with an api_key=%s' %
                                 api_key)
    else:
      user = models.user_test.User.get_by_key_name(current_user.user_id())

    try:
      # edit
      if test:
        test.name = request.REQUEST.get('name')
        test.url = request.REQUEST.get('url')
        test.description = request.REQUEST.get('description')
        deleted = request.REQUEST.get('deleted')
        if deleted == '1':
          test.deleted = True
        logging.info('deleted: %s' % test.deleted)
        if request.REQUEST.get('sandboxid'):
          test.sandboxid = request.REQUEST.get('sandboxid')
        test.test_keys = request.REQUEST.get('test_keys').split(',')
      # create
      else:
        meta = models.user_test.TestMeta().save()
        test = models.user_test.Test(
                   user=user,
                   name=request.REQUEST.get('name'),
                   url=request.REQUEST.get('url'),
                   description=request.REQUEST.get('description'),
                   sandboxid=request.REQUEST.get('sandboxid',
                                                 _get_random_sandboxid()),
                   meta=meta)
      test.save()
      test.add_memcache()

      if api_key:
        return http.HttpResponse('{"test_key": "%s"}' % test.key(),
                                 mimetype='application/json')
      else:
        return http.HttpResponseRedirect('/user/settings')

    # App Engine model caught a validation exception.
    except datastore_errors.BadValueError, error_msg:
      if api_key:
        msg = 'Validation error: %s' % error_msg
        logging.info(msg)
        return http.HttpResponseServerError(msg)

      request = decorators.add_csrf_to_request(request)
      test = {
        'name': request.REQUEST.get('name'),
        'url': request.REQUEST.get('url'),
        'description': request.REQUEST.get('description'),
        'sandboxid': request.REQUEST.get('sandboxid')
      }
    # Do not try to catch / variable-ize this exception, it breaks in
    # production.
    except:
      error_msg = 'Something did not quite work there, very sorry.'
      logging.info(error_msg)
      if api_key:
        return http.HttpResponseServerError(error_msg)

      request = decorators.add_csrf_to_request(request)
      test = {
        'name': request.REQUEST.get('name'),
        'url': request.REQUEST.get('url'),
        'description': request.REQUEST.get('description'),
        'sandboxid': request.REQUEST.get('sandboxid')
      }

  params = {
    'test': test,
    'sandboxid': _get_random_sandboxid(),
    'max_sandboxid_len': _MAX_SANDBOXID_LEN,
    'error_msg': error_msg,
    'csrf_token': request.session.get('csrf_token')
  }
  return util.Render(request, 'user_test_form.html', params)


@decorators.login_required
def RawTestData(request, key):
  current_user = users.get_current_user()

  if not key:
    return http.HttpResponse('No key.')

  test = models.user_test.Test.get_mem(key)
  if (test.user.key().name() != current_user.user_id() and not
      users.is_current_user_admin()):
    return http.HttpResponse('You cannot mess with this test duder.')

  fields = request.GET.get('f')
  if fields:
    test_keys = fields.split(',')
  else:
    test_keys = test.test_keys

  result_parents = db.Query(models.result.ResultParent)
  result_parents.filter('category', test.get_memcache_keyname())
  result_parents.order('created')
  lines = []
  for result_parent in result_parents:
    line = [
      '"%s"' % result_parent.created,
      '"%s"' % result_parent.user_agent.string,
      '"%s"' % result_parent.user_agent.family,
      '"%s"' % result_parent.user_agent.v1,
      '"%s"' % result_parent.user_agent.v2,
      '"%s"' % result_parent.user_agent.v3]

    result_times_dict = result_parent.GetResults()
    for test_key in test_keys:
      line.append('"%s"' % result_times_dict[test_key])

    lines.append(line)

  headers = ['"Created"', '"UA String"', '"UA Family"', '"v1"', '"v2"', '"v3"']
  for test_key in test_keys:
    headers.append('"%s"' % test_key)

  line_delim = '\n'
  out = ','.join(headers) + line_delim
  for line in lines:
    out += ','.join(line) + line_delim
  #return http.HttpResponse(out)
  return http.HttpResponse(out, mimetype='text/csv')


def Button(request):
  """Draws a Run the test button on the page for a user."""
  params = {
    'mimetype': 'text/javascript',
    'fn': request.GET.get('fn', '_bRunTest'),
    'btn_text': request.GET.get('btn_text', 'Run the test'),
    'cb_text': request.GET.get('cb_text',
        'and send my results to Browserscope (anonymously)'),
  }
  return util.Render(request, 'user_test_button.js', params)


def Table(request, key):
  """The User Test results table.
  Args:
    request: The request object.
    key: The Test.key() string.
  """
  test = models.user_test.Test.get_mem(key)
  if not test:
    msg = 'No test was found with test_key %s.' % key
    return http.HttpResponseServerError(msg)

  params = {
    'hide_nav': True,
    'hide_footer': True,
    'test': test,
  }

  return util.GetResults(request, 'user_test_table.html', params,
                         test.get_test_set())


def Index(request):
  """Shows a table of user tests."""
  output = request.GET.get('o')
  if output == 'gviz_table_data':
    return http.HttpResponse(FormatUserTestsAsGviz(request))
  else:
    params = {
      'height': '400px',
      'width': 'auto',
      'page_size': 20
    }
    return util.Render(request, 'user_tests_index.html', params)


# Note this is *not* checked in.
WEBPAGETEST_KEY = ''
try:
 import settings_webpagetest
 WEBPAGETEST_KEY = settings_webpagetest.KEY
except:
  pass
WEBPAGETEST_URL = ('http://www.webpagetest.org/runtest.php?k=%s'
                   '&priority=3&fvonly=1&noopt=1&noimages=1'
                   '&noheaders=1&f=json' % WEBPAGETEST_KEY)
WEBPAGETEST_STATUS_URL = 'http://www.webpagetest.org/testStatus.php?f=xml&test='
WEBPAGETEST_LOCATIONS_URL = 'http://www.webpagetest.org/getLocations.php?f=xml'
WEBPAGETEST_LOCATIONS = ('Dulles_IE6', 'Dulles_IE7', 'Dulles_IE8',
                         'Dulles_IE9')

@decorators.login_required
def WebPagetest(request, key):
  """Sends an API request to run one's test page on WebPagetest.org."""
  test = models.user_test.Test.get_mem(key)
  if not test:
    msg = 'No test was found with test_key %s.' % key
    return http.HttpResponseServerError(msg)

  current_user = users.get_current_user()
  if (test.user.key().name() != current_user.user_id() and not
        users.is_current_user_admin()):
      return http.HttpResponse('You can\'t play with tests you don\'t own')

  # Help users autorun their tests by adding autorun=1 to the test url.
  test_url_parts = list(urlparse.urlparse(test.url))
  test_url_query = dict(cgi.parse_qsl(test_url_parts[4]))
  test_url_query.update({'autorun': '1'})
  test_url_parts[4] = urllib.urlencode(test_url_query)
  test_url = urlparse.urlunparse(test_url_parts)

  # TODO(elsigh): callback url.
  webpagetest_url = ('%s&url=%s&notify=%s' %
                     (WEBPAGETEST_URL, test_url,
                      urllib.quote('elsigh@gmail.com')))

  webpagetests = {}
  # See http://goo.gl/EfK1r for WebPagetest instructions.
  for location in WEBPAGETEST_LOCATIONS:
    url = '%s&location=%s' % (webpagetest_url, location)
    response = urlfetch.fetch(url)
    json = simplejson.loads(response.content)
    webpagetests[location] = json

  params = {
    'test': test,
    'webpagetests': webpagetests
  }
  return util.Render(request, 'user_test_webpagetest.html', params)



def FormatUserTestsAsGviz(request):
  tq = request.GET.get('tq')
  tqx = request.GET.get('tqx')
  limit = int(request.GET.get('limit', 10))
  bookmark = request.GET.get('bookmark')

  description = [('created', 'datetime', 'Created'),
                 ('author', 'string', 'Author'),
                 ('name', 'string', 'Test'),
                 ('description', 'string', 'Description'),
                 ('results', 'string', 'Results'),
                 ('beacon_count', 'number', '# Tests')]


  query = (pager.PagerQuery(models.user_test.Test).
       filter('deleted =', False).
       order('-beacon_count').
       order('-created'))
  prev_bookmark, results, next_bookmark = query.fetch(limit, bookmark)
  if prev_bookmark is None:
    prev_bookmark = ''
  if next_bookmark is None:
    next_bookmark = ''

  data = []
  for test in results:
    data.append([test.created,
                 re.sub(r'\@.+', '', test.user.email),
                 #test.user.key(),
                 '<a href="%s">%s</a>' % (test.url, test.name),
                 test.description,
                 '<a href="/user/tests/table/%s">Table</a>' % test.key(),
                 test.beacon_count])

  custom_properties = {
    'prev_bookmark': prev_bookmark,
    'next_bookmark': next_bookmark
  }
  data_table = gviz_api.DataTable(description, data, custom_properties)
  return data_table.ToResponse(tqx=tqx)


@decorators.provide_csrf
def BeaconJs(request, key):

  test = models.user_test.Test.get_mem(key)
  if not test:
    return http.HttpResponseServerError('No test key sent or no tests match.')

  # TODO(elsigh): Is referer check enough prevent abuse? IP-based better?
  do_referer_check = False
  if do_referer_check:
    referer = request.META.get('HTTP_REFERER', None)
    if referer is None:
      msg = 'No referer, no beacon.'
      logging.info(msg)
      return http.HttpResponseServerError(msg)
    if not re.match(test.url, referer):
      msg = 'Referer check failed.'
      logging.info(msg)
      return http.HttpResponseServerError(msg)

  # Get the ua-parser project's js override functionality.
  f = open('third_party/uaparser/resources/user_agent_overrides.js', 'r')
  js_ua_override = f.read()
  f.close()

  params = {
    'test_key': test.key(),
    'test_results_var': request.GET.get(
        'test_results_var', settings.USER_TEST_RESULTS_VAR_DEFAULT),
    'csrf_token': request.session.get('csrf_token'),
    'server': util.GetServer(request),
    'sandboxid': request.GET.get('sandboxid', ''),
    'epoch': int(time.time()),
    'js_ua_override': js_ua_override,
  }

  # Does the user want a callback?
  callback = request.GET.get('callback')
  if callback:
    params['callback'] = callback

  response = shortcuts.render_to_response('user_test_beacon.js', params,
                                          mimetype='text/javascript')

  # Add on a P3P header so that the provide_csrf will work as a third-party
  # cookie for IE security happiness.
  # Reference: http://www.w3.org/P3P/
  # To be fair, I copied this example string from a blog and it works in IE.
  # I did not spend the 6 hours it looks like it would take to read this
  # documentation nor did I spend $39 for the P3PEdit service ;0
  # So I'm not sure that this string honestly represents our cookie policy.
  response['P3P'] = ('CP="NOI DSP COR NID ADM DEV PSA OUR IND UNI PUR COM '
                     'NAV INT STA"')

  return response

