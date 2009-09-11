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


RANKER_VERSIONS = ['previous', 'current', 'next']
DEFAULT_RANKER_VERSION = 'current'


class Error(Exception):
  """Base exception class for result_ranker module."""
  pass

class ReleaseError(Error):
  """Raised when a release fails."""
  pass


def _CheckParamsStr(params_str):
  """Check that params_str is a reasonable value.

  Raises:
    ValueError if params_str is a 'None' string or an empty string.
    (A None value is okay.)
  """
  if params_str in ('None', ''):
    raise ValueError

class ResultRankerGrandparent(db.Model):
  """Collect together ResultRankerParent's that represent the same data slice.

  This allows us to do things such as rebuilding a ranker.
  """
  category = db.StringProperty()
  test_key = db.StringProperty()
  user_agent_version = db.StringProperty()
  params_str = db.StringProperty(default=None)

  @classmethod
  def KeyName(cls, category, test_key, user_agent_version, params_str):
    if params_str:
      params_hash = hashlib.md5(params_str).hexdigest()
      return '_'.join((category, test_key, user_agent_version, params_hash))
    else:
      return '_'.join((category, test_key, user_agent_version))

  @classmethod
  def Get(cls, category, test_key, user_agent_version, params_str):
    _CheckParamsStr(params_str)
    return cls.get_by_key_name(cls.KeyName(
        category, test_key, user_agent_version, params_str))

  @classmethod
  def GetOrCreate(cls, category, test_key, user_agent_version, params_str):
    _CheckParamsStr(params_str)
    return cls.get_or_insert(
        cls.KeyName(category, test_key, user_agent_version, params_str),
        category=category,
        test_key=test_key,
        user_agent_version=user_agent_version,
        params_str=params_str)


class ResultRankerParent(db.Model):
  """ResultRankerParent is the parent to all the ranker nodes."""
  MEMCACHE_NAMESPACE = 'result_ranker_parent'

  ranker_version = db.StringProperty(
      required=True,
      choices=set(RANKER_VERSIONS),
      default=DEFAULT_RANKER_VERSION)
  min_value = db.IntegerProperty()
  max_value = db.IntegerProperty()
  branching_factor = db.IntegerProperty()

  @classmethod
  def MemcacheParams(cls, ranker_version, grandparent_key_name):
    key = '%s_%s' % (ranker_version, grandparent_key_name)
    return {'key': key, 'namespace': cls.MEMCACHE_NAMESPACE}

  @classmethod
  def Get(cls, category, test, user_agent_version, params_str,
          ranker_version=DEFAULT_RANKER_VERSION):
    _CheckParamsStr(params_str)
    grandparent_key_name = ResultRankerGrandparent.KeyName(
        category, test.key, user_agent_version, params_str)
    memcache_params = cls.MemcacheParams(ranker_version, grandparent_key_name)
    result_ranker_parent = memcache.get(**memcache_params)
    if not result_ranker_parent:
      grandparent = ResultRankerGrandparent.Get(
          category, test.key, user_agent_version, params_str)
      if grandparent:
        query = ResultRankerParent.all()
        query.ancestor(grandparent)
        query.filter('ranker_version =', ranker_version)
        result_ranker_parent = query.get()
        if result_ranker_parent:
          memcache.add(value=result_ranker_parent, **memcache_params)
    return result_ranker_parent

  @classmethod
  def GetOrCreate(cls, category, test, user_agent_version, params_str,
                  ranker_version=DEFAULT_RANKER_VERSION):
    _CheckParamsStr(params_str)
    grandparent_key_name = ResultRankerGrandparent.KeyName(
        category, test.key, user_agent_version, params_str)
    memcache_params = cls.MemcacheParams(ranker_version, grandparent_key_name)
    result_ranker_parent = memcache.get(**memcache_params)
    if not result_ranker_parent:
      grandparent = ResultRankerGrandparent.GetOrCreate(
          category, test.key, user_agent_version, params_str)
      query = ResultRankerParent.all()
      query.ancestor(grandparent)
      query.filter('ranker_version =', ranker_version)
      result_ranker_parent = query.get()
      is_newly_created = False
      if not result_ranker_parent:
        is_newly_created = True
        result_ranker_parent = cls(
            parent=grandparent,
            ranker_version=ranker_version,
            min_value=test.min_value,
            max_value=test.max_value,
            branching_factor=score_ranker.GetShallowBranchingFactor(
                test.min_value, test.max_value))
        result_ranker_parent.put()
      if not memcache.add(value=result_ranker_parent, **memcache_params):
        if is_newly_created:
          # Another process created the parent first. Use that instead.
          result_ranker_parent.delete()
        result_ranker_parent = memcache.get(**memcache_params)
    return result_ranker_parent

  def Release(self):
    if self.ranker_version != 'next':
      raise ReleaseError('Release(): ranker_version must be "next". (was %s)'
                         % self.ranker_version)
    update_parents = {}
    grandparent_key = self.parent_key()
    query = self.all()
    query.ancestor(grandparent_key)
    for parent in query.fetch(3):
      if parent.ranker_version == 'previous':
        db.delete(parent)
      elif parent.ranker_version == 'current':
        parent.ranker_version = 'previous'
        update_parents['previous'] = parent
    self.ranker_version = 'current'
    update_parents['current'] = self
    logging.info('Release: update_parents=%s', update_parents)
    for ranker_version in RANKER_VERSIONS:
      memcache_params = self.MemcacheParams(
          ranker_version, grandparent_key.name())
      if ranker_version in update_parents:
        memcache.set(value=update_parents[ranker_version], **memcache_params)
      else:
        memcache.delete(**memcache_params)
    db.run_in_transaction(db.put, update_parents.values())


  def delete(self):
    grandparent_key = self.parent_key()
    memcache_params = self.MemcacheParams(
        self.ranker_version, grandparent_key.name())
    memcache.delete(**memcache_params)
    db.Model.delete(self)
    query = self.__class__.all().ancestor(grandparent_key)
    if query.count() == 0:
      db.delete(grandparent_key)


