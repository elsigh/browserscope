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

"""Result ranker Unit Tests."""

__author__ = 'slamm@google.com (Stephen Lamm)'

import logging
import unittest

from google.appengine.api import datastore
from google.appengine.api import datastore_errors
from google.appengine.api import memcache
from categories import test_set_base
from models import result_ranker
from third_party import mox

import mock_data

MockTestSet = mock_data.MockTestSet


class RankerCacherTest(unittest.TestCase):
  def setUp(self):
    self.mox = mox.Mox()
    self.cls = result_ranker.RankerCacher
    self.memcache_params = {'namespace': self.cls.MEMCACHE_NAMESPACE}

  def tearDown(self):
    self.mox.UnsetStubs()

  def testCacheGetOneItemInMemcache(self):
    ranker_class = self.mox.CreateMock(result_ranker.CountRanker)
    self.mox.StubOutWithMock(memcache, 'get_multi')
    memcache.get_multi(['k1'], **self.memcache_params).AndReturn({'k1': 's1'})
    ranker_class.FromString('k1', 's1').AndReturn('r1')
    self.mox.ReplayAll()
    rankers = self.cls.CacheGet(['k1'], {'k1': ranker_class})
    self.mox.VerifyAll()
    self.assertEqual({'k1': 'r1'}, rankers)

  def testCacheGetOneItemInDb(self):
    ranker_class = self.mox.CreateMock(result_ranker.CountRanker)
    self.mox.StubOutWithMock(memcache, 'get_multi')
    memcache.get_multi(['k1'], **self.memcache_params).AndReturn({})
    ranker_class.get_by_key_name(['k1']).AndReturn(['r1'])
    self.mox.ReplayAll()
    rankers = self.cls.CacheGet(['k1'], {'k1': ranker_class})
    self.mox.VerifyAll()
    self.assertEqual({'k1': 'r1'}, rankers)

  def testCacheGetOneItemNotFound(self):
    ranker_class = self.mox.CreateMock(result_ranker.CountRanker)
    self.mox.StubOutWithMock(memcache, 'get_multi')
    memcache.get_multi(['k1'], **self.memcache_params).AndReturn({})
    ranker_class.get_by_key_name(['k1']).AndReturn([None])
    self.mox.ReplayAll()
    rankers = self.cls.CacheGet(['k1'], {'k1': ranker_class})
    self.mox.VerifyAll()
    self.assertEqual({}, rankers)

  def testCacheGetMulti(self):
    ranker_class_a = self.mox.CreateMock(result_ranker.CountRanker)
    ranker_class_b = self.mox.CreateMock(result_ranker.LastNRanker)
    self.mox.StubOutWithMock(memcache, 'get_multi')
    memcache.get_multi(
        ['ka1', 'ka2', 'kb1', 'kb2', 'kb3'], **self.memcache_params).AndReturn(
        {'ka2': 'sa2'})
    ranker_class_a.FromString('ka2', 'sa2').AndReturn('ra2')
    ranker_class_a.get_by_key_name(['ka1']).InAnyOrder().AndReturn([])
    ranker_class_b.get_by_key_name(['kb1', 'kb2', 'kb3']).InAnyOrder(
        ).AndReturn([None, 'rb2', None])
    self.mox.ReplayAll()
    rankers = self.cls.CacheGet(['ka1', 'ka2', 'kb1', 'kb2', 'kb3'], {
        'ka1': ranker_class_a,
        'ka2': ranker_class_a,
        'kb1': ranker_class_b,
        'kb2': ranker_class_b,
        'kb3': ranker_class_b,
        })
    self.mox.VerifyAll()
    self.assertEqual({'ka2': 'ra2', 'kb2': 'rb2'}, rankers)


