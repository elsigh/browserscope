#!/usr/bin/python2.5
#
# Copyright 2008 Google Inc.
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

import logging
import sys

from google.appengine.ext import db
from google.appengine.api.labs import taskqueue

from categories import all_test_sets
from categories import test_set_base
from models import result_stats
from models.user_agent import UserAgent


class ResultTime(db.Model):
  test = db.StringProperty()
  score = db.IntegerProperty()
  dirty = db.BooleanProperty(default=True)

  def UpdateStats(self):
    logging.info('ResultTime.UpdateStats for test: %s, score: %s, dirty: %s' %
                 (self.test, self.score, self.dirty))
    if self.dirty:
      for ranker in self.GetOrCreateRankers():
        ranker.Add(self.score)
      self.dirty = False
      self.put()

  def GetOrCreateRankers(self):
    parent = self.parent()
    test_set = all_test_sets.GetTestSet(parent.category)
    test = test_set.GetTest(self.test)
    if test:
      params_str = parent.params_str or None
      return test.GetOrCreateRankers(parent.GetBrowsers(), params_str)
    else:
      logging.warn('Test key not found in test_set: %s', self.test)
      return []


class ResultParent(db.Expando):
  """A parent entity for a test run.

  Inherits from db.Expando instead of db.Model to allow the network_loader
  to add an attribute for 'loader_id'.
  """
  category = db.StringProperty()
  user_agent = db.ReferenceProperty(UserAgent)
  ip = db.StringProperty()
  user = db.UserProperty(auto_current_user_add=True)
  created = db.DateTimeProperty(auto_now_add=True)
  params_str = db.StringProperty(default=None)

  @classmethod
  def AddResult(cls, test_set, ip, user_agent_string, results_str,
                is_import=False, params_str=None,
                js_user_agent_string=None,
                js_document_mode=None,
                skip_dirty_update=False,
                **kwds):
    """Create result models and stores them as one transaction.

    Args:
      test_set: an instance of test_set_base.
      ip: a string to store as the user's IP. This should be hashed beforehand.
      user_agent_string: the http user agent string.
      results_str: a string like 'test1=time1,test2=time2,[...]'.
      is_import: if True, skip checking test_keys and do not mark dirty.
      params_str: a string representation of test_set_params.Params.
      js_user_agent_string: chrome frame ua string from client-side JavaScript.
      js_document_mode: js document.documentMode (e.g. '9' for IE 9 preview)
      skip_dirty_update: For tests, allow skipping the update-dirty task.
      kwds: optional fields including 'loader_id'.
    Returns:
      A ResultParent instance.
    """
    logging.debug('ResultParent.AddResult category=%s' % test_set.category)
    if params_str in ('None', ''):
      # params_str should either unset, None, or a non-empty string
      logging.debug('params_str is wonky')
      raise ValueError

    user_agent = UserAgent.factory(user_agent_string,
                                   js_user_agent_string=js_user_agent_string,
                                   js_document_mode=js_document_mode)
    parent = cls(category=test_set.category,
                 ip=ip,
                 user_agent=user_agent,
                 params_str=params_str, **kwds)
    try:
      results = test_set.GetResults(results_str, ignore_key_errors=is_import)
    except test_set_base.ParseResultsKeyError, e:
      logging.warn(e)
      return None
    except test_set_base.ParseResultsValueError:
      logging.warn('Results string with bad value(s): %s', results_str)
      return None

    for test_key, values in results.items():
      if 'expando' in values:
        # test_set.GetResults may add 'expando' value; save it on the parent.
        parent.__setattr__(test_key, values['expando'])

    def _AddResultInTransaction():
      parent.put()
      result_times = [ResultTime(parent=parent,
                                 test=test_key,
                                 score=values['raw_score'],
                                 dirty=not is_import)
                      for test_key, values in results.items()]
      db.put(result_times)
      return result_times
    result_times = db.run_in_transaction(_AddResultInTransaction)
    if not skip_dirty_update:
      cls.ScheduleUpdateDirty(result_times[0].key(), parent.category)
    return parent

  @classmethod
  def ScheduleUpdateDirty(cls, result_time_key, category=None):
    """Schedule UpdateStats for a given ResultTime.

    This gets handled by base.manage_dirty.UpdateDirty which
    then calls ResultTime.UpdateStats().

    Args:
      result_time_key: a dirty ResultTime key
      category: the category string
    """
    if not category:
      category = cls.get(result_time_key.parent()).category
    task = taskqueue.Task(
        method='GET', url='/admin/update_dirty/%s' % category,
        name='update-dirty-%s' % str(result_time_key).replace('_', '-'),
        params={'result_time_key': result_time_key, 'category': category})
    try:
      task.add(queue_name='update-dirty')
    except taskqueue.InvalidTaskError:
      logging.info('Cannot add task: %s:%s' % (sys.exc_type, sys.exc_value))
      return False
    return True

  def UpdateStatsNonProduction(self):
    """This is not efficient enough to be used in prod."""
    result_times = self.GetResultTimes()
    for result_time in result_times:
      result_time.UpdateStats()
    result_stats.UpdateCategory(self.category, self.user_agent)

  def ResultTimesQuery(self):
    return ResultTime.all().ancestor(self)

  def GetResultTimes(self):
    return self.ResultTimesQuery().fetch(1000)

  def GetResults(self):
    """Return a dict of scores indexed by test key names."""
    return dict((x.test, x.score) for x in self.GetResultTimes())

  def GetBrowsers(self):
    """Get browser list (e.g. ['Firefox', 'Firefox 3', 'Firefox 3.5])."""
    return self.user_agent.get_string_list()