class MedianRanker(object):
  """Mix-in class to compute median."""

  def TotalRankedScores(self):
    raise NotImplementedError

  def FindScore(self, rank):
    raise NotImplementedError

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


class ResultRanker(score_ranker.Ranker, MedianRanker):

  def __init__(self, ranker_parent):
    """Initialize a ResultRanker.

    Args:
      ranker_parent: a ResultRankerParent instance.
    """
    self.ranker_parent = ranker_parent
    self.storage = result_ranker_storage.ScoreDatastore(
        self.ranker_parent.key())
    score_ranker.Ranker.__init__(
        self,
        self.storage,
        self.ranker_parent.min_value,
        self.ranker_parent.max_value,
        self.ranker_parent.branching_factor)

  @classmethod
  def Get(
      cls, category, test, user_agent_version, params_str=None,
      ranker_version=DEFAULT_RANKER_VERSION, is_created_if_needed=False):
    _CheckParamsStr(params_str)
    ranker_parent = ResultRankerParent.Get(
        category, test, user_agent_version, params_str, ranker_version)
    if ranker_parent:
      return cls(ranker_parent)
    else:
      return None

  @classmethod
  def GetOrCreate(
      cls, category, test, user_agent_version, params_str=None,
      ranker_version=DEFAULT_RANKER_VERSION):
    """Return an existing or new ranker.

    Args:
      category: a test category string (e.g. 'network' or 'reflow')
      test: a test instance (e.g. NetworkTest or ReflowTest)
      user_agent_version: browser name and version (e.g. 'Safari 4.0' or 'IE 8')
      params_str: a string representing parameters to add to the key
      ranker_version: either 'previous', 'current', or 'next'
    Returns:
      a Ranker instance
    """
    _CheckParamsStr(params_str)
    ranker_parent = ResultRankerParent.GetOrCreate(
        category, test, user_agent_version, params_str, ranker_version)
    return cls(ranker_parent)

  def Delete(self):
    """Remove the ranker."""
    self.Reset()
    self.ranker_parent.delete()

  def Reset(self):
    """Remove the ranker."""
    self.storage.DeleteAll()


class RankListRanker(MedianRanker):
  MAX_TEST_MSEC = 60000
  BRANCHING_FACTOR = 100

  def __init__(self, category, test, user_agent_version, params_str=None):
    key_name = self.KeyName(category, test.key, user_agent_version, params_str)
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
  def KeyName(category, test_key, user_agent_version, params_str=None):
    if params_str:
      params_hash = hashlib.md5(params_str).hexdigest()
      return '_'.join((category, test_key, user_agent_version, params_hash))
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


def _UseRankListRanker():
  use_ranklist_ranker = False
  try:
    datastore.Get(datastore_types.Key.from_path('ranker migration', 'complete'))
  except datastore_errors.EntityNotFoundError:
    use_ranklist_ranker = True
  return use_ranklist_ranker


def GetRanker(category, test, user_agent_version, params_str=None,
              ranker_version=DEFAULT_RANKER_VERSION):
  """Get a ranker that matches the given args.

  Args:
    category: a category string like 'network' or 'reflow'.
    test: an instance of a test_set_base.TestBase derived class.
    user_agent_version: a string like 'Firefox 3' or 'Chrome 2.0.156'.
    params_str: a string representation of test_set_params.Params.
  Returns:
    an instance of a MedianRanker derived class (None if not found).
  """
  _CheckParamsStr(params_str)
  if _UseRankListRanker():
    # ranklist will create if needed. It is going away soon, so no fix needed.
    return RankListRanker(category, test, user_agent_version, params_str)
  else:
    return ResultRanker.Get(
        category, test, user_agent_version, params_str, ranker_version)


def GetOrCreateRanker(category, test, user_agent_version, params_str=None,
                      ranker_version=DEFAULT_RANKER_VERSION):
  """Get or create a ranker that matches the given args.

  Args:
    category: a category string like 'network' or 'reflow'.
    test: an instance of a test_set_base.TestBase derived class.
    user_agent_version: a string like 'Firefox 3' or 'Chrome 2.0.156'.
    params_str: a string representation of test_set_params.Params.
  Returns:
    an instance of a MedianRanker derived class (None if not found).
  """
  _CheckParamsStr(params_str)
  if _UseRankListRanker():
    return RankListRanker(category, test, user_agent_version, params_str)
  else:
    return ResultRanker.GetOrCreate(
        category, test, user_agent_version, params_str, ranker_version)
