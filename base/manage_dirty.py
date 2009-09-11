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

"""Manage dirty ResultTime's."""

__author__ = 'slamm@google.com (Stephen Lamm)'

import logging
import time
import traceback

from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.api.labs import taskqueue
from google.appengine import runtime

import django
from django import http

from models.result import ResultParent
from models.result import ResultTime

from base import decorators

import settings


UPDATE_DIRTY_DONE = 'No more dirty ResultTimes.'
_UPDATE_DIRTY_FETCH_LIMIT = 100


class UpdateDirtyController(db.Model):
  NAMESPACE = 'cron_update_dirty'
  LOCK_TIMEOUT_SECONDS = 33

  is_paused = db.BooleanProperty(default=False)

  @classmethod
  def SetPaused(cls, is_paused):
    cls(key_name=cls.NAMESPACE, is_paused=is_paused).put()
    memcache.set(key='paused', value=is_paused, namespace=cls.NAMESPACE)
    if is_paused:
      # Allow pending changes to finish
      while memcache.get(key='lock', namespace=cls.NAMESPACE):
        time.sleep(1)


  @classmethod
  def IsPaused(cls):
    is_paused = memcache.get(key='paused', namespace=cls.NAMESPACE)
    logging.info('UpdateDirtyController is_paused: %s' % is_paused)
    if is_paused is None:
      is_paused = cls.get_or_insert(
          key_name=cls.NAMESPACE, is_paused=False).is_paused
      memcache.set(key='paused', value=is_paused, namespace=cls.NAMESPACE)
    logging.info('UpdateDirtyController returning is_paused: %s' % is_paused)
    return is_paused

  @classmethod
  def AcquireLock(cls):
    """Attempt to acquire a lock for UpdateDirty.

    Returns:
       True if lock acquired; otherwise, False.
    """
    return memcache.add(key='lock', value=1, time=cls.LOCK_TIMEOUT_SECONDS,
                        namespace=cls.NAMESPACE)

  @classmethod
  def ReleaseLock(cls):
    """Release UpdateDirty lock."""
    memcache.delete(key='lock', namespace=cls.NAMESPACE)


def GetDirtyResultTimeQuery(ancestor=None):
  """Return a query for ResultTime's with dirty=True.

  Args:
    ancestor: a ResultParent instance or Key instance
  Returns:
    a Query instance
  """
  query = ResultTime.all().filter('dirty =', True)
  if ancestor:
    query.ancestor(ancestor)
  return query


def _GetNextDirty():
  result_parent_key = None
  dirty_result_time = GetDirtyResultTimeQuery().get()
  if dirty_result_time:
    result_parent_key = dirty_result_time.parent_key()
  return result_parent_key


def _GetDirtySiblings(encoded_result_parent_key):
  dirty_siblings = None
  if encoded_result_parent_key:
    result_parent_key = db.Key(encoded_result_parent_key)
    dirty_query = GetDirtyResultTimeQuery(result_parent_key)
    dirty_siblings = dirty_query.fetch(_UPDATE_DIRTY_FETCH_LIMIT)
  else:
    result_parent_key = _GetNextDirty()
    if result_parent_key:
      dirty_siblings = GetDirtyResultTimeQuery(result_parent_key)
  return dirty_siblings


def UpdateDirty(request):
  """Updates any dirty tests, adding its score to the appropriate ranker."""
  if UpdateDirtyController.IsPaused():
    return http.HttpResponse('UpdateDirty is paused.')
  if not UpdateDirtyController.AcquireLock():
    return http.HttpResponse('UpdateDirty: unable to acquire lock.')
  try:
    num_completed = 0
    try:
      dirty_siblings = _GetDirtySiblings(request.GET.get('result_parent_key'))
      if dirty_siblings:
        result_parent = dirty_siblings[0].parent()
        # Mark non-live test categories as not-dirty, don't rank their scores.
        if (result_parent.category not in settings.CATEGORIES and
            settings.BUILD == 'production'):
          for result_time in dirty_siblings:
            result_time.dirty = False
          db.put(dirty_siblings)
        else:
          for result_time in dirty_siblings:
            # Count the times and mark them !dirty.
            result_time.increment_all_counts()
            num_completed += 1
          result_parent.invalidate_ua_memcache()
    except runtime.DeadlineExceededError:
      logging.warn('UpdateDirty DeadlineExceededError; '
                   'number of increment_all_counts completed=%s', num_completed)
    next_result_parent_key = _GetNextDirty()
    if next_result_parent_key:
      ScheduleDirtyUpdate(next_result_parent_key)
      return http.HttpResponse('UpdateDirty: added task to update more.')
    else:
      return http.HttpResponse(UPDATE_DIRTY_DONE)
  except:
    return http.HttpResponse('UpdateDirty: bailed: %s' % traceback.format_exc())
  finally:
    UpdateDirtyController.ReleaseLock()


@decorators.admin_required
def UnPauseUpdateDirty(request):
  paused_was = UpdateDirtyController.IsPaused()
  UpdateDirtyController.SetPaused(False)
  paused_is = UpdateDirtyController.IsPaused()
  return http.HttpResponse('UnPauseUpdateDirty Done. Was: %s, Is: %s' %
                           (paused_was, paused_is))


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


def ScheduleDirtyUpdate(result_parent_instance_or_key=None):
  logging.info('ScheduleDirtyUpdate result_parent_instance_or_key:%s'
               % result_parent_instance_or_key)
  if UpdateDirtyController.IsPaused():
    # The update will happen when UpdateDirty is unpaused.
    logging.info('ScheduleDirtyUpdate: UpdateDirtyController.IsPaused')
    return
  try:
    result_parent_key = result_parent_instance_or_key
    if hasattr(result_parent_instance_or_key, 'key'):
      result_parent_key = result_parent_instance_or_key.key()
    logging.info('ScheduleDirtyUpdate result_parent_key: %s' %
                 result_parent_key)
    if not result_parent_key:
      result_parent_key = _GetNextDirty()
    if result_parent_key:
      task = taskqueue.Task(
          method='GET', params={'result_parent_key': result_parent_key}).add(queue_name='update-dirty')
      logging.info('Added update-dirty task for result_parent_key: %s' %
                   result_parent_key)
    else:
      logging.info('No dirty result times to schedule.')
  except:
    logging.warn('Unable to add update-dirty task: %s' % traceback.format_exc())