class CountRankerTest(unittest.TestCase):
  def setUp(self):
    self.test_set = MockTestSet()
    self.ranker_params = (self.test_set.tests[1], 'Android 0.5')
    self.ranker = result_ranker.GetOrCreateRanker(*self.ranker_params)

  def testAddScore(self):
    ranker = result_ranker.GetRanker(*self.ranker_params)
    ranker.Add(2)
    ranker = result_ranker.GetRanker(*self.ranker_params)
    self.assertEqual([0, 0, 1], ranker.counts)
    self.assertEqual((2, 1), ranker.GetMedianAndNumScores())
    ranker.Add(4)
    ranker = result_ranker.GetRanker(*self.ranker_params)
    self.assertEqual([0, 0, 1, 0, 1], ranker.counts)
    self.assertEqual((4, 2), ranker.GetMedianAndNumScores())
    ranker.Add(2)
    ranker = result_ranker.GetRanker(*self.ranker_params)
    self.assertEqual([0, 0, 2, 0, 1], ranker.counts)
    self.assertEqual((2, 3), ranker.GetMedianAndNumScores())

  def testSetValues(self):
    ranker = result_ranker.GetRanker(*self.ranker_params)
    ranker.SetValues([0, 3, 1, 3], 7)
    ranker = result_ranker.GetRanker(*self.ranker_params)
    self.assertEqual((2, 7), ranker.GetMedianAndNumScores())
    ranker.SetValues([4, 3], 7)
    ranker = result_ranker.GetRanker(*self.ranker_params)
    self.assertEqual((0, 7), ranker.GetMedianAndNumScores())
    ranker.Add(1)
    ranker = result_ranker.GetRanker(*self.ranker_params)
    self.assertEqual((1, 8), ranker.GetMedianAndNumScores())

  def testAddScoreTooBig(self):
    ranker = result_ranker.GetRanker(*self.ranker_params)
    ranker.Add(101)
    ranker = result_ranker.GetRanker(*self.ranker_params)
    self.assertEqual((100, 1), ranker.GetMedianAndNumScores())

  def testAddScoreTooSmall(self):
    ranker = result_ranker.GetRanker(*self.ranker_params)
    ranker.Add(-1)
    ranker = result_ranker.GetRanker(*self.ranker_params)
    self.assertEqual((0, 1), ranker.GetMedianAndNumScores())


class LastNRankerTest(unittest.TestCase):
  def setUp(self):
    self.test_set = MockTestSet()
    self.ranker_params = (self.test_set.tests[2], 'Safari 4.1')
    self.ranker = result_ranker.GetOrCreateRanker(*self.ranker_params)
    self.old_max_num_scores = result_ranker.LastNRanker.MAX_NUM_SAMPLED_SCORES

  def tearDown(self):
    result_ranker.LastNRanker.MAX_NUM_SAMPLED_SCORES = self.old_max_num_scores

  def testAddScore(self):
    ranker = result_ranker.GetRanker(*self.ranker_params)
    ranker.Add(1000)
    ranker = result_ranker.GetRanker(*self.ranker_params)
    self.assertEqual([1000], ranker.scores)
    self.assertEqual((1000, 1), ranker.GetMedianAndNumScores())

    ranker.Add(0)
    ranker = result_ranker.GetRanker(*self.ranker_params)
    self.assertEqual([0, 1000], ranker.scores)
    self.assertEqual((1000, 2), ranker.GetMedianAndNumScores())
    ranker.Add(500)
    ranker = result_ranker.GetRanker(*self.ranker_params)
    self.assertEqual([0, 500, 1000], ranker.scores)
    self.assertEqual((500, 3), ranker.GetMedianAndNumScores())

  def testSetValues(self):
    ranker = result_ranker.GetRanker(*self.ranker_params)
    ranker.SetValues([4, 4, 5, 5, 6], 10)
    ranker = result_ranker.GetRanker(*self.ranker_params)
    self.assertEqual((5, 10), ranker.GetMedianAndNumScores())
    ranker.Add(4)
    ranker = result_ranker.GetRanker(*self.ranker_params)
    self.assertEqual((5, 11), ranker.GetMedianAndNumScores())
    ranker.Add(4)
    ranker = result_ranker.GetRanker(*self.ranker_params)
    self.assertEqual([4, 4, 4, 4, 5, 5, 6], ranker.scores)
    self.assertEqual((4, 12), ranker.GetMedianAndNumScores())

  def testDropLowScore(self):
    result_ranker.LastNRanker.MAX_NUM_SAMPLED_SCORES = 5
    ranker = result_ranker.GetRanker(*self.ranker_params)
    ranker.SetValues([4, 4, 5, 5, 6], 15)
    ranker.Add(5)
    ranker = result_ranker.GetRanker(*self.ranker_params)
    self.assertEqual([4, 5, 5, 5, 6], ranker.scores)
    self.assertEqual((5, 16), ranker.GetMedianAndNumScores())

  def testDropHighScore(self):
    result_ranker.LastNRanker.MAX_NUM_SAMPLED_SCORES = 4
    ranker = result_ranker.GetRanker(*self.ranker_params)
    ranker.SetValues([4, 4, 5, 5], 20)
    ranker.Add(4)
    ranker = result_ranker.GetRanker(*self.ranker_params)
    self.assertEqual([4, 4, 4, 5], ranker.scores)
    self.assertEqual((4, 21), ranker.GetMedianAndNumScores())


class GetRankersTest(unittest.TestCase):
  def setUp(self):
    self.test_set = MockTestSet()

  def testGetRankersOneDoesNotExist(self):
    test = self.test_set.tests[0]
    rankers = result_ranker.GetRankers([(test, 'Android 1.5')])
    self.assertEqual([None], rankers)
