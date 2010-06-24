#!/usr/bin/python2.5
#
# Copyright 2009 Google Inc.
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

"""Test admin_rankers."""

__author__ = 'slamm@google.com (Stephen Lamm)'


import datetime
import logging
import re
import unittest

from django.test.client import Client

from google.appengine.api import memcache
from google.appengine.api import users
from google.appengine.ext import db

from base import util

from categories import all_test_sets

from models import result_stats
import models.user_test

import mock_data
import settings
from third_party import mox


class TestModels(unittest.TestCase):

  def testUser(self):
    current_user = users.get_current_user()
    u = models.user_test.User.get_or_insert(current_user.user_id())
    u.email = current_user.email()
    u.save()

    user_q = models.user_test.User.get_by_key_name(current_user.user_id())
    self.assertTrue(user_q.email, current_user.email())

  def testGetTestSetFromResultString(self):
    current_user = users.get_current_user()
    u = models.user_test.User.get_or_insert(current_user.user_id())
    test = models.user_test.Test(user=u, name='Fake Test',
                                 url='http://fakeurl.com/test.html',
                                 description='stuff')
    test.save()

    results_str = 'test_1=0,test_2=1'
    test_set_category = 'usertest_%s' % test.key()
    test_set = models.user_test.Test.get_test_set_from_results_str(
        test_set_category, results_str)
    self.assertTrue(test_set != None)
    self.assertEqual(test_set.category, test_set_category)
    self.assertEqual(len(test_set.tests), 2)
    self.assertEqual('test_1', test_set.tests[0].key)
    self.assertEqual('test_2', test_set.tests[1].key)


class TestHandlers(unittest.TestCase):

  def setUp(self):
    self.client = Client()

  def testHowto(self):
    response = self.client.get('/user/tests/howto')
    self.assertEqual(200, response.status_code)

  def testGetSettings(self):
    response = self.client.get('/user/settings')
    self.assertEqual(200, response.status_code)

  def testCreateTestBad(self):
    csrf_token = self.client.get('/get_csrf').content
    data = {
      'name': '',
      'url': 'http://fakeurl.com/test.html',
      'description': 'whatever',
      'csrf_token': csrf_token,
    }
    response = self.client.post('/user/tests/create', data)
    self.assertEqual(200, response.status_code)

    tests = db.Query(models.user_test.Test)
    self.assertEquals(0, tests.count())

  def testCreateTestOk(self):
    csrf_token = self.client.get('/get_csrf').content
    data = {
      'name': 'FakeTest',
      'url': 'http://fakeurl.com/test.html',
      'description': 'whatever',
      'csrf_token': csrf_token,
    }
    response = self.client.post('/user/tests/create', data)
    # Should redirect to /user/settings when all goes well.
    self.assertEqual(302, response.status_code)

    tests = db.Query(models.user_test.Test)
    self.assertEquals(1, tests.count())

  def testUserBeacon(self):
    current_user = users.get_current_user()
    u = models.user_test.User.get_or_insert(current_user.user_id())
    u.email = current_user.email()
    u.save()

    test = models.user_test.Test(user=u, name='Fake Test',
                                 url='http://fakeurl.com/test.html',
                                 description='stuff')
    test.save()

    response = self.client.get('/user/beacon/%s' % test.key())
    self.assertEquals('text/javascript', response['Content-type'])

    # There should be no callback setTimeout in the page.
    self.assertFalse(re.search('window.setTimeout', response.content))

    # Now test a beacon with a callback specified.
    # This is a regex test ensuring it's there in a setTimeout.
    params = {'callback': 'MyFunction'}
    response = self.client.get('/user/beacon/%s' % test.key(), params)
    self.assertEquals('text/javascript', response['Content-type'])
    self.assertTrue(re.search('window.setTimeout\(%s' % params['callback'],
        response.content))


  def testBeaconWithSandboxId(self):
    current_user = users.get_current_user()
    u = models.user_test.User.get_or_insert(current_user.user_id())
    u.email = current_user.email()
    u.save()

    test = models.user_test.Test(user=u, name='Fake Test SandboxID',
                                 url='http://fakeurl.com/test.html',
                                 description='stuff',
                                 sandboxid='sandbox-id')
    test.save()

    params = {
      'category': test.get_memcache_keyname(),
      'results': 'apple=1,banana=2,coconut=4',
    }
    # Run 10 times.
    for i in range(11):
      csrf_token = self.client.get('/get_csrf').content
      params['csrf_token'] = csrf_token
      response = self.client.get('/beacon', params, **mock_data.UNIT_TEST_UA)
      self.assertEqual(204, response.status_code)

    # The 11th should bomb due to IP throttling.
    csrf_token = self.client.get('/get_csrf').content
    params['csrf_token'] = csrf_token
    response = self.client.get('/beacon', params, **mock_data.UNIT_TEST_UA)
    self.assertEqual(util.BAD_BEACON_MSG + 'IP', response.content)

    # But we should be able to run 11 beacons (i.e. 10 + 1) with a sandboxid.
    params['sandboxid'] = test.sandboxid
    # Run 11 times
    for i in range(12):
      csrf_token = self.client.get('/get_csrf').content
      params['csrf_token'] = csrf_token
      response = self.client.get('/beacon', params, **mock_data.UNIT_TEST_UA)
      self.assertEqual(204, response.status_code)


