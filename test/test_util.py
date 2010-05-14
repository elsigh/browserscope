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

import unittest
import random
import logging

from google.appengine.ext import db
from google.appengine.api import memcache
from django.test.client import Client

from base import util
from categories import all_test_sets
from categories import test_set_params
from models import result
from models.user_agent import UserAgent

import mock_data
import settings

from categories import richtext

class TestHome(unittest.TestCase):

  def setUp(self):
    self.client = Client()

  def testHome(self):
    response = self.client.get('/', {}, **mock_data.UNIT_TEST_UA)
    self.assertEqual(200, response.status_code)

  #def testHomeWithResults(self):
    #test_set = mock_data.MockTestSet('cat_home')
    #params = {'cat_home_results': 'apple=0,banana=97,coconut=677'}
    #response = self.client.get('/', params, **mock_data.UNIT_TEST_UA)
    #self.assertEqual(200, response.status_code)

class TestBeacon(unittest.TestCase):

  def setUp(self):
    self.test_set = mock_data.MockTestSet()
    all_test_sets.AddTestSet(self.test_set)
    self.client = Client()

  def tearDown(self):
    all_test_sets.RemoveTestSet(self.test_set)

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
    csrf_token = self.client.get('/get_csrf').content
    params = {
      'category': self.test_set.category,
      'results': 'apple=1,banana=2,coconut=4',
      'csrf_token': csrf_token
    }
    response = self.client.get('/beacon', params, **mock_data.UNIT_TEST_UA)
    self.assertEqual(204, response.status_code)

    # Did a ResultParent get created?
    query = db.Query(result.ResultParent)
    query.filter('category =', self.test_set.category)
    result_parent = query.get()
    self.assertNotEqual(result_parent, None)

    result_times = result_parent.GetResultTimes()
    self.assertEqual(
        [('apple', 1, False), ('banana', 2, False), ('coconut', 4, False)],
        sorted((x.test, x.score, x.dirty) for x in result_times))


  def testBeaconWithChromeFrame(self):
    csrf_token = self.client.get('/get_csrf').content
    chrome_ua_string = ('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) '
        'AppleWebKit/530.1 (KHTML, like Gecko) Chrome/4.0.169.1 Safari/530.1')
    chrome_frame_ua_string = ('Mozilla/4.0 '
        '(compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; '
        'chromeframe; '
        '.NET CLR 2.0.50727; .NET CLR 1.1.4322; '
        '.NET CLR 3.0.04506.648; .NET CLR 3.5.21022)')
    unit_test_ua = mock_data.UNIT_TEST_UA
    unit_test_ua['HTTP_USER_AGENT'] = chrome_frame_ua_string
    params = {
      'category': self.test_set.category,
      'results': 'apple=0,banana=0,coconut=1000',
      'csrf_token': csrf_token,
      'js_ua': chrome_ua_string
    }
    response = self.client.get('/beacon', params, **unit_test_ua)
    self.assertEqual(204, response.status_code)

    # Did a ResultParent get created?
    query = db.Query(result.ResultParent)
    query.filter('category =', self.test_set.category)
    result_parent = query.get()
    self.assertNotEqual(result_parent, None)

    # What UA did the ResultParent get tied to? Chrome Frame (IE 7) I hope.
    user_agent = result_parent.user_agent
    self.assertEqual('Chrome Frame (IE 7) 4.0.169', user_agent.pretty())

    # Were ResultTimes created?
    result_times = result_parent.GetResultTimes()
    self.assertEqual(
        [('apple', 0, False), ('banana', 0, False), ('coconut', 1000, False)],
        sorted((x.test, x.score, x.dirty) for x in result_times))

  def testBeaconWithBogusTests(self):
    csrf_token = self.client.get('/get_csrf').content
    params = {
      'category': self.test_set.category,
      'results': 'testBogus=1,testVisibility=2',
      'csrf_token': csrf_token
    }
    response = self.client.get('/beacon', params, **mock_data.UNIT_TEST_UA)
    self.assertEqual(util.BAD_BEACON_MSG + 'ResultParent', response.content)

    # Did a ResultParent get created? Shouldn't have.
    query = db.Query(result.ResultParent)
    query.filter('category =', self.test_set.category)
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


class TestUtilFunctions(unittest.TestCase):
  def testCheckThrottleIpAddress(self):
    ip = mock_data.UNIT_TEST_UA['REMOTE_ADDR']
    ua_string = mock_data.UNIT_TEST_UA['HTTP_USER_AGENT']
    category = 'foo'
    for i in range(11):
      self.assertTrue(util.CheckThrottleIpAddress(ip, ua_string, category))

    # The next one should bomb.
    self.assertFalse(util.CheckThrottleIpAddress(ip, ua_string, category))

    # But a new category should work fine.
    self.assertTrue(util.CheckThrottleIpAddress(ip, ua_string, 'bar'))


class TestClearMemcache(unittest.TestCase):
  def setUp(self):
    self.client = Client()

  def testClearMemcacheRecentTests(self):
    memcache.set(util.RECENT_TESTS_MEMCACHE_KEY, 'foo')
    params = {'recent': 1}
    response = self.client.get('/clear_memcache', params)
    recent_tests = memcache.get(util.RECENT_TESTS_MEMCACHE_KEY)
    self.assertEqual(None, recent_tests)
    self.assertEqual(200, response.status_code)

if __name__ == '__main__':
  unittest.main()
