#!/usr/bin/python2.4
#
# Copyright 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the 'License')
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import sys

from google.appengine.ext import db
from google.appengine.api import memcache

from categories import all_test_sets
from categories import test_set_base
from models import user_agent
from models.user_agent import UserAgent

import settings

class ResultTime(db.Model):
  test = db.StringProperty()
  score = db.IntegerProperty()
  dirty = db.BooleanProperty(default=True)

  def increment_all_counts(self):
    for ranker in self.GetOrCreateRankers():
      ranker.Add(self.score)
    self.dirty = False
    self.put()

  def GetOrCreateRankers(self):
    parent = self.parent()
    test_set = all_test_sets.GetTestSet(parent.category)
    try:
      test = test_set.GetTest(self.test)
    except KeyError:
      logging.warn('Test key not found in test_set: %s', self.test)
    else:
      params_str = None
      if parent.params_str:
        params_str = parent.params_str
      elif parent.params:
        # TODO(slamm): Remove after converting params -> params_str
        params_str = str(test_set_params.Params(
            [urllib.unquote(x) for x in parent.params]))
      for user_agent_string in parent.user_agent.get_string_list():
        yield test.GetOrCreateRanker(user_agent_string, params_str)


class ResultParent(db.Expando):
  """A parent entity for a test run.

  Inherits from db.Expando instead of db.Model to allow the network_loader
  to add an attribute for 'loader_id'.
  """
  category = db.StringProperty()
  user_agent = db.ReferenceProperty(UserAgent)
  user_agent_pretty = db.StringProperty()
  ip = db.StringProperty()
  # TODO(elsigh) remove user in favor of user_id
  user = db.UserProperty()
  user_id = db.StringProperty()
  created = db.DateTimeProperty(auto_now_add=True)
  params = db.StringListProperty(default=[])
  params_str = db.StringProperty(default=None)

  @classmethod
  def AddResult(cls, test_set, ip, user_agent_string, results_str,
                is_import=False, **kwds):
    """Create result models and stores them as one transaction.

    Args:
      test_set: an instance of test_set_base.
      ip: a string to store as the user's IP. This should be hashed beforehand.
      user_agent_string: The full user agent string.
      results_str: a string like 'test1=time1,test2=time2,[...]'.
      kwds: optional fields including 'user' and 'params_str'.
    Returns:
      A ResultParent instance.
    """
    logging.debug('ResultParent.AddResult')
    if kwds.get('params_str', None) in ('None', ''):
      # params_str should either unset, None, or a non-empty string
      raise ValueError

    user_agent = UserAgent.factory(user_agent_string)
    parent = cls(category=test_set.category,
                 ip=ip,
                 user_agent=user_agent,
                 user_agent_pretty=user_agent.pretty(),
                 **kwds)
    try:
      results = test_set.GetResults(results_str, is_import)
    except test_set_base.ParseResultsKeyError, e:
      logging.warn(e)
      return None
    except test_set_base.ParseResultsValueError:
      logging.warn('Results string with bad value(s): %s', results_str)
      return None

    for result in results:
      if 'expando' in result:
        # test_set.GetResults may add 'expando' value; save it on the parent.
        parent.__setattr__(result['key'], result['expando'])

    def _AddResultInTransaction():
      parent.put()
      for result in results:
        db.put(ResultTime(parent=parent,
                          test=result['key'],
                          score=result['score'],
                          dirty=not is_import))
    db.run_in_transaction(_AddResultInTransaction)
    return parent

  def invalidate_ua_memcache(self):
    memcache_ua_keys = ['%s_%s' % (self.category, user_agent)
                        for user_agent in self._get_user_agent_list()]
    #logging.debug('invalidate_ua_memcache, memcache_ua_keys: %s' %
    #             memcache_ua_keys)
    memcache.delete_multi(keys=memcache_ua_keys, seconds=0,
                          namespace=settings.STATS_MEMCACHE_UA_ROW_NS)

  def increment_all_counts(self):
    """This is not efficient enough to be used in prod."""
    result_times = self.get_result_times_as_query()
    for result_time in result_times:
      #logging.debug('ResultTime key is %s ' % (result_time.key()))
      #logging.debug('w/ ua: %s' %  result_time.parent().user_agent)
      result_time.increment_all_counts()

  def get_result_times_as_query(self):
    return ResultTime.all().ancestor(self)

  def get_result_times(self):
    """As long as a parent has less than 1000 result times,
       this will return them all.
    """
    return self.get_result_times_as_query().fetch(1000, 0)

  def _get_user_agent_list(self):
    """Build user_agent_list on-the-fly from user_agent_pretty.

    In the past, we stored user_agent_list.
    """
    return UserAgent.parse_to_string_list(self.user_agent_pretty)

  def get_score_and_display(self):
    """Gets a row score for this ResultParent data set from the test_set.
    """
    test_set = all_test_sets.GetTestSet(self.category)
    result_times = self.get_result_times()
    #logging.info('test_set: %s, %s' % (test_set, result_times))

    results = {}
    medians = {}
    for result_time in result_times:
      medians[result_time.test] = result_time.score
    for result_time in result_times:
      test = test_set.GetTest(result_time.test)
      if test is None:
        continue
      #logging.info('result_time: %s, score: %s, medians: %s' % (result_time, result_time.score, medians))
      score, display = test.GetScoreAndDisplayValue(result_time.score,
          medians)
      #logging.info('score: %s, display: %s' % (score, display))
      results[result_time.test] = {
        'score': score,
        'median': result_time.score,
        'display': display
      }
    row_score, row_display = test_set.GetRowScoreAndDisplayValue(results)
    #logging.info('row_score: %s, row_display: %s' % (row_score, row_display))
    return row_score, row_display


