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

import array
import bisect
import hashlib
import logging

from google.appengine.api import memcache
from google.appengine.ext import db

class RankerCacher(object):

  MEMCACHE_NAMESPACE = 'result_ranker'

  @classmethod
  def CachePut(cls, ranker):
    memcache.set(ranker.key().name(), ranker.ToString(),
                 namespace=cls.MEMCACHE_NAMESPACE)
    ranker.put()

  @classmethod
  def CacheGet(cls, key_names, ranker_classes):
    serialized_rankers = memcache.get_multi(
        key_names, namespace=cls.MEMCACHE_NAMESPACE)
    rankers = dict((k, ranker_classes[k].FromString(k, v))
                   for k, v in serialized_rankers.items())
    db_key_names = {}
    for key_name in key_names:
      if key_name not in rankers:
        db_key_names.setdefault(ranker_classes[key_name], []).append(key_name)
    if db_key_names:
      for ranker_class, key_names in db_key_names.items():
        for key_name, ranker in zip(
            key_names, ranker_class.get_by_key_name(key_names)):
          if ranker:
            rankers[key_name] = ranker
    return rankers


class CountRanker(db.Model):
  """Maintain a list of score counts.

  The minimum score is assumed to be 0.
  The maximum score must be MAX_SCORE or less.
  """
  MIN_SCORE = 0
  MAX_SCORE = 100

  counts = db.ListProperty(long, indexed=False)

  def GetMedianAndNumScores(self):
    median = None
    num_scores = sum(self.counts)
    median_rank = num_scores / 2
    index = 0
    for score, count in enumerate(self.counts):
      median = score
      index += count
      if median_rank < index:
        break
    return median, num_scores

  def Add(self, score):
    if score < self.MIN_SCORE:
      score = self.MIN_SCORE
      logging.warn('CountRanker(key_name=%s) value out of range (%s to %s): %s',
                   self.key().name(), self.MIN_SCORE, self.MAX_SCORE, score)
    elif score > self.MAX_SCORE:
      score = self.MAX_SCORE
      logging.warn('CountRanker(key_name=%s) value out of range (%s to %s): %s',
                   self.key().name(), self.MIN_SCORE, self.MAX_SCORE, score)
    slots_needed = score - len(self.counts) + 1
    if slots_needed > 0:
      self.counts.extend([0] * slots_needed)
    self.counts[score] += 1
    RankerCacher.CachePut(self)

  def SetValues(self, counts, num_scores):
    self.counts = counts
    RankerCacher.CachePut(self)

  def ToString(self):
    return array.array('L', self.counts).tostring()

  @classmethod
  def FromString(cls, key_name, value_str):
    counts = array.array('L')
    counts.fromstring(value_str)
    return cls(key_name=key_name, counts=counts.tolist())


class LastNRanker(db.Model):
  """Approximate the median by keeping the last MAX_SCORES scores."""
  MAX_NUM_SAMPLED_SCORES = 100

  scores = db.ListProperty(long, indexed=False)
  num_scores = db.IntegerProperty(default=0, indexed=False)

  def GetMedianAndNumScores(self):
    """Return the median of the last N scores."""
    num_sampled_scores = len(self.scores)
    if num_sampled_scores:
      return self.scores[num_sampled_scores / 2], self.num_scores
    else:
      return None, 0

  def Add(self, score):
    """Add a score into the last N scores.

    If needed, drops the score that is furthest away from the given score.
    """
    num_sampled_scores = len(self.scores)
    if num_sampled_scores < self.MAX_NUM_SAMPLED_SCORES:
      bisect.insort(self.scores, score)
    else:
      index_left = bisect.bisect_left(self.scores, score)
      index_right = bisect.bisect_right(self.scores, score)
      index_center = index_left + (index_right - index_left) / 2
      self.scores.insert(index_left, score)
      if index_center < num_sampled_scores / 2:
        self.scores.pop()
      else:
        self.scores.pop(0)
    self.num_scores += 1
    RankerCacher.CachePut(self)

  def SetValues(self, scores, num_scores):
    self.scores = scores
    self.num_scores = num_scores
    RankerCacher.CachePut(self)

  def ToString(self):
    return array.array('l', self.scores + [self.num_scores]).tostring()

  @classmethod
  def FromString(cls, key_name, value_str):
    scores = array.array('l')
    scores.fromstring(value_str)
    num_scores = scores.pop()
    return cls(key_name=key_name, scores=scores.tolist(), num_scores=num_scores)


def RankerKeyName(category, test_key, browser, params_str=None):
  if params_str:
    params_hash = hashlib.md5(params_str).hexdigest()
    return '_'.join((category, test_key, browser, params_hash))
  else:
    return '_'.join((category, test_key, browser))


def RankerClass(min_value, max_value):
  if min_value >= 0 and max_value <= CountRanker.MAX_SCORE:
    return CountRanker
  else:
    return LastNRanker


def GetRanker(test, browser, params_str=None):
  """Get a ranker that matches the given args.

  Args:
    test: an instance of a test_set_base.TestBase derived class.
    browser: a string like 'Firefox 3' or 'Chrome 2.0.156'.
    params_str: a string representation of test_set_params.Params.
  Returns:
    an instance of a RankerBase derived class (None if not found).
  """
  return GetRankers([(test, browser)], params_str)[0]


def GetRankers(test_browsers, params_str=None, use_insert=False):
  """Get a ranker that matches the given args.

  Args:
    test_browsers: a list of tuples of (test_instance, browser)
        where 'browser' a string like 'Firefox 3' or 'Chrome 2.0.156'.
    params_str: a string representation of test_set_params.Params.
    use_insert: a boolean for whether to create non-existent rankers.
  Returns:
    a list of instances derived from RankerBase
    (None for each ranker that does not exist).
  """
  key_names = []
  ranker_classes = {}
  for test, browser in test_browsers:
    category = test.test_set.category

    # If this is an aliased UserTest (like HTML5), use its key instead.
    if test.test_set.user_test_category is not None:
      category = test.test_set.user_test_category
      #logging.info('GetRankers Special Category: %s:%s' % (category, test.key))

    key_name = RankerKeyName(category, test.key, browser, params_str)
    #logging.info('RankerKeyName: %s' % key_name)
    key_names.append(key_name)
    ranker_classes[key_name] = RankerClass(test.min_value, test.max_value)
  existing_rankers = RankerCacher.CacheGet(key_names, ranker_classes)
  if use_insert:
    rankers = [(existing_rankers.get(key_name, None) or
                ranker_classes[key_name].get_or_insert(key_name))
               for key_name in key_names]
  else:
    rankers = [existing_rankers.get(k, None) for k in key_names]
  #logging.info('Rankers: %s' % rankers)
  return rankers


def GetOrCreateRanker(test, browser, params_str=None):
  """Get a ranker that matches the given args.

  Args:
    test: an instance of a test_set_base.TestBase derived class.
    browser: a string like 'Firefox 3' or 'Chrome 2.0.156'.
    params_str: a string representation of test_set_params.Params.
  Returns:
    an instance of a RankerBase derived class (None if not found).
  """
  return GetRankers([(test, browser)], params_str, use_insert=True)[0]

def GetOrCreateRankers(test_browsers, params_str=None):
  """Get a ranker that matches the given args.

  Args:
    test_browsers: a list of tuples of (test_instance, browser)
        where 'browser' a string like 'Firefox 3' or 'Chrome 2.0.156'.
    params_str: a string representation of test_set_params.Params.
  Returns:
    an instance of a RankerBase derived class (None if not found).
  """
  return GetRankers(test_browsers, params_str, use_insert=True)
