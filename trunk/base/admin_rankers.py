#!/usr/bin/python2.5
#
# Copyright 2009 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the 'License')
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Handle administrative tasks for rankers (i.e. median trees)."""

__author__ = 'slamm@google.com (Stephen Lamm)'

import logging
import time
import traceback

from google.appengine.ext import db
from google.appengine.runtime import DeadlineExceededError

from base import decorators
from categories import all_test_sets
import models
from models import result_ranker
from models import result_stats

import util

import django
from django import http
from django.utils import simplejson

from django.template import add_to_builtins
add_to_builtins('base.custom_filters')


@decorators.admin_required
def FixFirefoxBetaCategories(request):
  query = db.Query(result_stats.CategoryBrowserManager)
  key = request.GET.get('key')
  if key:
    query.filter('__key__ >', db.Key(key))
  query.order('__key__')
  bm = query.get()
  if not bm:
    return http.HttpResponse('All Done!')

  dirty = False
  newbrowsers = []
  for browser in bm.browsers:
    if browser.find('Firefox 4') != -1:
      dirty = True
      browser = browser.replace('Firefox 4', 'Firefox Beta 4')
    newbrowsers.append(browser)

  if dirty:
    bm.browsers = newbrowsers
    bm.save()

  params = {
    'next_url': '/admin/ua/ffbeta?key=%s' % bm.key(),
    'current_name': 'Dirty? %s - %s' % (dirty, newbrowsers)
  }
  return util.Render(request, 'update_datastore.html', params)


@decorators.admin_required
def FixFirefoxBeta(request):
  query = db.Query(models.user_agent.UserAgent)
  query.filter('family =', 'Firefox')
  query.filter('v3 =', 'b5')
  key = request.GET.get('key')
  if key:
    query.filter('__key__ >', db.Key(key))
  query.order('__key__')
  user_agent = query.get()
  if not user_agent:
    return http.HttpResponse('All Done!')

  # Do something with user_agent here.
  user_agent.family = 'Firefox Beta'
  user_agent.save()

  params = {
    'next_url': '/admin/ua/ffbeta?key=%s' % user_agent.key(),
    'current_name': user_agent.get_string_list(),
    'next_name': 'nextosity'
  }
  return util.Render(request, 'update_datastore.html', params)


@decorators.admin_required
def UploadRankers(request):
  """Rebuild rankers."""
  time_limit = int(request.REQUEST.get('time_limit', 8))
  category = request.REQUEST.get('category')
  params_str = request.REQUEST.get('params_str')
  test_key_browsers_json = request.REQUEST.get('test_key_browsers_json')
  ranker_values_json = request.REQUEST.get('ranker_values_json')

  if not category:
    return http.HttpResponseServerError('Must send "category".')
  if not test_key_browsers_json:
    return http.HttpResponseServerError('Must send "test_key_browsers_json".')
  if not ranker_values_json:
    return http.HttpResponseServerError('Must send "ranker_values_json".')

  test_key_browsers = simplejson.loads(test_key_browsers_json)
  ranker_values = simplejson.loads(ranker_values_json)
  start_time = time.clock()

  message = None
  test_set = all_test_sets.GetTestSet(category)
  test_browsers = [(test_set.GetTest(test_key), browser)
                   for test_key, browser in test_key_browsers]
  rankers = result_ranker.GetOrCreateRankers(test_browsers, params_str)

  for ranker, (median, num_scores, values_str) in zip(rankers, ranker_values):
    if time.clock() - start_time > time_limit:
      message = 'Over time limit'
      break
    if ranker.GetMedianAndNumScores() == (median, num_scores):
      logging.info('Skipping ranker with unchanged values: %s',
                   ranker.key().name())
      continue
    values = map(int, values_str.split('|'))
    try:
      ranker.SetValues(values, num_scores)
    except db.Timeout:
      message = 'db.Timeout'
      break
  response_params = {}
  if message:
    logging.info('message: %s', message)
    response_params['message'] = message
  return http.HttpResponse(simplejson.dumps(response_params))
