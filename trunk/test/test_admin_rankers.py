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


import time
import logging
import unittest

import mock_data
import settings

from django.test.client import Client
from django.utils import simplejson
from google.appengine.api import datastore_types
from google.appengine.ext import db

from models import result_ranker
from third_party import mox

from base import admin_rankers

class TestUploadRankers(unittest.TestCase):
  """Test uploading rankers"""

  def setUp(self):
    self.test_set = mock_data.MockTestSet()

    self.mox = mox.Mox()
    self.mox.StubOutWithMock(time, 'clock')
    self.mox.StubOutWithMock(result_ranker, 'GetOrCreateRankers')
    self.apple_test = self.test_set.GetTest('apple')
    self.coconut_test = self.test_set.GetTest('coconut')
    self.apple_ranker = self.mox.CreateMock(result_ranker.CountRanker)
    self.apple_ranker_key = self.mox.CreateMock(datastore_types.Key)
    self.coconut_ranker = self.mox.CreateMock(result_ranker.LastNRanker)
    self.coconut_ranker_key = self.mox.CreateMock(datastore_types.Key)

    self.client = Client()

  def tearDown(self):
    self.mox.UnsetStubs()

  def testBasic(self):
    test_key_browsers = (
        ('apple', 'Firefox 3.0'),
        ('coconut', 'Firefox 3.0'),
        )
    ranker_values = (
        (1, 5, '2|3'),
        (101, 7, '101|99|101|2|988|3|101'),
        )
    params = {
        'category': self.test_set.category,
        'test_key_browsers_json': simplejson.dumps(test_key_browsers),
        'ranker_values_json': simplejson.dumps(ranker_values),
        'time_limit': 10,
        }
    time.clock().AndReturn(0)
    test_browsers = [
        (self.apple_test, 'Firefox 3.0'),
        (self.coconut_test, 'Firefox 3.0'),
        ]
    result_ranker.GetOrCreateRankers(test_browsers, None).AndReturn(
        [self.apple_ranker, self.coconut_ranker])
    time.clock().AndReturn(0.5)
    self.apple_ranker.GetMedianAndNumScores().AndReturn((1, 2))
    self.apple_ranker.SetValues([2, 3], 5)
    time.clock().AndReturn(1)  # under timelimit
    self.coconut_ranker.GetMedianAndNumScores().AndReturn((50, 5))
    self.coconut_ranker.SetValues([101, 99, 101, 2, 988, 3, 101], 7)

    self.mox.ReplayAll()
    response = self.client.get('/admin/rankers/upload', params)
    self.mox.VerifyAll()
    self.assertEqual(simplejson.dumps({}), response.content)
    self.assertEqual(200, response.status_code)


  def testOverTimeLimit(self):
    test_key_browsers = (
        ('apple', 'Firefox 3.0'),
        ('coconut', 'Firefox 3.0'),
        )
    ranker_values = (
        (1, 5, '2|3'),
        (101, 7, '101|99|101|2|988|3|101'),
        )
    params = {
        'category': self.test_set.category,
        'test_key_browsers_json': simplejson.dumps(test_key_browsers),
        'ranker_values_json': simplejson.dumps(ranker_values),
        'time_limit': 10,
        }

    time.clock().AndReturn(0)
    test_browsers = [
        (self.apple_test, 'Firefox 3.0'),
        (self.coconut_test, 'Firefox 3.0'),
        ]
    result_ranker.GetOrCreateRankers(test_browsers, None).AndReturn(
        [self.apple_ranker, self.coconut_ranker])

    time.clock().AndReturn(0.5)
    self.apple_ranker.GetMedianAndNumScores().AndReturn((1, 2))
    self.apple_ranker.SetValues([2, 3], 5)
    time.clock().AndReturn(10.1)  # over timelimit
    self.mox.ReplayAll()
    response = self.client.get('/admin/rankers/upload', params)
    self.mox.VerifyAll()
    expected_response_content = simplejson.dumps({
        'message': 'Over time limit',
        })
    self.assertEqual(expected_response_content, response.content)
    self.assertEqual(200, response.status_code)


  def testSkipUnchangedValues(self):
    test_key_browsers = (
        ('apple', 'Firefox 3.0'),
        ('coconut', 'Firefox 3.0'),
        )
    ranker_values = (
        (1, 5, '2|3'),
        (101, 7, '101|99|101|2|988|3|101'),
        )
    params = {
        'category': self.test_set.category,
        'test_key_browsers_json': simplejson.dumps(test_key_browsers),
        'ranker_values_json': simplejson.dumps(ranker_values),
        'time_limit': 10,
        }
    time.clock().AndReturn(0)
    test_browsers = [
        (self.apple_test, 'Firefox 3.0'),
        (self.coconut_test, 'Firefox 3.0'),
        ]
    result_ranker.GetOrCreateRankers(test_browsers, None).AndReturn(
        [self.apple_ranker, self.coconut_ranker])
    time.clock().AndReturn(0.5)
    self.apple_ranker.GetMedianAndNumScores().AndReturn((1, 5))
    self.apple_ranker.key().AndReturn(self.apple_ranker_key)
    self.apple_ranker_key.name().AndReturn('appl')
    time.clock().AndReturn(1)
    self.coconut_ranker.GetMedianAndNumScores().AndReturn((101, 7))
    self.coconut_ranker.key().AndReturn(self.coconut_ranker_key)
    self.coconut_ranker_key.name().AndReturn('coco')
    self.mox.ReplayAll()
    response = self.client.get('/admin/rankers/upload', params)
    logging.info('response: %s', response)
    self.mox.VerifyAll()
    self.assertEqual('{}', response.content)
    self.assertEqual(200, response.status_code)
