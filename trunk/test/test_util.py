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

"""Shared Models Unit Tests."""

__author__ = 'elsigh@google.com (Lindsey Simon)'

import unittest
import random
import logging

from google.appengine.ext import db
from google.appengine.api import memcache
from django.http import HttpRequest
from django.test.client import Client

from base import util
from categories import test_set_params
from models import result
from models.user_agent import UserAgent

import mock_data
import settings

from categories import richtext

class TestUtilHandlers(unittest.TestCase):

  def setUp(self):
    self.client = Client()

  def testHome(self):
    response = self.client.get('/', {},
        **mock_data.UNIT_TEST_UA)
    self.assertEqual(200, response.status_code)


  def testHomeWithResults(self):
    test_set = mock_data.MockTestSet('cat_home')
    params = {'cat_home_results': 'testDisplay=1558,testVisibility=1227'}
    response = self.client.get('/', params, **mock_data.UNIT_TEST_UA)
    self.assertEqual(200, response.status_code)


  def testBeaconWithoutCsrfToken(self):
    params = {}
    response = self.client.get('/beacon', params, **mock_data.UNIT_TEST_UA)
    self.assertEqual(403, response.status_code)


  def testBeaconWithoutCategory(self):
    csrf_token = self.client.get('/get_csrf').content
    params = {'results': 'testDisply:200', 'csrf_token': csrf_token}
    response = self.client.get('/beacon', params, **mock_data.UNIT_TEST_UA)
    self.assertEqual(util.BAD_BEACON_MSG + 'Category/Results', response.content)


  def testBeacon(self):
    category = 'test_beacon'
    test_set = mock_data.MockTestSet(category)
    csrf_token = self.client.get('/get_csrf').content
    params = {
      'category': category,
      'results': 'testDisplay=1,testVisibility=2',
      'csrf_token': csrf_token
    }
    response = self.client.get('/beacon', params, **mock_data.UNIT_TEST_UA)
    self.assertEqual(204, response.status_code)

    # Did a ResultParent get created?
    query = db.Query(result.ResultParent)
    query.filter('category =', category)
    result_parent = query.get()
    self.assertNotEqual(result_parent, None)

    # Were ResultTimes created?
    result_times = result_parent.get_result_times_as_query()
    self.assertEqual(2, result_times.count())
    self.assertEqual(1, result_times[0].score)
    self.assertEqual('testDisplay', result_times[0].test)
    self.assertEqual(2, result_times[1].score)
    self.assertEqual('testVisibility', result_times[1].test)
    self.assertEqual(True, result_times[0].dirty)
    self.assertEqual(True, result_times[1].dirty)


  def testBeaconWithBogusTests(self):
    category = 'test_beacon_w_bogus_tests'
    test_set = mock_data.MockTestSet(category)
    csrf_token = self.client.get('/get_csrf').content
    params = {
      'category': category,
      'results': 'testBogus=1,testVisibility=2',
      'csrf_token': csrf_token
    }
    response = self.client.get('/beacon', params, **mock_data.UNIT_TEST_UA)
    self.assertEqual(util.BAD_BEACON_MSG + 'ResultParent', response.content)

    # Did a ResultParent get created? Shouldn't have.
    query = db.Query(result.ResultParent)
    query.filter('category =', category)
    result_parent = query.get()
    self.assertEqual(None, result_parent)


  def testBeaconWithoutTestSet(self):
    category = 'test_beacon_wo_test_set'
    csrf_token = self.client.get('/get_csrf').content
    params = {
      'category': category,
      'results': 'testDisplay=1,testVisibility=2',
      'csrf_token': csrf_token
    }
    response = self.client.get('/beacon', params, **mock_data.UNIT_TEST_UA)
    self.assertEqual(util.BAD_BEACON_MSG + 'TestSet', response.content)


  def testBeaconWithParams(self):
    category = 'test_beacon_w_params'
    test_set = mock_data.MockTestSet(category)
    csrf_token = self.client.get('/get_csrf').content
    beacon_params = test_set_params.Params(
        'nested_anchors',
        'num_elements=1000',
        'num_css_rules=1000',
        'num_nest=2',
        'css_selector=#g-content *',
        'css_text=border: 1px solid #0C0; padding: 8px;')
    params = {
      'category': category,
      'results': 'testDisplay=1,testVisibility=2',
      'params': str(beacon_params),
      'csrf_token': csrf_token
    }
    response = self.client.get('/beacon', params, **mock_data.UNIT_TEST_UA)

    # Did a ResultParent get created?
    query = db.Query(result.ResultParent)
    query.filter('category =', category)
    query.filter('params_str =', str(beacon_params))
    result_parent = query.get()
    self.assertNotEqual(None, result_parent)

    # Were ResultTimes created?
    result_times = result.ResultTime.all().ancestor(result_parent)
    self.assertEqual(2, result_times.count())
    self.assertEqual(1, result_times[0].score)
    self.assertEqual('testDisplay', result_times[0].test)
    self.assertEqual(True, result_times[0].dirty)
    self.assertEqual(2, result_times[1].score)
    self.assertEqual('testVisibility', result_times[1].test)
    self.assertEqual(True, result_times[1].dirty)


