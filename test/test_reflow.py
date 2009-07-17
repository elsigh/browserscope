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
import logging

from django.test.client import Client

from controllers import reflow_test_set

class ReflowTestTest(unittest.TestCase):

  #def setUp(self):
    # Every test needs a client.
    #self.client = Client()

  def testScoreAndDisplayValueNone(self):
    test = reflow_test_set.ReflowTest('testVisibility', 'zer', 'Zero Test')
    score, display = test.GetScoreAndDisplayValue(None)
    self.assertEqual((90, ''), (score, display))

  def testScoreAndDisplayValueZero(self):
    test = reflow_test_set.ReflowTest('testVisibility', 'zer', 'Zero Test')
    score, display = test.GetScoreAndDisplayValue(0)
    self.assertEqual((100, '~0X'), (score, display))

  def testScoreAndDisplayValueVisibility(self):
    test = reflow_test_set.ReflowTest('testVisibility', 'da up', 'da up Test')
    score, display = test.GetScoreAndDisplayValue(20)
    self.assertEqual((100, '~0X'), (score, display))
    score, display = test.GetScoreAndDisplayValue(40)
    self.assertEqual((90, '1X'), (score, display))
    score, display = test.GetScoreAndDisplayValue(30)
    self.assertEqual((90, '1X'), (score, display))
    score, display = test.GetScoreAndDisplayValue(50)
    self.assertEqual((90, '1X'), (score, display))
    score, display = test.GetScoreAndDisplayValue(60)
    self.assertEqual((80, '2X'), (score, display))
    score, display = test.GetScoreAndDisplayValue(100)
    self.assertEqual((80, '2X'), (score, display))
    score, display = test.GetScoreAndDisplayValue(150)
    self.assertEqual((70, '3X'), (score, display))
    score, display = test.GetScoreAndDisplayValue(180)
    self.assertEqual((60, '4X'), (score, display))
    score, display = test.GetScoreAndDisplayValue(200)
    self.assertEqual((60, '4X'), (score, display))


if __name__ == '__main__':
  unittest.main()
