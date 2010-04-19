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
import time
import traceback

from google.appengine.api import memcache
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

UPDATE_DIRTY_DONE = 'No more dirty ResultTimes.'
UPDATE_DIRTY_ADDED_TASK = 'Added task to update more dirty.'

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
    """Release UpdateDirty lock.
    The return value is 0 (DELETE_NETWORK_FAILURE) on network failure,
    1 (DELETE_ITEM_MISSING) if the server tried to delete the item but didn't
    have it, and 2 (DELETE_SUCCESSFUL) if the item was actually deleted. This
    can be used as a boolean value, where a network failure is the only bad
    condition.
    @see http://code.google.com/appengine/docs/python/memcache/functions.html
    """
    return memcache.delete(key='lock', namespace=cls.NAMESPACE)


class DirtyResultTimesQuery(object):
  """Iterate through dirty ResultTimes grouped by ResultParents."""

  RESULT_TIME_LIMIT = 20

  def __init__(self, encoded_result_parent_key=None):
    """Initialize a DirtyResultTimesQuery.

    Args:
      encoded_result_parent_key: a string encoded ResultParent key
    """
    self.result_parent_key = None
    if encoded_result_parent_key:
      self.result_parent_key = db.Key(encoded_result_parent_key)
    else:
      self.result_parent_key = self._GetResultParentKey()

  @classmethod
  def _GetQuery(cls, result_parent_key=None):
    """Return a query for ResultTime's with dirty=True.

    Args:
      result_parent_key: a ResultParent instance or Key instance
    Returns:
      a Query instance
    """
    query = ResultTime.all().filter('dirty =', True)
    if result_parent_key:
      query.ancestor(result_parent_key)
    return query

  @classmethod
  def _GetResultParentKey(cls):
    result_parent_key = None
    dirty_result_time = cls._GetQuery().get()
    if dirty_result_time:
      result_parent_key = dirty_result_time.parent_key()
    return result_parent_key

  def Fetch(self):
    dirty_result_times = []
    if self.result_parent_key:
      query = self._GetQuery(self.result_parent_key)
      dirty_result_times = query.fetch(self.RESULT_TIME_LIMIT + 1)
      if len(dirty_result_times) < self.RESULT_TIME_LIMIT + 1:
        self.result_parent_key = None
      else:
        dirty_result_times.pop()
      return dirty_result_times

  def IsResultParentDone(self):
    return self.result_parent_key is None

  def NextResultParentKey(self):
    if self.result_parent_key:
      return self.result_parent_key
    else:
      return self._GetResultParentKey()


def UpdateDirty(request):
  """Updates any dirty tests, adding its score to the appropriate ranker."""
  if UpdateDirtyController.IsPaused():
    return http.HttpResponse('UpdateDirty is paused.')
  if not UpdateDirtyController.AcquireLock():
    return http.HttpResponse('UpdateDirty: unable to acquire lock.')
  try:
    try:
      dirty_query = DirtyResultTimesQuery(request.GET.get('result_parent_key'))
      ResultParent.UpdateStatsFromDirty(dirty_query)
    except runtime.DeadlineExceededError:
      logging.warn('UpdateDirty DeadlineExceededError')
    next_result_parent_key = dirty_query.NextResultParentKey()
    if next_result_parent_key:
      ScheduleDirtyUpdate(next_result_parent_key)
      return http.HttpResponse(UPDATE_DIRTY_ADDED_TASK)
    else:
      return http.HttpResponse(UPDATE_DIRTY_DONE)
  finally:
    UpdateDirtyController.ReleaseLock()


@decorators.admin_required
def PauseUpdateDirty(request):
  paused_was = UpdateDirtyController.IsPaused()
  UpdateDirtyController.SetPaused(True)
  paused_is = UpdateDirtyController.IsPaused()
  return http.HttpResponse('PauseUpdateDirty Done. Was: %s, Is: %s' %
                           (paused_was, paused_is))

@decorators.admin_required
def UnPauseUpdateDirty(request):
  paused_was = UpdateDirtyController.IsPaused()
  UpdateDirtyController.SetPaused(False)
  paused_is = UpdateDirtyController.IsPaused()
  return http.HttpResponse('UnPauseUpdateDirty Done. Was: %s, Is: %s' %
                           (paused_was, paused_is))


@decorators.admin_required
def ReleaseLock(request):
  released = UpdateDirtyController.ReleaseLock()
  return http.HttpResponse('Released Lock with return: %s' % released)


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
  result_parent_key = result_parent_instance_or_key
  if hasattr(result_parent_instance_or_key, 'key'):
    result_parent_key = result_parent_instance_or_key.key()
  logging.info('ScheduleDirtyUpdate result_parent_key: %s' %
               result_parent_key)
  if not result_parent_key:
    result_parent_key = DirtyResultTimesQuery().NextResultParentKey()
  if result_parent_key:
    ResultParent.ScheduleDirtyUpdate(result_parent_key)
  else:
    logging.info('No dirty result times to schedule.')
