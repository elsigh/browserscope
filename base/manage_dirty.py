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

"""Manage dirty ResultTime's."""

__author__ = 'slamm@google.com (Stephen Lamm)'

import datetime
import logging
import random
import sys
import time
import traceback

from google.appengine.api import memcache
from google.appengine.api.labs import taskqueue
from google.appengine.ext import db
from google.appengine import runtime

import django
from django import http

from models.result import ResultParent
from models.result import ResultTime

from base import decorators

import settings

from django.template import add_to_builtins
add_to_builtins('base.custom_filters')


def ScheduleCategoryUpdate(result_parent_key):
  """Add a task to update a category's statistics.

  The task is handled by base.admin.UpdateCategory which then
  calls UpdateCategory below.
  """
  # Give the task a name to ensure only one task for each ResultParent.
  result_parent = ResultParent.get(result_parent_key)
  category = result_parent.category
  name = 'categoryupdate-%s' % str(result_parent_key).replace('_', '-under-')
  url = '/_ah/queue/update-category/%s/%s' % (category, result_parent_key)

  task = taskqueue.Task(url=url, name=name, params={
      'category': category,
      'user_agent_key': result_parent.user_agent.key(),
      })
  attempt = 0
  while attempt < 3:
    try:
      task.add(queue_name='update-category')
      break
    except:
      attempt += 1
      logging.info('Cannot add task(attempt %s): %s:%s' %
                   (attempt, sys.exc_type, sys.exc_value))


def UpdateDirty(request):
  """Updates any dirty tests, adding its score to the appropriate ranker."""
  logging.debug('UpdateDirty start.')

  task_name_prefix = request.REQUEST.get('task_name_prefix', '')
  result_time_key = request.REQUEST.get('result_time_key')
  category = request.REQUEST.get('category')
  count = int(request.REQUEST.get('count', 0))
  if result_time_key:
    result_time = ResultTime.get(result_time_key)
    try:
      ResultTime.UpdateStats(result_time)
    except:
      logging.info('UpdateStats: %s:%s' % (sys.exc_type, sys.exc_value))
    result_parent_key = result_time.parent_key()
  else:
    result_parent_key = request.REQUEST.get('result_parent_key')
    if result_parent_key:
      result_parent_key = db.Key(result_parent_key)
    else:
      UpdateOldDirty()
      return http.HttpResponse('Done scheduling old results.')

  # Create a task for the next dirty ResultTime to update.
  dirty_query = ResultTime.all(keys_only=True)
  dirty_query.filter('dirty =', True)
  dirty_query.ancestor(result_parent_key)
  next_result_time_key = dirty_query.get()
  if next_result_time_key:
    logging.debug('Schedule next ResultTime: %s', next_result_time_key)
    ResultParent.ScheduleUpdateDirty(
        next_result_time_key, category, count+1, task_name_prefix)
  else:
    logging.debug('Done with result_parent: %s', result_parent_key)
    ScheduleCategoryUpdate(result_parent_key)
  return http.HttpResponse('Done.')


MAX_RESULT_TIMES = 500
MAX_SCHEDULED = 8
OLD_SECONDS = 5 * 60  # code assumes this is less than one day
def UpdateOldDirty():
  """Update dirty queries from the past."""
  num_scheduled = 0
  seen_result_parent_keys = set()
  dirty_query = ResultTime.all(keys_only=True).filter('dirty =', True)
  for i, result_time_key in enumerate(dirty_query.fetch(500)):
    result_parent_key = result_time_key.parent()
    if result_parent_key not in seen_result_parent_keys:
      seen_result_parent_keys.add(result_parent_key)
      result_parent = ResultParent.get(result_parent_key)
      category = result_parent.category
      age = datetime.datetime.now() - result_parent.created
      if age.days > 0 or age.seconds > OLD_SECONDS:
        logging.info(
            'Schedule old dirty:%d:%d: %s, age=%s, result_parent=%s, result_time=%s',
            i, num_scheduled, category, age, result_parent_key, result_time_key)
        if ResultParent.ScheduleUpdateDirty(
            result_time_key, category, count=-1):
          num_scheduled += 1
          if num_scheduled == 10:
            break

def MakeDirty(request):
  """For testing purposes, make some tests dirty."""
  query = ResultParent.all()
  result_times = []
  for result_parent in query.fetch(10):
    for result_time in ResultTime.all().ancestor(result_parent).fetch(1000):
      result_time.dirty = True
      result_times.append(result_time)
  db.put(result_times)
  return http.HttpResponse('Made %s result_times dirty' % len(result_times))
