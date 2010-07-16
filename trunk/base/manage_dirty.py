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


# Maximum number of ResultTime's to query when picking the next one to update.
MAX_RESULT_TIMES = 100


def ScheduleCategoryUpdate(result_parent_key):
  """Add a task to update a category's statistics.

  The task is handled by base.admin.UpdateCategory which then
  calls UpdateCategory below.
  """
  # Give the task a name to ensure only one task for each ResultParent.
  name = 'category-update-%s' % result_parent_key.replace('_', '-')
  result_parent = ResultParent.get(result_parent_key)
  task = taskqueue.Task(method='GET', name=name, params={
      'category': result_parent.category,
      'user_agent_key': result_parent.user_agent.key(),
      })
  try:
    task.add(queue_name='update-category')
  except:
    logging.info('Cannot add task: %s:%s' % (sys.exc_type, sys.exc_value))


def UpdateDirty(request):
  """Updates any dirty tests, adding its score to the appropriate ranker."""
  logging.debug('UpdateDirty start.')

  result_time_key = request.REQUEST.get('result_time_key')
  category = request.REQUEST.get('category')
  if result_time_key:
    result_time = ResultTime.get(result_time_key)
    try:
      ResultTime.UpdateStats(result_time)
    except:
      logging.info('UpdateStats: %s:%s' % (sys.exc_type, sys.exc_value))
    result_parent_key = result_time.parent_key()
  else:
    result_parent_key = request.REQUEST.get('result_parent_key')

  # Create a task for the next dirty ResultTime to update.
  dirty_query = ResultTime.all(keys_only=True).filter('dirty =', True)
  if result_parent_key:
    if not hasattr(result_parent_key, 'id'):
      result_parent_key = db.Key(result_parent_key)
    dirty_query.ancestor(result_parent_key)
  elif category:
    # TODO: Filter ResultTime on category (would need to add it as a field)
    pass
  dirty_result_times = dirty_query.fetch(MAX_RESULT_TIMES)
  if dirty_result_times:
    next_result_time_key = random.choice(dirty_result_times)
    logging.debug('Schedule next ResultTime: %s', next_result_time_key)
    ResultParent.ScheduleUpdateDirty(next_result_time_key, category)
  elif result_parent_key:
    logging.debug('Done with result_parent: %s', result_parent_key)
    ScheduleCategoryUpdate(result_parent_key)
  return http.HttpResponse('Done.')


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
