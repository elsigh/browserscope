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
from models.result import ResultParent

import mock_data

class ResultTest(unittest.TestCase):

  def testTotalRankedScores(self):
    test_set = mock_data.AddOneTest()

    ranker = result_ranker.GetRanker(
        test_set.category, test_set.GetTest('testDisplay'), 'Firefox 3')
    self.assertEqual(1, ranker.TotalRankedScores())

    ranker = result_ranker.GetRanker(
        test_set.category, test_set.GetTest('testDisplay'), 'Firefox 3.0')
    self.assertEqual(1, ranker.TotalRankedScores())

    ranker = result_ranker.GetRanker(
        test_set.category, test_set.GetTest('testVisibility'), 'Firefox 3')
    self.assertEqual(1, ranker.TotalRankedScores())

    ranker = result_ranker.GetRanker(
        test_set.category, test_set.GetTest('testDisplay'), 'Firefox 3.0.6')
    self.assertEqual(1, ranker.TotalRankedScores())


  def testGetMedianAndNumScores(self):
    test_set = mock_data.AddFiveResultsAndIncrementAllCounts()

    ranker = result_ranker.GetRanker(
        test_set.category, test_set.GetTest('testDisplay'), 'Firefox 3')
    self.assertEqual((300, 5), ranker.GetMedianAndNumScores())

    ranker = result_ranker.GetRanker(
        test_set.category, test_set.GetTest('testVisibility'), 'Firefox 3')
    self.assertEqual((2, 5), ranker.GetMedianAndNumScores())


  def testGetMedianAndNumScoresWithParams(self):
    test_set = mock_data.AddThreeResultsWithParamsAndIncrementAllCounts()

    ranker = result_ranker.GetRanker(
        test_set.category, test_set.GetTest('testDisplay'), 'Firefox 3',
        str(test_set.default_params))
    self.assertEqual((2, 3), ranker.GetMedianAndNumScores())


  def testAddResult(self):
    parent = mock_data.AddOneTestUsingAddResult()
    result_times = parent.get_result_times()
    self.assertEqual(2, len(result_times))
    self.assertEqual('testDisplay', result_times[0].test)
    self.assertEqual(500, result_times[0].score)
    self.assertEqual('testVisibility', result_times[1].test)
    self.assertEqual(200, result_times[1].score)


  def testAddResultForTestSetWithAdjustResults(self):
    parent = mock_data.AddOneTestUsingAddResultWithAdjustResults()
    self.assertEqual(500, parent.testDisplay)
    self.assertEqual(200, parent.testVisibility)
    result_times = parent.get_result_times()
    self.assertEqual(2, len(result_times))
    self.assertEqual('testDisplay', result_times[0].test)
    self.assertEqual(250, result_times[0].score)
    self.assertEqual('testVisibility', result_times[1].test)
    self.assertEqual(100, result_times[1].score)


  def testAddResultWithExpando(self):
    parent = mock_data.AddOneTestUsingAddResultWithExpando()
    result_times = parent.get_result_times()
    self.assertEqual(2, len(result_times))
    self.assertEqual(20, parent.testDisplay)
    self.assertEqual('testeroo', parent.testVisibility)
    self.assertEqual('testDisplay', result_times[0].test)
    self.assertEqual(500, result_times[0].score)
    self.assertEqual('testVisibility', result_times[1].test)
    self.assertEqual(200, result_times[1].score)


class ChromeFrameAddResultTest(unittest.TestCase):

  def testAddResult(self):
    chrome_ua_string = ('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) '
                        'AppleWebKit/530.1 (KHTML, like Gecko) '
                        'Chrome/2.0.169.1 Safari/530.1')
    ua_string = (
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 6.0; Trident/4.0; '
        'chromeframe; SLCC1; .NET CLR 2.0.5077; 3.0.30729),gzip(gfe),gzip(gfe)')

    test_set = mock_data.MockTestSet('category-for-chrome-frame-test')
    parent = ResultParent.AddResult(
        test_set, '12.2.2.25', ua_string, 'testDisplay=500,testVisibility=200',
        js_user_agent_string=chrome_ua_string)
    self.assertEqual(chrome_ua_string,
                     parent.user_agent.js_user_agent_string)
