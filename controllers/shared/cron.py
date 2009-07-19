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

"""Shared cron handlers."""

__author__ = 'elsigh@google.com (Lindsey Simon)'

import logging
import random
import re
import sys

from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api.labs import taskqueue


import django
from django import http
from django import shortcuts

from django.template import add_to_builtins
add_to_builtins('custom_filters')

from models.result import ResultParent
from models.result import ResultTime
from models.user_agent import UserAgent
from models.user_agent import UserAgentGroup

import util
import decorators


_CRON_MEMCACHE_TIMEOUT = 30
_CRON_FETCH_SIZE = 20

UPDATE_DIRTY_DONE = 'No more dirty ResultTimes.'
UPDATE_DIRTY_MEMCACHE_NS = 'cron_update_dirty'
def UpdateDirty(request):
  """Updates any dirty tests, adding its score to the appropriate ranker."""
  try:
    query = db.Query(ResultTime)
    query.filter('dirty =', True)

    result_times = query.fetch(_CRON_FETCH_SIZE, 0)

    if not result_times:
      return http.HttpResponse(UPDATE_DIRTY_DONE)

    result_time = random.choice(result_times)
    if result_time.parent().category == 'richtext':
      result_time.dirty = False
      result_time.put()
      return http.HttpResponse('richtext')

    # Create a mutex so we can have multiple workers.
    lock_key = 'cron_' + str(result_time.key())
    if not memcache.add(key=lock_key, value=1, time=_CRON_MEMCACHE_TIMEOUT,
                        namespace=UPDATE_DIRTY_MEMCACHE_NS):
      msg = 'Bummer, unable to acquire lock for update: key=%s.' % lock_key
      return http.HttpResponse(msg, status=403)

    #logging.info('set memcache for key %s' % memcache_keyname)
    result_time.increment_all_counts()

    try:
      taskqueue.Task(method='GET', url='/cron/more_dirty',
          params={'key': result_time.key()}).add(queue_name='update-dirty')
    except:
      logging.info('Cannot add task: %s:%s' % (sys.exc_type, sys.exc_value))

    return http.HttpResponse('UpdateDirty done in category: %s, key: %s' %
                             (result_time.parent().category, result_time.key()))
  except:
    return http.HttpResponse('Things did not go well.')


def MoreDirty(request):
  """Checks to see if there's more work to be done."""
  key = request.GET.get('key')
  if not key:
    return http.HttpResponse('No key')
  key = db.Key(key)


  query = db.Query(ResultTime)
  query.filter('__key__ =', key)
  result_time = query.get()
  if not result_time:
    return http.HttpResponse('No result_time with this key.')

  # If there's more dirty tests add another task OR
  # invalidate GetStatsData memcache for the ua + category combo
  # if all the test times are now accounted for.
  query = db.Query(ResultTime)
  query.ancestor(result_time.parent())
  query.filter('dirty =', True)
  result = query.get()
  if result:
    logging.info('Not done with ResultParent, add another update_dirty task.')
    try:
      taskqueue.Task(method='GET').add(queue_name='update-dirty')
    except:
      logging.info('Cannot add task: %s:%s' % (sys.exc_type, sys.exc_value))

  else:
    logging.info('Finished with this ResultParent\'s TestTimes, '
                 'invalidating memcache...')
    result_parent = result_time.parent()
    result_parent.invalidate_ua_memcache()

    # Are there any more dirty times of any kind?
    query = db.Query(ResultTime)
    query.filter('dirty =', True)
    result = query.get()
    if result:
      logging.info('There are more dirty, spawning update_dirty task.')
      try:
        taskqueue.Task(method='GET').add(queue_name='update-dirty')
      except:
        logging.info('Cannot add task: %s:%s' % (sys.exc_type, sys.exc_value))
    else:
      logging.info('No more dirty of any kind.')

  return http.HttpResponse('MoreDirty done in category: %s, key: %s' %
                           (result_time.parent().category, result_time.key()))


def UserAgentGroup(request):
  key = request.GET.get('key')
  if not key:
    return http.HttpResponse('No key')
  key = db.Key(key)

  query = db.Query(UserAgent)
  query.filter('__key__ =', key)
  user_agent = query.get()
  if not user_agent:
    return http.HttpResponse('No user_agent with this key.')

  user_agent.update_groups()

  return http.HttpResponse('Done with UserAgent key=%s' % key)


def UpdateRecentTests(request):
  query = db.Query(ResultParent)
  query.order('-created')
  recent_tests = query.fetch(10, 0)
  memcache.set(key=util.RECENT_TESTS_MEMCACHE_KEY, value=recent_tests,
               time=util.STATS_MEMCACHE_TIMEOUT)
  return http.HttpResponse('Done')
