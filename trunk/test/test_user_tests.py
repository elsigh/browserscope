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
import unittest


from django.test.client import Client

from google.appengine.api import memcache
from google.appengine.api import users
from google.appengine.ext import db

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
