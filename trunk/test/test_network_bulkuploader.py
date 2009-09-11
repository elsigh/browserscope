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

"""Test categories.network.bulkloader."""

__author__ = 'slamm@google.com (Stephen Lamm)'


import logging
import unittest

import mock_data

from django.test.client import Client
from django.utils import simplejson

# from google.appengine.ext import db

# from models import result_ranker
# from models.result import ResultParent
# from models.result import ResultTime

from categories.network import bulkloader

USER_AGENT_STRINGS = {
    'Firefox 3.0.6': ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) '
                      'Gecko/2009011912 Firefox/3.0.6'),
    'Firefox 3.5': ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) '
                    'Gecko/2009011912 Firefox/3.5'),
    'Firefox 3.0.9': ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) '
                      'Gecko/2009011912 Firefox/3.0.9'),
    }

class TestResultLoader(unittest.TestCase):
  def setUp(self):
    self.old_test_set = bulkloader.TEST_SET
    bulkloader.TEST_SET = mock_data.MockTestSet('cagetory')
    self.client = Client()

  def tearDown(self):
    bulkloader.TEST_SET = self.old_test_set

  def testEmptyUpload(self):
    results = [
        [111, '12.1.1.1', USER_AGENT_STRINGS['Firefox 3.5'], 1234455,
         [('testDisplay', 100), ('testVisibility', 2)]],
        [222, '12.2.2.2', USER_AGENT_STRINGS['Firefox 3.0.9'], 1234456,
         [('testDisplay', 200), ('testVisibility', 1)]],
        ]
    results = []
    raw_post_data = simplejson.dumps(results)
    response = self.client.post('/network/loader', raw_post_data,
                                content_type='application/jsonrequest')
    self.assertEqual(200, response.status_code)

    last_loader_id = simplejson.loads(response.content)
    self.assertEqual(0, last_loader_id)

  def testEmptyBasic(self):
    results = [
        [111, '12.1.1.1', USER_AGENT_STRINGS['Firefox 3.5'], 1234455,
         [('testDisplay', 100), ('testVisibility', 2)]],
        [222, '12.2.2.2', USER_AGENT_STRINGS['Firefox 3.0.9'], 1234456,
         [('testDisplay', 200), ('testVisibility', 1)]],
        ]
    raw_post_data = simplejson.dumps(results)
    response = self.client.post('/network/loader', raw_post_data,
                                content_type='application/jsonrequest')
    self.assertEqual(200, response.status_code)
    last_loader_id = simplejson.loads(response.content)
    self.assertEqual(222, last_loader_id)

    results = [
        [333, '12.1.1.1', USER_AGENT_STRINGS['Firefox 3.0.6'], 1234666,
         [('testDisplay', 150), ('testVisibility', 12)]],
        [444, '12.2.2.2', USER_AGENT_STRINGS['Firefox 3.5'], 1234777,
         [('testDisplay', 250), ('testVisibility', 11)]],
        ]
    raw_post_data = simplejson.dumps(results)
    response = self.client.post('/network/loader', raw_post_data,
                                content_type='application/jsonrequest')
    self.assertEqual(200, response.status_code)
    last_loader_id = simplejson.loads(response.content)
    self.assertEqual(444, last_loader_id)
