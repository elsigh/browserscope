#!/usr/bin/python2.4
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
from models import result_ranker
import mock_data


class ResultRankerGrandparentTest(unittest.TestCase):
  def testKeyNameNoParams(self):
    key_name = result_ranker.ResultRankerGrandparent.KeyName(
        'category', 'test', 'user_agent_version', '')
    self.assertEqual('category_test_user_agent_version', key_name)

  def testKeyNameWithParams(self):
    key_name = result_ranker.ResultRankerGrandparent.KeyName(
        'category', 'test', 'user_agent_version', 'param1=val1,param2=val2')
    self.assertEqual(
        'category_test_user_agent_version_e2d0b92f7dde373c9889f4c4cde6c59d',
        key_name)


class ResultRankerParentTest(unittest.TestCase):

  def testGetOrCreateMakesDatastoreEntities(self):
    mock_test = mock_data.MockTest('da test', 'Da Test', 'url', 'boolean')
    # test not there
    grandparent_key_name = result_ranker.ResultRankerGrandparent.KeyName(
        'cate', 'da test', 'C 3.p0', '')
    grandparent = result_ranker.ResultRankerParent.get_by_key_name(
        grandparent_key_name)
    self.assertEqual(None, grandparent)
    result_ranker_parent = result_ranker.ResultRankerParent.GetOrCreate(
        'cate', mock_test, 'C 3.p0', params_str=None)
    grandparent = result_ranker.ResultRankerGrandparent.get_by_key_name(
        grandparent_key_name)
    self.assertEqual('cate', grandparent.category)
    query = result_ranker.ResultRankerParent.all()
    query.ancestor(grandparent)
    query.filter('ranker_version =', result_ranker.DEFAULT_RANKER_VERSION)
    result_ranker_parent = query.get()
    self.assertNotEqual(None, result_ranker_parent)

  def testDelete(self):
    category, test_key, ua_version, params_str = 'cat', 'dog', 'mouse 1.0', None
    mock_test = mock_data.MockTest(test_key, test_key.capitalize(), 'url', 'oo')
    result_ranker_parent = result_ranker.ResultRankerParent.GetOrCreate(
        category, mock_test, ua_version, params_str=params_str)
    result_ranker_parent.delete()
    grandparent_key_name = result_ranker.ResultRankerGrandparent.KeyName(
        category, test_key, ua_version, params_str)
    memcache_params = result_ranker.ResultRankerParent.MemcacheParams(
        'current', grandparent_key_name)
    self.assertEqual(None, memcache.get(**memcache_params))
    grandparent = result_ranker.ResultRankerGrandparent.get_by_key_name(
        grandparent_key_name)
    self.assertEqual(None, grandparent)
    query = result_ranker.ResultRankerParent.all()
    query.filter('ranker_version =', 'current')
    result_ranker_parent = query.get()
    self.assertEqual(None, result_ranker_parent)

  def testReleaseNotNextRaises(self):
    category = 'cat'
    test = mock_data.MockTest('foo', 'Boo Hoo', '/poopoo', 'custom')
    user_agent_version = 'Chrome 3'
    params_str = None
    ranker = result_ranker.ResultRankerParent.GetOrCreate(
        category, test, user_agent_version, params_str,
        ranker_version='current')
    self.assertRaises(result_ranker.ReleaseError, ranker.Release)

  def testReleaseBasic(self):
    category = 'cat'
    test = mock_data.MockTest('foo', 'Boo Hoo', '/poopoo', 'custom')
    user_agent_version = 'Chrome 3'
    params_str = None
    ranker = None
    for min_value, ranker_version in (
        (3, 'previous'), (5, 'current'), (7, 'next')):
      ranker_parent = result_ranker.ResultRankerParent.GetOrCreate(
          category, test, user_agent_version, params_str, ranker_version)
      ranker_parent.min_value = min_value
      ranker_parent.put()
    ranker_parent.Release()

    previous_parent = result_ranker.ResultRankerParent.Get(
        category, test, user_agent_version, params_str, 'previous')
    self.assertEqual(5, previous_parent.min_value)

    current_parent = result_ranker.ResultRankerParent.Get(
        category, test, user_agent_version, params_str, 'current')
    self.assertEqual(7, current_parent.min_value)

    next_parent = result_ranker.ResultRankerParent.Get(
        category, test, user_agent_version, params_str, 'next')
    self.assertEqual(None, next_parent)

    # TODO: test that 'previous' was deleted


class ResultRankerTest(unittest.TestCase):
  def testTotalRankedScoresGivesZeroOnEmpty(self):
    mock_test = mock_data.MockTest('empty', 'Empty', '/empty', 'ugly')
    r = result_ranker.ResultRanker.GetOrCreate('cat', mock_test, 'gg 1')
    self.assertEqual(0, r.TotalRankedScores())

  def testTotalRankedScoresGivesOneAfterAdd(self):
    mock_test = mock_data.MockTest('one', 'One', '/one', 'tall')
    r = result_ranker.ResultRanker.GetOrCreate('cat', mock_test, 'gg 2')
    r.Add(10)
    self.assertEqual(1, r.TotalRankedScores())

  def testFindScoreCanRetrieveAllScores(self):
    mock_test = mock_data.MockTest('find', 'Find', '/find', 'lost')
    r = result_ranker.ResultRanker.GetOrCreate('cat', mock_test, 'hh 3')
    scores = [0, 4, 4, 5, 6, 10]
    r.Update(scores)
    self.assertEqual(scores,
                     [r.FindScore(x) for x in range(len(scores))])

  def testAddAfterInitialUpdateSucceeds(self):
    mock_test = mock_data.MockTest('add', 'Add', '/add', 'moire')
    mock_test.min_value = 0
    mock_test.max_value = 60000
    r = result_ranker.ResultRanker.GetOrCreate('cat', mock_test, 'ii 4')
    scores = [0, 554, 555, 555, 59888]
    r.Update(scores)
    r.Add(554)
    self.assertEqual(sorted(scores + [554]),
                     [r.FindScore(x) for x in range(len(scores) + 1)])

  def testRemoveAfterInitialUpdateSucceeds(self):
    mock_test = mock_data.MockTest('del', 'Del', '/del', 'pickle')
    mock_test.min_value = 0
    mock_test.max_value = 60000
    r = result_ranker.ResultRanker.GetOrCreate('cat', mock_test, 'jj 6')
    scores = [0, 554, 555, 555, 59888]
    r.Update(scores)
    r.Remove(554)
    self.assertEqual([0, 555, 555, 59888],
                     [r.FindScore(x) for x in range(len(scores) - 1)])

  def testReset(self):
    mock_test = mock_data.MockTest('del', 'Del', '/del', 'pickle')
    mock_test.min_value = 0
    mock_test.max_value = 60000
    r = result_ranker.ResultRanker.GetOrCreate('cat', mock_test, 'jj 6')
    scores = [0, 554, 555, 555, 59888]
    r.Update(scores)
    r.Reset()
    self.assertEqual((None, 0), r.GetMedianAndNumScores())


  def testGetMedianAndNumScores(self):
    mock_test = mock_data.MockTest('del', 'Del', '/del', 'pickle')
    mock_test.min_value = 0
    mock_test.max_value = 60000
    r = result_ranker.ResultRanker.GetOrCreate('cat', mock_test, 'jj 6')
    scores = [0, 554, 555, 555, 59888]
    r.Update(scores)
    self.assertEqual((555, 5), r.GetMedianAndNumScores())