class TestUtilFunctions(unittest.TestCase):

  def setUp(self):
    memcache.flush_all()

  def testCheckThrottleIpAddress(self):
    ip = mock_data.UNIT_TEST_UA['REMOTE_ADDR']
    ua_string = mock_data.UNIT_TEST_UA['HTTP_USER_AGENT']
    for i in range(11):
      self.assertTrue(util.CheckThrottleIpAddress(ip, ua_string))
    # The next one should bomb.
    self.assertFalse(util.CheckThrottleIpAddress(ip, ua_string))


class TestStats(unittest.TestCase):

  # overload this
  #def util.GetTestsByCategory(category):
  #  tests = (
  #    ('test1', 'Test 1', 'url1', 'boolean')
  #  )
  #  return tests

  def setUp(self):
    # Every test needs a client.
    self.client = Client()


  def GetStatsData(self, use_memcache):

    test_set = mock_data.AddFiveResultsAndIncrementAllCounts()
    user_agents = mock_data.GetUserAgent().get_string_list()

    request = HttpRequest()
    request.META = {'HTTP_USER_AGENT': 'Firefox 3.0.1'}

    stats = util.GetStatsData(test_set.category,
        test_set.tests, user_agents, params_str=None,
        use_memcache=use_memcache)

    expected_medians = {'testDisplay': 300, 'testVisibility': 2}
    expected_scores = {'testDisplay': 9, 'testVisibility': 10}
    expected_display = {'testDisplay': '3X', 'testVisibility':
                        settings.STATS_SCORE_TRUE}
    for test in test_set.tests:
      for user_agent in user_agents:
        self.assertEqual(expected_medians[test.key],
                         stats[user_agent]['results'][test.key]['median'])
        self.assertEqual(expected_scores[test.key],
                         stats[user_agent]['results'][test.key]['score'])
        self.assertEqual(expected_display[test.key],
                         stats[user_agent]['results'][test.key]['display'])

    expected_total_runs = 5
    for user_agent in user_agents:
      self.assertEqual(expected_total_runs, stats[user_agent]['total_runs'])


  def testGetStatsDataWithoutMemcache(self):
    self.GetStatsData(use_memcache=False)

  def testGetStatsDataWithParamsLiteralNoneRaises(self):
    # A params_str with a None value is fine, but not a 'None' string
    test_set = mock_data.MockTestSet('categore')
    self.assertRaises(
        ValueError,
        util.GetStatsData, test_set.category, test_set.tests, ['ua1'], 'None')

  def testGetStatsDataWithParamsEmptyStringRaises(self):
    test_set = mock_data.MockTestSet('categore')
    self.assertRaises(
        ValueError,
        util.GetStatsData, test_set.category, test_set.tests, ['ua1'], '')

if __name__ == '__main__':
  unittest.main()
