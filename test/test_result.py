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

"""Shared Models Unit Tests."""

__author__ = 'elsigh@google.com (Lindsey Simon)'

import new
import unittest

from google.appengine.ext import db
from categories import all_test_sets
from categories import test_set_params
from base import manage_dirty
from models import result_stats
from models.result import ResultParent
from models.result import ResultTime

import mock_data

def AddAdjustResults(test_set):
  def AdjustResults(self, results):
    for values in results.values():
      # Add the raw value to be expando'd and store a munged value in score.
      values['expando'] = values['raw_score']
      values['raw_score'] = int(round(values['raw_score'] / 2.0))
    return results
  test_set.AdjustResults = new.instancemethod(
      AdjustResults, test_set, test_set.__class__)


class ResultTest(unittest.TestCase):

  def setUp(self):
    self.test_set = mock_data.MockTestSet()
    all_test_sets.AddTestSet(self.test_set)

  def tearDown(self):
    all_test_sets.RemoveTestSet(self.test_set)

  def testGetMedianAndNumScores(self):
    for scores in ((0, 0, 500), (1, 1, 200),
                   (0, 2, 300), (1, 3, 100), (0, 4, 400)):
      parent = ResultParent.AddResult(
          self.test_set,
          '12.2.2.25',
          mock_data.GetUserAgentString('Firefox 3.5'),
          'apple=%s,banana=%s,coconut=%s' % scores)
    rankers = self.test_set.GetRankers('Firefox 3')
    self.assertEqual([(0, 5), (2, 5), (300, 5)],
                     [ranker.GetMedianAndNumScores() for ranker in rankers])

  def testGetMedianAndNumScoresWithParams(self):
    params = test_set_params.Params('w-params', 'a=b', 'c=d', 'e=f')
    self.test_set.default_params = params
    for scores in ((1, 0, 2), (1, 1, 1), (0, 2, 200)):
      parent = ResultParent.AddResult(
          self.test_set,
          '12.2.2.25',
          mock_data.GetUserAgentString('Firefox 3.5'),
          'apple=%s,banana=%s,coconut=%s' % scores,
          params_str=str(params))
    ranker = self.test_set.GetTest('coconut').GetRanker('Firefox 3')
    self.assertEqual((2, 3), ranker.GetMedianAndNumScores())

  def testAddResult(self):
    parent = ResultParent.AddResult(
        self.test_set, '12.2.2.25', mock_data.GetUserAgentString('Firefox 3.5'),
        'apple=1,banana=11,coconut=111')
    expected_results = {
        'apple': 1,
        'banana': 11,
        'coconut': 111,
        }
    self.assertEqual(expected_results, parent.GetResults())

  def testAddResultForTestSetWithAdjustResults(self):
    AddAdjustResults(self.test_set)
    parent = ResultParent.AddResult(
        self.test_set, '12.2.2.25', mock_data.GetUserAgentString('Firefox 3.5'),
        'apple=0,banana=80,coconut=200')
    self.assertEqual(0, parent.apple)
    self.assertEqual(80, parent.banana)
    self.assertEqual(200, parent.coconut)
    expected_results = {
        'apple': 0,
        'banana': 40,
        'coconut': 100,
        }
    self.assertEqual(expected_results, parent.GetResults())


  def testAddResultWithExpando(self):
    AddAdjustResults(self.test_set)
    parent = ResultParent.AddResult(
        self.test_set, '12.2.2.25', mock_data.GetUserAgentString('Firefox 3.5'),
        'apple=1,banana=49,coconut=499')
    self.assertEqual(1, parent.apple)
    self.assertEqual(49, parent.banana)
    self.assertEqual(499, parent.coconut)
    expected_results = {
        'apple': 1,
        'banana': 25,
        'coconut': 250,
        }
    self.assertEqual(expected_results, parent.GetResults())

  def testAddResultWithParamsLiteralNoneRaises(self):
    # A params_str with a None value is fine, but not a 'None' string
    ua_string = (
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 6.0; Trident/4.0; '
        'chromeframe; SLCC1; .NET CLR 2.0.5077; 3.0.30729),gzip(gfe),gzip(gfe)')
    self.assertRaises(
        ValueError,
        ResultParent.AddResult, self.test_set, '12.1.1.1', ua_string,
        'testDisplay=500,testVisibility=200', params_str='None')

  def testGetStatsDataWithParamsEmptyStringRaises(self):
    ua_string = (
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 6.0; Trident/4.0; '
        'chromeframe; SLCC1; .NET CLR 2.0.5077; 3.0.30729),gzip(gfe),gzip(gfe)')
    self.assertRaises(
        ValueError,
        ResultParent.AddResult, self.test_set, '12.1.1.1', ua_string,
        'testDisplay=500,testVisibility=200', params_str='')


class IncrementAllCountsTest(unittest.TestCase):

  def setUp(self):
    self.test_set = mock_data.MockTestSet()
    all_test_sets.AddTestSet(self.test_set)

  def tearDown(self):
    all_test_sets.RemoveTestSet(self.test_set)

  def testIncrementAllCountsBogusTest(self):
    parent = ResultParent.AddResult(
        self.test_set, '12.2.2.25', mock_data.GetUserAgentString('Firefox 3.5'),
        'apple=0,banana=44,coconut=444')
    db.put(ResultTime(parent=parent,
                      test='bogus test key',
                      score=1,
                      dirty=True))
    self.assertEqual(3 + 1, ResultTime.all(keys_only=True).count())
    dirty_query = manage_dirty.DirtyResultTimesQuery()
    parent.UpdateStatsFromDirty(dirty_query)
    self.assert_(dirty_query.IsResultParentDone())


class ChromeFrameAddResultTest(unittest.TestCase):

  def setUp(self):
    self.test_set = mock_data.MockTestSet()
    all_test_sets.AddTestSet(self.test_set)

  def tearDown(self):
    all_test_sets.RemoveTestSet(self.test_set)

  def testAddResult(self):
    chrome_ua_string = ('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) '
                        'AppleWebKit/530.1 (KHTML, like Gecko) '
                        'Chrome/2.0.169.1 Safari/530.1')
    ua_string = (
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 6.0; Trident/4.0; '
        'chromeframe; SLCC1; .NET CLR 2.0.5077; 3.0.30729),gzip(gfe),gzip(gfe)')

    parent = ResultParent.AddResult(
        self.test_set, '12.2.2.25', ua_string, 'apple=1,banana=3,coconut=500',
        js_user_agent_string=chrome_ua_string)
    self.assertEqual(chrome_ua_string,
                     parent.user_agent.js_user_agent_string)
