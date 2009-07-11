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

from google.appengine.api import datastore
from google.appengine.api import datastore_errors
from google.appengine.api import datastore_types
from google.appengine.api import memcache

from google.appengine.ext import db

from google_app_engine_ranklist import ranker

import user_agent
from user_agent import UserAgent

from settings import *


MAX_TEST_MSEC = 60000  # 1 minute

if BUILD == 'production':
  NUM_RANKERS = 100
else:
  NUM_RANKERS = 2


def GetRanker(name):
  key = datastore_types.Key.from_path('app', name)
  try:
    r = ranker.Ranker(datastore.Get(key)['ranker'])
    #if BUILD == 'development':
    #  logging.info('found ranker w/ name %s' % name)
    return r
  except datastore_errors.EntityNotFoundError:
    #if BUILD == 'development':
    #  logging.info('new ranker w/ %s rankers and name %s' % (NUM_RANKERS, name))
    r = ranker.Ranker.Create([0, MAX_TEST_MSEC], NUM_RANKERS)
    app = datastore.Entity('app', name=name)
    app['ranker'] = r.rootkey
    datastore.Put(app)
    return r


class ResultTime(db.Model):
  test = db.StringProperty()
  score = db.IntegerProperty()
  dirty = db.BooleanProperty(default=True)

  def increment_all_counts(self):
    parent = self.parent()
    for user_agent_string in parent.user_agent.get_string_list():
      guid = ResultParent.guid(
          parent.category, self.test, user_agent_string, parent.params)
      ResultParent.count_test_score(guid, parent.created, self.score)
      #logging.info('counting score for guid: %s' % guid)
    self.dirty = False
    self.put()


class ResultParent(db.Expando):
  """A parent entity for a run.

  Inherits from db.Expando instead of db.Model to allow the network_loader
  to add an attribute for 'loader_id'.
  TODO(slamm): use __getattribute to expando attributes to 'loader_id'
  """
  category = db.StringProperty()
  user_agent = db.ReferenceProperty(UserAgent)
  user_agent_list = db.StringListProperty()
  ip = db.StringProperty()
  user = db.UserProperty()
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


  def increment_all_counts(self):
    """This is not efficient enough to be used in prod."""
    logging.info('ResultParent.increment_all_counts: %s, ua: %s'
                 % (self.key(), self.user_agent.key()))
    result_times = ResultTime.all().ancestor(self)
    for result_time in result_times:
      #logging.info('ResultTime key is %s ' % (result_time.key()))
      #logging.info('w/ ua: %s' %  result_time.parent().user_agent)
      result_time.increment_all_counts()


  def invalidate_ua_memcache(self):
    memcache_ua_keys = []
    for user_agent in self.user_agent_list:
      memcache_ua_key = '%s_%s' % (self.category, user_agent)
      memcache_ua_keys.append(memcache_ua_key)
    #logging.info('invalidate_ua_memcache, memcache_ua_keys: %s' %
    #             memcache_ua_keys)
    memcache.delete_multi(keys=memcache_ua_keys, seconds=0,
                          namespace=STATS_MEMCACHE_UA_ROW_NS)


  @staticmethod
  def guid(category, test, user_agent_version, params=None):
    guid = category + '_' + test + '_' + user_agent_version
    if params:
      hash_params = hashlib.md5(','.join(params)).hexdigest()
      guid += '_' + hash_params
    return guid


  @staticmethod
  def get_ranker(guid):
    return GetRanker(guid)


  @staticmethod
  def count_test_score(guid, created, score):
    r = ResultParent.get_ranker(guid)
    # A ranker's score value keyname must start with a letter.
    #logging.debug('setting score %s for %s' % (score, guid))
    r.SetScore('n_' + str(created), [score])


  @staticmethod
  def get_total(guid):
    r = ResultParent.get_ranker(guid)
    return r.TotalRankedScores()

  @staticmethod
  def get_median(guid, return_total=False, total=None):
    r = ResultParent.get_ranker(guid)
    if not total:
      total = r.TotalRankedScores()
    median_offset = int(round(total/2))
    try:
      median = r.FindScore(median_offset)[0][0]
    except:
      median = None

    if return_total:
      return (median, total)
    else :
      return median
