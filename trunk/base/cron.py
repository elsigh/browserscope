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

"""Shared cron handlers."""

__author__ = 'elsigh@google.com (Lindsey Simon)'

import logging
import time
import traceback

from google.appengine.api import memcache
from google.appengine.ext import db

import django
from django import http

from categories import all_test_sets
from models import result_stats
from models.result import ResultParent
from models.user_agent import UserAgent

from base import decorators
from base import util
import settings

from django.template import add_to_builtins
add_to_builtins('base.custom_filters')

from mapreduce import control

def UpdateRecentTests(request):
  max_recent_tests = 10
  visible_categories = all_test_sets.GetVisibleTestSets()
  #logging.info('visible_categories %s' % visible_categories)

  prev_recent_tests = memcache.get(util.RECENT_TESTS_MEMCACHE_KEY)
  prev_result_parent_key = None
  if prev_recent_tests:
    prev_result_parent_key = prev_recent_tests[0]['result_parent_key']

  recent_tests = []
  recent_query = db.Query(ResultParent).order('-created').filter('category IN',
      [vis.category for vis in visible_categories])
  for result_parent in recent_query.fetch(max_recent_tests):
    if str(result_parent.key()) == prev_result_parent_key:
      num_needed = max_recent_tests - len(recent_tests)
      if num_needed == max_recent_tests:
        return http.HttpResponse('No update needed.')
      else:
        recent_tests.extend(prev_recent_tests[:num_needed])
        break
    recent_scores = result_parent.GetResults()
    test_set = all_test_sets.GetTestSet(result_parent.category)
    visible_test_keys = [t.key for t in test_set.VisibleTests()]
    recent_stats = test_set.GetStats(visible_test_keys, recent_scores)
    recent_tests.append({
        'result_parent_key': str(result_parent.key()),
        'category': result_parent.category,
        'created': result_parent.created,
        'user_agent_pretty': result_parent.user_agent.pretty(),
        'score': recent_stats['summary_score'],
        'display': recent_stats['summary_display'],
        })
  #logging.info('Setting recent tests: %s' % recent_tests)
  memcache.set(util.RECENT_TESTS_MEMCACHE_KEY, recent_tests,
               time=settings.STATS_MEMCACHE_TIMEOUT)
  #logging.info('Read recent tests: %s' %
  #    memcache.get(key=util.RECENT_TESTS_MEMCACHE_KEY))
  return http.HttpResponse('Done')


@decorators.admin_required
def UpdateUserTestBeaconCounts(request):
  """Starts mapreducer.UserTestBeaconCount."""
  mr_id = control.start_map(
      'UserTest beacon_count update',
      'base.mapreducer.UserTestBeaconCount',
      'mapreduce.input_readers.DatastoreInputReader',
      {'entity_kind': 'models.user_test.Test'})
  return http.HttpResponse('Started MR w/ ID:%s' % mr_id)
