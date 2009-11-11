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
import base

class ResultTime(db.Model):
  test = db.StringProperty()
  score = db.IntegerProperty()
  dirty = db.BooleanProperty(default=True)

  def increment_all_counts(self):
    logging.info('ResultTime.increment_all_counts for test: %s, score: %s' %
                 (self.test, self.score))
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
      params_str = parent.params_str or None
      for user_agent_string in parent.get_user_agent_list():
        yield test.GetOrCreateRanker(user_agent_string, params_str)


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
  def GetMemcacheKey(cls, category, user_agent):
    memcache_ua_key = '%s_%s' % (category, user_agent)
    if category in settings.CATEGORIES_BETA:
      memcache_ua_key += '_beta'
    return memcache_ua_key


  @classmethod
  def AddResult(cls, test_set, ip, user_agent_string, results_str,
                is_import=False, params_str=None, js_user_agent_string=None,
                **kwds):
    """Create result models and stores them as one transaction.

    Args:
      test_set: an instance of test_set_base.
      ip: a string to store as the user's IP. This should be hashed beforehand.
      user_agent_string: the http user agent string.
      results_str: a string like 'test1=time1,test2=time2,[...]'.
      js_user_agent_string: chrome frame ua string from client-side JavaScript.
      kwds: optional fields including 'loader_id'.
    Returns:
      A ResultParent instance.
    """
    logging.debug('ResultParent.AddResult')
    if params_str in ('None', ''):
      # params_str should either unset, None, or a non-empty string
      raise ValueError

    user_agent = UserAgent.factory(user_agent_string,
                                   js_user_agent_string=js_user_agent_string)
    parent = cls(category=test_set.category,
                 ip=ip,
                 user_agent=user_agent,
                 params_str=params_str, **kwds)
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
    memcache_ua_keys = [ResultParent.GetMemcacheKey(self.category, user_agent)
                        for user_agent in self.get_user_agent_list()]
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

  def get_user_agent_list(self):
    """Get user_agent string list."""
    return self.user_agent.get_string_list()

  def get_score_and_display(self):
    """Gets a row score for this ResultParent data set from the test_set.
    """
    # look in memcache first
    memcache_key = str(self.key())
    score_ns = 'SCORE_DISPLAY'

    score_display = memcache.get(memcache_key, score_ns)
    if score_display:
      row_score = score_display['score']
      row_display = score_display['display']
      logging.info('get_score_and_display memcache for score: %s, display: %s' %
                   (row_score, row_display))
    else:
      test_set = all_test_sets.GetTestSet(self.category)
      result_times = self.get_result_times()
      #logging.info('cat: %s, test_set: %s, %s' %
      #             (self.category, test_set, len(result_times)))

      results = {}
      medians = {}
      visible_tests = []
      for result_time in result_times:
        #logging.info('result_time.test: %s, .score: %s, key: %s' %
        #             (result_time.test, result_time.score, result_time.key()))
        medians[result_time.test] = result_time.score
        test = test_set.GetTest(result_time.test)
        if test is None:
          continue
        if not hasattr(test, 'is_hidden_stat') or not test.is_hidden_stat:
          visible_tests.append(test)

      for test in visible_tests:
        score, display = base.util.GetScoreAndDisplayValue(
            test, medians[test.key], medians)
        #logging.info('%s score %s, display: %s' % (test.key, score, display))
        results[test.key] = {
          'score': score,
          'median': medians[test.key],
          'display': display
        }
      row_score, row_display = test_set.GetRowScoreAndDisplayValue(results)
      #logging.info('get_score_and_display, row_score: %s, row_display: %s' %
      #             (row_score, row_display))
      score_display = {
        'score': row_score,
        'display': row_display
      }
      memcache.set(key=memcache_key, value=score_display, time=300,
          namespace=score_ns)
      logging.info('set memcache for key: %s, score: %s, display: %s' %
                   (memcache_key, score, display))

    return row_score, row_display
