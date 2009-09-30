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

import mock_data
import settings

from django.test.client import Client
from django.utils import simplejson
from google.appengine.ext import db
from models.result import ResultParent
from models.result import ResultTime
from models.user_agent import UserAgent
from models.user_agent import UserAgentGroup

from base import admin

USER_AGENT_STRINGS = {
    'Firefox 3.0.6': ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) '
                      'Gecko/2009011912 Firefox/3.0.6'),
    'Firefox 3.5': ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) '
                    'Gecko/2009011912 Firefox/3.5'),
    'Firefox 3.0.9': ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) '
                      'Gecko/2009011912 Firefox/3.0.9'),
    }

class TestConfirmUa(unittest.TestCase):
  def setUp(self):
    self.client = Client()
    ua_string = ('Mozilla/5.0 (X11 U Linux armv6l de-DE rv:1.9a6pre) '
                 'Gecko/20080606 '
                 'Firefox/3.0a1 Tablet browser 0.3.7 '
                 'RX-34+RX-44+RX-48_DIABLO_4.2008.23-14')
    self.ua = UserAgent.factory(ua_string)

  def testConfirmBasic(self):
    params = {
        'submit': 1,
        'ac_%s' % self.ua.key(): 'confirm',
        'cht_%s' % self.ua.key(): '',
        'csrf_token': self.client.get('/get_csrf').content,
        }
    response = self.client.get('/admin/confirm-ua', params)
    self.assertEqual(200, response.status_code)
    self.assertTrue(self.ua.get(self.ua.key()).confirmed)


class TestDataDump(unittest.TestCase):
  def setUp(self):
    self.client = Client()

  def tearDown(self):
    db.delete(ResultParent.all(keys_only=True).fetch(1000))
    db.delete(ResultTime.all(keys_only=True).fetch(1000))
    db.delete(UserAgent.all(keys_only=True).fetch(1000))
    db.delete(UserAgentGroup.all(keys_only=True).fetch(1000))

  def testNoParamsGivesError(self):
    params = {}
    response = self.client.get('/admin/data_dump', params)
    self.assertEqual(400, response.status_code)

  def testBookmarkAndCreatedGivesError(self):
    params = {'bookmark': 'foo', 'created': '2009-09-09 09:09:09'}
    response = self.client.get('/admin/data_dump', params)
    self.assertEqual(400, response.status_code)

  def testNoBookmarkOrCreatedResultParent(self):
    test_set = mock_data.MockTestSet('category')
    for scores in ((10, 0), (20, 1), (30, 2), (50, 3), (50, 4)):
      result = ResultParent.AddResult(
          test_set, '1.2.2.5', mock_data.GetUserAgentString(),
          'testDisplay=%s,testVisibility=%s' % scores)
    params = {'model': 'ResultParent'}
    response = self.client.get('/admin/data_dump', params)
    self.assertEqual(200, response.status_code)
    response_params = simplejson.loads(response.content)
    self.assertEqual(None, response_params['bookmark'])
    self.assertEqual(15, len(response_params['data'])) # 5 parents, 10 times

  def testNoBookmarkOrCreatedUserAgent(self):
    test_set = mock_data.MockTestSet('category')
    for scores in ((10, 0), (20, 1)):
      result = ResultParent.AddResult(
          test_set, '1.2.2.5', mock_data.GetUserAgentString(),
          'testDisplay=%s,testVisibility=%s' % scores)
    params = {'model': 'UserAgent'}
    response = self.client.get('/admin/data_dump', params)
    self.assertEqual(200, response.status_code)
    response_params = simplejson.loads(response.content)
    self.assertEqual(None, response_params['bookmark'])
    self.assertEqual(1, len(response_params['data']))
    self.assertEqual('Firefox', response_params['data'][0]['family'])

  def testCreated(self):
    test_set = mock_data.MockTestSet('category')
    created_base = datetime.datetime(2009, 9, 9, 9, 9, 0)
    for scores in ((10, 0), (20, 1)):
      ip = '1.2.2.%s' % scores[0]
      result = ResultParent.AddResult(
          test_set, ip, mock_data.GetUserAgentString(),
          'testDisplay=%s,testVisibility=%s' % scores,
          created=created_base + datetime.timedelta(seconds=scores[0]))
    params = {
          'model': 'ResultParent',
          'created': created_base + datetime.timedelta(seconds=15),
          }
    response = self.client.get('/admin/data_dump', params)
    self.assertEqual(200, response.status_code)
    response_params = simplejson.loads(response.content)
    self.assertEqual(None, response_params['bookmark'])
    self.assertEqual(3, len(response_params['data']))  # parent + 2 times
    self.assertEqual('1.2.2.20', response_params['data'][0]['ip'])
