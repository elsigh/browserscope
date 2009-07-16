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

import hashlib
import logging
import sys

from google.appengine.ext import db

from controllers import all_test_sets
from models import user_agent
from models import result_ranker
from models.user_agent import UserAgent

from settings import *


class ResultTime(db.Model):
  test = db.StringProperty()
  score = db.IntegerProperty()
  dirty = db.BooleanProperty(default=True)

  def increment_all_counts(self):
    for ranker in self.GetRankers():
      ranker.Add(self.score)
    self.dirty = False
    self.put()

  def GetRankers(self):
    parent = self.parent()
    test = all_test_sets.GetTestSet(parent.category).GetTest(self.test)
    for user_agent_string in parent.user_agent.get_string_list():
      yield result_ranker.Factory(
          parent.category, test, user_agent_string, parent.params)


class ResultParent(db.Expando):
  """A parent entity for a run.

  Inherits from db.Expando instead of db.Model to allow the network_loader
  to add an attribute for 'loader_id'.
  TODO(slamm): use __getattribute to expando attributes to 'loader_id'
  """
  category = db.StringProperty()
  user_agent = db.ReferenceProperty(UserAgent)
  user_agent_pretty = db.StringProperty()
  user_agent_list = db.StringListProperty()
  ip = db.StringProperty()
  # TODO(elsigh) remove user in favor of user_id
  user = db.UserProperty()
  user_id = db.StringProperty()
  created = db.DateTimeProperty(auto_now_add=True)
  params = db.StringListProperty(default=[])

  @classmethod
  def AddResult(cls, category, ip, user_agent_string, test_scores, **kwds):
    """Create result models and stores them as one transaction."""
    user_agent = UserAgent.factory(user_agent_string)
    parent = cls(category=category,
                 ip=ip,
                 user_agent=user_agent,
                 user_agent_list=user_agent.get_string_list(),
                 **kwds)
    def _AddResultInTransaction():
      parent.put()
      db.put([ResultTime(parent=parent, test=str(test), score=int(score))
              for test, score in test_scores])
    db.run_in_transaction(_AddResultInTransaction)
    return parent

  def invalidate_ua_memcache(self):
    memcache_ua_keys = ['%s_%s' % (self.category, user_agent)
                        for user_agent in self.user_agent_list]
    #logging.info('invalidate_ua_memcache, memcache_ua_keys: %s' %
    #             memcache_ua_keys)
    memcache.delete_multi(keys=memcache_ua_keys, seconds=0,
                          namespace=STATS_MEMCACHE_UA_ROW_NS)

  def increment_all_counts(self):
    """This is not efficient enough to be used in prod."""
    logging.info('ResultParent.increment_all_counts: %s, ua: %s'
                 % (self.key(), self.user_agent.key()))
    result_times = ResultTime.all().ancestor(self)
    for result_time in result_times:
      #logging.info('ResultTime key is %s ' % (result_time.key()))
      #logging.info('w/ ua: %s' %  result_time.parent().user_agent)
      result_time.increment_all_counts()
