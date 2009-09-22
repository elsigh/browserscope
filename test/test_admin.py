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


import logging
import unittest

import mock_data
import settings

from django.test.client import Client
from google.appengine.ext import db
from models.user_agent import UserAgent

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
