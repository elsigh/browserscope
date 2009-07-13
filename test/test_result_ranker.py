#!/usr/bin/python2.4
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

"""Result ranker Unit Tests."""

__author__ = 'slamm@google.com (Stephen Lamm)'

import unittest
import logging

from models import result_ranker

class RankListRankerTest(unittest.TestCase):

  def testKeyName(self):
    key_name = result_ranker.RankListRanker.KeyName(
        'category', 'test', 'user_agent_version')
    self.assertEqual('category_test_user_agent_version', key_name)

  def testKeyName(self):
    key_name = result_ranker.RankListRanker.KeyName(
        'category', 'test', 'user_agent_version',
        ['param1=val1', 'param2=val2', 'param3=val3'])
    self.assertEqual(
        'category_test_user_agent_version_1c565ba4056b84201ed4fe4c4b6b2e42',
        key_name)