class TestAliasedUserTest(unittest.TestCase):
  """Using HTML5 as an example."""

  def setUp(self):
    self.client = Client()

    current_user = users.get_current_user()
    u = models.user_test.User.get_or_insert(current_user.user_id())
    u.email = current_user.email()
    u.save()

    test = models.user_test.Test(user=u, name='Fake Test',
                                 url='http://fakeurl.com/test.html',
                                 description='stuff')
    # Because GAEUnit won't run the deferred taskqueue properly.
    test.test_keys = ['apple', 'coconut', 'banana']
    test.save()
    self.test = test

    self.test_set = mock_data.MockUserTestSet()
    self.test_set.user_test_category = test.get_memcache_keyname()
    #all_test_sets.AddTestSet(self.test_set)

    params = {
      'category': self.test.get_memcache_keyname(),
      'results': 'apple=1,banana=2,coconut=4',
    }
    csrf_token = self.client.get('/get_csrf').content
    params['csrf_token'] = csrf_token
    response = self.client.get('/beacon', params, **mock_data.UNIT_TEST_UA)
    self.assertEqual(204, response.status_code)

  def testResultStats(self):
    # These stats do not run through GetTestScoreAndDisplayValue, etc..
    stats = {
      'Other': {
         'summary_display': '',
         'total_runs': 1,
         'summary_score': 0,
         'results': {
            'apple': {'score': 0, 'raw_score': 1, 'display': '1'},
            'banana': {'score': 0, 'raw_score': 2, 'display': '2'},
            'coconut': {'score': 0, 'raw_score': 4, 'display': '4'},
         }
      },
      'total_runs': 1,
    }
    # First get results for the UserTest test_set
    test_set = self.test.get_test_set_from_test_keys(
        ['apple', 'banana', 'coconut'])
    results = result_stats.CategoryStatsManager.GetStats(
        test_set, browsers=('Other',),
        test_keys=['apple', 'banana', 'coconut'], use_memcache=False)
    self.assertEqual(stats, results)

    # Our MockTestSet has GetTestScoreAndDisplayValue &
    # GetRowScoreAndDisplayValue
    stats = {
      'Other': {
        'summary_display': '7',
        'total_runs': 1,
        'summary_score': 14,
        'results': {
          'apple': {'score': 2, 'raw_score': 1, 'display': 'd:2'},
          'banana': {'score': 4, 'raw_score': 2, 'display': 'd:4'},
          'coconut': {'score': 8, 'raw_score': 4, 'display': 'd:8'},
        }
      },
      'total_runs': 1,
    }

    # Now see if the test_set with user_test_category gets the same.
    results = result_stats.CategoryStatsManager.GetStats(
        self.test_set, browsers=('Other',),
        test_keys=['apple', 'banana', 'coconut'], use_memcache=False)
    self.assertEqual(stats, results)
