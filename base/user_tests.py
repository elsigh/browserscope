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


import logging
import re

from google.appengine.api import users
from google.appengine.api import datastore_errors
from google.appengine.ext import deferred
from google.appengine.ext import db

import django
from django import http
from django import shortcuts
from django.template import loader, Context

import models.user_test
from base import decorators
from base import util

#from third_party.mirorrr import mirror

from django.template import add_to_builtins
add_to_builtins('base.custom_filters')

def TestHowto(request):
  params = {}
  return util.Render(request, 'user_test_howto.html', params)

#@decorators.login_required
@decorators.admin_required
#@decorators.provide_check_csrf
def Settings(request):
  logging.info('Settings start.')
  if request.POST:
    current_user = users.get_current_user()
    u = models.user_test.User.get_or_insert(current_user.user_id())
    u.email = request.POST.get('email', current_user.email())
    u.save()
    return http.HttpResponseRedirect('/user/settings')

  # Regular GET.
  current_user = users.get_current_user()
  logging.info('current user: %s' % current_user)
  u = models.user_test.User.get_or_insert(current_user.user_id(),
      email=current_user.email())
  tests = db.Query(models.user_test.Test)
  tests.filter('user', u)
  if tests.count() == 0:
    tests = None

  params = {
    'api_key': current_user.user_id(),
    'tests': tests,
    'csrf_token': request.session.get('csrf_token')
  }
  return util.Render(request, 'user_settings.html', params)


@decorators.admin_required
@decorators.provide_check_csrf
def TestCreate(request):
  return TestEdit(request, None)

@decorators.admin_required
@decorators.provide_check_csrf
def TestEdit(request, key):
  test = None
  error_msg = None
  current_user = users.get_current_user()

  if key:
    test = models.user_test.Test.get_mem(key)
    if test.user != current_user and not users.is_current_user_admin():
      return http.HttpResponse('You cannot mess with this test duder.')

  if request.POST:
    user = models.user_test.User.get_by_key_name(current_user.user_id())

    try:
      if test:
        test.name = request.POST.get('name')
        test.url = request.POST.get('url')
        test.description = request.POST.get('description')
      else:
        test = models.user_test.Test(user=user, name=request.POST.get('name'),
                                url=request.POST.get('url'),
                                description=request.POST.get('description'))
      test.save()
      test.add_memcache()
      return http.HttpResponseRedirect('/user/settings')

    # Note: that syntax totally didn't work in prod app engine.
    #except datastore_errors.BadValueError as strerror:
    except datastore_errors.BadValueError, e:
      error_msg = e
      test = {
        'name': request.POST.get('name'),
        'url': request.POST.get('url'),
        'description': request.POST.get('description')
      }
    except:
      error_msg = 'Something did not quite work there, very sorry'
      test = {
        'name': request.POST.get('name'),
        'url': request.POST.get('url'),
        'description': request.POST.get('description')
      }

  params = {
    'test': test,
    'error_msg': error_msg,
    'csrf_token': request.session.get('csrf_token')
  }
  return util.Render(request, 'user_test_form.html', params)


def RawTestData(request, key):
  test = models.user_test.Test.get_mem(key)

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


def TestStatsTable(request, key):
  test = models.user_test.Test.get_mem(key)
  if not test:
    msg = 'No test was found with test_key %s.' % key
    logging.info(msg)
    return http.HttpResponseServerError(msg)

  output = request.GET.get('o', 'html')
  if output not in ['html', 'pickle', 'xhr', 'csv',
                    'gviz', 'gviz_data', 'gviz_timeline_data']:
    return http.HttpResponse('Invalid output specified')

  fields = request.GET.get('f')
  if fields:
    test_keys = fields.split(',')
  else:
    test_keys = test.test_keys
  test_set = test.get_test_set_from_test_keys(test_keys)

  stats_table = util.GetStats(request, test_set, output)
  simple_layout = request.GET.get('layout') == 'simple'
  params = {
    'hide_nav': simple_layout,
    'hide_footer': simple_layout,
    'test': test,
    'stats_table': stats_table
  }
  return util.Render(request, 'user_test_table.html', params)


@decorators.admin_required
def TestView(request, key):
  test = models.user_test.Test.get_mem(key)

  #TODO(elsigh): Remove this.
  #mirror.DEBUG = True
  #mirror.EXPIRATION_DELTA_SECONDS = 1
  #mirror.EXPIRATION_RECENT_URLS_SECONDS = 1

  mirrored_content = None
  if not request.GET.get('sc'):
    mirrored_content = test.get_mirrored_content()
    mirrored_content = None
    #logging.info('mc from memcache: %s' % mirrored_content)
  if mirrored_content is None:
    #logging.info('store w/ key: %s' % test.get_memcache_keyname())
    mirrored_content = mirror.MirroredContent.fetch_and_store(
        key_name=test.get_memcache_keyname(),
        base_url=test.get_base_url(),
        translated_address=request.get_full_path(),
        mirrored_url=test.url)
  params = {
    'mirrored_content': mirrored_content
  }
  return util.Render(request, 'user_test.html', params)


@decorators.admin_required
def Test(request, key):
  """Loads the test frameset for a category."""
  test = models.user_test.Test.get_mem(key)
  params = {
    'category': test.get_memcache_keyname(),
    'page_title': '%s' % test.name,
    'continue': request.GET.get('continue', ''),
    'autorun': '',
    'testurl': '',
    'test': test,
    'test_page': test.url
  }
  #return shortcuts.render_to_response('test_frameset.html', params)
  return util.Render(request, 'test_frameset.html', params)


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

  params = {
    'test_key': test.key(),
    'csrf_token': request.session.get('csrf_token'),
    'callback': request.GET.get('callback'),
    'server': util.GetServer(request)
  }
  return shortcuts.render_to_response('user_test_beacon.js', params,
                                      mimetype='text/javascript')



