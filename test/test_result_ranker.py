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

import unittest
import logging

from models import result_ranker
from third_party.pymox import mox
import mock_data


class ResultRankerParentTest(unittest.TestCase):

  def testKeyNameNoParams(self):
    key_name = result_ranker.ResultRankerParent.KeyName(
        'category', 'test', 'user_agent_version', '')
    self.assertEqual('category_test_user_agent_version', key_name)

  def testKeyNameWithParams(self):
    key_name = result_ranker.ResultRankerParent.KeyName(
        'category', 'test', 'user_agent_version',
        ','.join(['param1=val1', 'param2=val2', 'param3=val3']))
    self.assertEqual(
        'category_test_user_agent_version_1c565ba4056b84201ed4fe4c4b6b2e42',
        key_name)

  def testFactoryCreatesDatastoreEntity(self):
    mock_test = mock_data.MockTest('da test', 'Da Test', 'url', 'boolean')
    result_ranker_parent = result_ranker.ResultRankerParent.factory(
        'cate', mock_test, 'C 3.p0', params=None)
    key_name = result_ranker.ResultRankerParent.KeyName(
        'cate', 'da test', 'C 3.p0', '')
    result = result_ranker.ResultRankerParent.get_by_key_name(key_name)
    self.assertEqual('cate', result.category)


class MedianRankerTest(unittest.TestCase):
  def setUp(self):
    self.mox = mox.Mox()
    storage = None
    self.ranker = result_ranker.MedianRanker(storage, 10, 1009, 10)

  def tearDown(self):
    self.mox.UnsetStubs()
    self.mox.VerifyAll()

  def testGetMedianAndNumScoresWithZeroScores(self):
    self.mox.StubOutWithMock(self.ranker, 'TotalRankedScores')
    self.mox.StubOutWithMock(self.ranker, 'FindScore')
    self.ranker.TotalRankedScores().AndReturn(0)
    self.mox.ReplayAll()
    median, num_scores = self.ranker.GetMedianAndNumScores()
    self.assertEqual(None, median)
    self.assertEqual(0, num_scores)

  def testGetMedianAndNumScoreWithOddNumber(self):
    self.mox.StubOutWithMock(self.ranker, 'TotalRankedScores')
    self.mox.StubOutWithMock(self.ranker, 'FindScore')
    self.ranker.TotalRankedScores().AndReturn(25)
    self.ranker.FindScore(12).AndReturn(99)
    self.mox.ReplayAll()
    median, num_scores = self.ranker.GetMedianAndNumScores()
    self.assertEqual(99, median)
    self.assertEqual(25, num_scores)


class ResultRankerTest(unittest.TestCase):
  def testTotalRankedScoresGivesZeroOnEmpty(self):
    mock_test = mock_data.MockTest('empty', 'Empty', '/empty', 'ugly')
    r = result_ranker.ResultRanker('cat', mock_test, 'gg 1')
    self.assertEqual(0, r.TotalRankedScores())

  def testTotalRankedScoresGivesOneAfterAdd(self):
    mock_test = mock_data.MockTest('one', 'One', '/one', 'tall')
    r = result_ranker.ResultRanker('cat', mock_test, 'gg 2')
    r.Add(10)
    self.assertEqual(1, r.TotalRankedScores())

  def testFindScoreCanRetrieveAllScores(self):
    mock_test = mock_data.MockTest('find', 'Find', '/find', 'lost')
    r = result_ranker.ResultRanker('cat', mock_test, 'hh 3')
    scores = [0, 4, 4, 5, 6, 10]
    r.Update(scores)
    self.assertEqual(scores,
                     [r.FindScore(x) for x in range(len(scores))])

  def testAddAfterInitialUpdateSucceeds(self):
    mock_test = mock_data.MockTest('add', 'Add', '/add', 'moire')
    mock_test.min_value = 0
    mock_test.max_value = 60000
    r = result_ranker.ResultRanker('cat', mock_test, 'ii 4')
    scores = [0, 554, 555, 555, 59888]
    r.Update(scores)
    r.Add(554)
    self.assertEqual(sorted(scores + [554]),
                     [r.FindScore(x) for x in range(len(scores) + 1)])

  def testDeleteAfterInitialUpdateSucceeds(self):
    mock_test = mock_data.MockTest('del', 'Del', '/del', 'pickle')
    mock_test.min_value = 0
    mock_test.max_value = 60000
    r = result_ranker.ResultRanker('cat', mock_test, 'jj 6')
    scores = [0, 554, 555, 555, 59888]
    r.Update(scores)
    r.Remove(554)
    self.assertEqual([0, 555, 555, 59888],
                     [r.FindScore(x) for x in range(len(scores) - 1)])


class RankListRankerTest(unittest.TestCase):

  def testKeyNameNoParams(self):
    key_name = result_ranker.RankListRanker.KeyName(
        'category', 'test', 'user_agent_version')
    self.assertEqual('category_test_user_agent_version', key_name)

  def testKeyNameWithParams(self):
    key_name = result_ranker.RankListRanker.KeyName(
        'category', 'test', 'user_agent_version',
        ['param1=val1', 'param2=val2', 'param3=val3'])
    self.assertEqual(
        'category_test_user_agent_version_1c565ba4056b84201ed4fe4c4b6b2e42',
        key_name)
