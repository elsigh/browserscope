#!/usr/bin/python2.5
# Copyright 2009 Google Inc.
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
#
# Author slamm@google.com (Stephen Lamm)


import unittest
import score_ranker


class TestGetShallowBranchingFactor(unittest.TestCase):
  def testGetShallowBranchingFactorOneLevel(self):
    self.assertEqual(8, score_ranker.GetShallowBranchingFactor(0, 7, 100))

  def testGetShallowBranchingFactorBasic(self):
    self.assertEqual(40, score_ranker.GetShallowBranchingFactor(0, 60000, 100))

  def testGetShallowBranchingFactorAtMax(self):
    self.assertEqual(10, score_ranker.GetShallowBranchingFactor(1, 1000, 10))


class MockStorage(score_ranker.StorageBase):
  def __init__(self):
    self.data = {}

  def RunInTransaction(self, func, *args, **kwds):
    return func(*args, **kwds)

  def Get(self, node_index):
    return self.data.get(node_index, None)

  def SetMultiple(self, nodes):
    for node_index, child_counts in nodes.items():
      self.data[node_index] = child_counts

  def GetMultiple(self, node_indexes):
    nodes = {}
    for node_index in node_indexes:
      if node_index in self.data:
        nodes[node_index] = self.data[node_index]
    return nodes

  def DeleteMultiple(self, node_indexes):
    for node_index in node_indexes:
      if node_index in self.data:
        del self.data[node_index]


class TestRanker(unittest.TestCase):
  def setUp(self):
    self.storage = MockStorage()

  def testTotalRankedScoresGivesZeroOnEmpty(self):
    r = score_ranker.Ranker(self.storage, 0, 2, 2)
    self.assertEqual(0, r.TotalRankedScores())

  def testTotalRankedScoresGivesOneAfterAdd(self):
    r = score_ranker.Ranker(self.storage, 0, 20, 10)
    r.Add(10)
    self.assertEqual(1, r.TotalRankedScores())

  def testFindScoreCanRetrieveAllScores(self):
    r = score_ranker.Ranker(self.storage, 0, 20, 4)
    scores = [0, 4, 4, 5, 6, 10]
    r.Update(scores)
    self.assertEqual(scores,
                     [r.FindScore(x) for x in range(len(scores))])

  def testAddAfterInitialUpdateSucceeds(self):
    r = score_ranker.Ranker(self.storage, 0, 60000, 40)
    scores = [0, 554, 555, 555, 59888]
    r.Update(scores)
    r.Add(554)
    self.assertEqual(sorted(scores + [554]),
                     [r.FindScore(x) for x in range(len(scores) + 1)])

  def testDeleteAfterInitialUpdateSucceeds(self):
    r = score_ranker.Ranker(self.storage, 0, 60000, 40)
    scores = [0, 554, 555, 555, 59888]
    r.Update(scores)
    r.Remove(554)
    self.assertEqual([0, 555, 555, 59888],
                     [r.FindScore(x) for x in range(len(scores) - 1)])


  def testFindScoreAndNumScoresMedian(self):
    r = score_ranker.Ranker(self.storage, 0, 60000, 40)
    scores = [0, 554, 555, 555, 59888]
    r.Update(scores)
    self.assertEqual((555, 5), r.FindScoreAndNumScores(percentile=50))

  def testFindScoreAndNumScoresEmpty(self):
    r = score_ranker.Ranker(self.storage, 0, 60000, 40)
    self.assertEqual((None, 0), r.FindScoreAndNumScores(percentile=1))

if __name__ == '__main__':
  unittest.main()
