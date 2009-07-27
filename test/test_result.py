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

"""Shared Models Unit Tests."""

__author__ = 'elsigh@google.com (Lindsey Simon)'

import unittest
import logging

from models import result_ranker

import mock_data

class ResultTest(unittest.TestCase):

  def testTotalRankedScores(self):
    test_set = mock_data.AddOneTest()

    ranker = result_ranker.Factory(
        test_set.category, test_set.GetTest('testDisplay'), 'Firefox 3')
    self.assertEqual(1, ranker.TotalRankedScores())

    ranker = result_ranker.Factory(
        test_set.category, test_set.GetTest('testDisplay'), 'Firefox 3.0')
    self.assertEqual(1, ranker.TotalRankedScores())

    ranker = result_ranker.Factory(
        test_set.category, test_set.GetTest('testVisibility'), 'Firefox 3')
    self.assertEqual(1, ranker.TotalRankedScores())

    ranker = result_ranker.Factory(
        test_set.category, test_set.GetTest('testDisplay'), 'Firefox 3.0.6')
    self.assertEqual(1, ranker.TotalRankedScores())


  def testGetMedian(self):
    test_set = mock_data.AddFiveResultsAndIncrementAllCounts()

    ranker = result_ranker.Factory(
        test_set.category, test_set.GetTest('testDisplay'), 'Firefox 3')
    self.assertEqual(300, ranker.GetMedian())

    ranker = result_ranker.Factory(
        test_set.category, test_set.GetTest('testVisibility'), 'Firefox 3')
    self.assertEqual(2, ranker.GetMedian())
    self.assertEqual((2, 5), ranker.GetMedianAndNumScores())


  def testGetMedianWithParams(self):
    test_set = mock_data.AddThreeResultsWithParamsAndIncrementAllCounts()

    ranker = result_ranker.Factory(
        test_set.category, test_set.GetTest('testDisplay'), 'Firefox 3',
        test_set.default_params)
    self.assertEqual(2, ranker.GetMedian())


  def testAddResult(self):
    parent = mock_data.AddOneTestUsingAddResult()
    result_times = parent.get_result_times()
    self.assertEqual(2, len(result_times))
    self.assertEqual('testDisplay', result_times[0].test)
    self.assertEqual(500, result_times[0].score)
    self.assertEqual('testVisibility', result_times[1].test)
    self.assertEqual(200, result_times[1].score)


  def testAddResultWithExpando(self):
    parent = mock_data.AddOneTestUsingAddResultWithExpando()
    result_times = parent.get_result_times()
    self.assertEqual(2, len(result_times))
    self.assertEqual('testDisplay', result_times[0].test)
    self.assertEqual(500, result_times[0].score)
    self.assertEqual(20, parent.testDisplay)
    self.assertEqual('testVisibility', result_times[1].test)
    self.assertEqual(200, result_times[1].score)
    self.assertEqual('testeroo', parent.testVisibility)


