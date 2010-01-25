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

from google.appengine.api import memcache
from google.appengine.ext import db

from django.test.client import Client
from base import cron
from base import util
from models.result import ResultParent
from models.result import ResultTime
from models.user_agent import UserAgent

import mock_data

class TestUpdateRecentTests(unittest.TestCase):
  def setUp(self):
    self.client = Client()

  def tearDown(self):
    db.delete(ResultParent.all(keys_only=True).fetch(1000))
    db.delete(ResultTime.all(keys_only=True).fetch(1000))
    db.delete(UserAgent.all(keys_only=True).fetch(1000))
    memcache.flush_all()

  def testRecentTestsBasic(self):
    test_set = mock_data.MockTestSet()
    result_parents = []
    for scores in ((1, 4, 50), (1, 1, 20), (0, 2, 30)):
      result = ResultParent.AddResult(
          test_set, '1.2.2.5', mock_data.GetUserAgentString('Firefox 3.5'),
          'apple=%s,banana=%s,coconut=%s' % scores)
      result_parents.append(result)

    params = {}
    response = self.client.get('/cron/update_recent_tests', params)

    recent_tests = memcache.get(key=util.RECENT_TESTS_MEMCACHE_KEY)



if __name__ == '__main__':
  unittest.main()
