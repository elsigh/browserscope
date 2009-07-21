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

__author__ = 'slamm@google.com (Stephen Lamm)'

import hashlib
import logging

from google.appengine.api import datastore
from google.appengine.api import datastore_errors
from google.appengine.api import datastore_types
from google.appengine.api import memcache
from google.appengine.ext import db

from models import result_ranker_storage

# Two alternative rankers here
import score_ranker
from third_party.google_app_engine_ranklist import ranker


class ResultRankerParent(db.Model):
  MEMCACHE_NAMESPACE = 'result_ranker_parent'
  PARAMS_SEPARATOR = '&'

  category = db.StringProperty()
  test_key = db.StringProperty()
  user_agent_version = db.StringProperty()
  params_str = db.StringProperty()
  min_value = db.IntegerProperty()
  max_value = db.IntegerProperty()
  branching_factor = db.IntegerProperty()

  @staticmethod
  def KeyName(category, test_key, user_agent_version, params_str):
    if params_str:
      params_hash = hashlib.md5(params_str).hexdigest()
      return '_'.join((category, test_key, user_agent_version, params_hash))
    else:
      return '_'.join((category, test_key, user_agent_version))

  @classmethod
  def factory(cls, category, test, user_agent_version, params):
    params_str = ''
    if params:
      params_str = cls.PARAMS_SEPARATOR.join(sorted(params))
    key_name = cls.KeyName(category, test.key, user_agent_version, params_str)
    result_ranker_parent = memcache.get(key=key_name,
                                        namespace=cls.MEMCACHE_NAMESPACE)
    if not result_ranker_parent:
      result_ranker_parent = cls.get_or_insert(
          key_name,
          category=category,
          test_key=test.key,
          user_agent_version=user_agent_version,
          params_str=params_str,
          min_value=test.min_value,
          max_value=test.max_value,
          branching_factor=score_ranker.GetShallowBranchingFactor(
              test.min_value, test.max_value))
      memcache.set(key=key_name, namespace=cls.MEMCACHE_NAMESPACE,
                   value=result_ranker_parent)
    return result_ranker_parent

  def delete(self):
    """Remove this from storage."""
    memcache.delete(key=self.key().name(), namespace=self.MEMCACHE_NAMESPACE)
    db.Model.delete(self)


class MedianRanker(score_ranker.Ranker):

  def GetMedian(self, num_scores=None):
    return self.GetMedianAndNumScores(num_scores)[0]

  def GetMedianAndNumScores(self, num_scores=None):
    median = None
    if num_scores is None:
      num_scores = self.TotalRankedScores()
    if num_scores:
      median_index = int(num_scores) / 2
      try:
        median = self.FindScore(median_index)
      # TODO: Give exact exceptions to catch
      except Exception, e:
        logging.warn('Exception, %s, from FindScore(rank=%s)',
                     str(e), median_index)
    return median, num_scores


class ResultRanker(MedianRanker):

  def __init__(self, category, test, user_agent_version, params=None):
    """Return an existing or new ranker.

    Args:
      category: a test category string (e.g. 'network' or 'reflow')
      test: a test instance (e.g. NetworkTest or ReflowTest)
      user_agent_version: browser name and version (e.g. 'Safari 4.0' or 'IE 8')
      params: addional parameters to add to the key
    Returns:
      a Ranker instance
    """
    self.ranker_parent = ResultRankerParent.factory(
        category, test, user_agent_version, params)
    self.storage = result_ranker_storage.ScoreDatastore(
        self.ranker_parent.key())
    score_ranker.Ranker.__init__(
        self,
        self.storage,
        self.ranker_parent.min_value,
        self.ranker_parent.max_value,
        self.ranker_parent.branching_factor)

  def Delete(self):
    """Remove the ranker."""
    self.storage.DeleteAll()
    self.ranker_parent.delete()


class RankListRanker(MedianRanker):
  MAX_TEST_MSEC = 60000
  BRANCHING_FACTOR = 100

  def __init__(self, category, test, user_agent_version, params=None):
    key_name = self.KeyName(category, test.key, user_agent_version, params)
    self.key = datastore_types.Key.from_path('app', key_name)
    try:
      self.ranker = ranker.Ranker(datastore.Get(self.key)['ranker'])
    except datastore_errors.EntityNotFoundError:
      self.ranker = ranker.Ranker.Create(
          [0, self.MAX_TEST_MSEC], self.BRANCHING_FACTOR)
      app = datastore.Entity('app', name=key_name)
      app['ranker'] = self.ranker.rootkey
      datastore.Put(app)

  @staticmethod
  def KeyName(category, test_key, user_agent_version, params=None):
    if params:
      params_str = hashlib.md5(','.join(params)).hexdigest()
      return '_'.join((category, test_key, user_agent_version, params_str))
    else:
      return '_'.join((category, test_key, user_agent_version))

  def Add(self, score):
    self.Update([score])

  def Update(self, scores):
    # The old code used 'created' as part of the score key.
    # That had the problem where if two tests had the same created time,
    # only one would get counted. This version is not much better.
    import datetime
    now = str(datetime.datetime.now())
    user_scores = dict(("n_%s_%s" % (now, i), [score])
                       for i, score in enumerate(scores))
    self.ranker.SetScores(user_scores)

  def FindScore(self, rank):
    return self.ranker.FindScore(rank)[0][0]

  def TotalRankedScores(self):
    return self.ranker.TotalRankedScores()

  def _delete_entity(self, name):
    query = datastore.Query(name, keys_only=True)
    query.Ancestor(self.ranker.rootkey)
    while 1:
      results = list(query.Run())
      db.delete(results)
      if len(results) < 1000:
        break

  def Delete(self):
    """Remove the ranker."""
    self._delete_entity('ranker_node')
    self._delete_entity('ranker_score')
    db.delete([self.ranker.rootkey, self.key])

def Factory(category, test, user_agent_version, params=None):
  #return ResultRanker(category, test, user_agent_version, params)
  return RankListRanker(category, test, user_agent_version, params)
