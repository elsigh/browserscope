#!/usr/bin/python2.5
# -*- coding: utf-8 -*-
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
import logging

from django.test.client import Client

from categories.reflow import test_set

class ReflowTestTest(unittest.TestCase):

  def setUp(self):
    self.test_set = test_set.TEST_SET

  def testScoreAndDisplayValueNone(self):
    self.assertEqual((90, ''), self.test_set.GetTestScoreAndDisplayValue(
        'testVisibility', {}))
    self.assertEqual((90, ''), self.test_set.GetTestScoreAndDisplayValue(
        'testVisibility', {'testVisibility': None}))
    self.assertEqual((90, ''), self.test_set.GetTestScoreAndDisplayValue(
        'testVisibility', {'testVisibility': ''}))

  def testScoreAndDisplayValueZero(self):
    self.assertEqual((100, '0X'), self.test_set.GetTestScoreAndDisplayValue(
        'testVisibility', {'testVisibility': 0}))

  def testScoreAndDisplayValueVisibility(self):
    self.assertEqual((97, '¼X'), self.test_set.GetTestScoreAndDisplayValue(
        'testVisibility', {'testVisibility': 20}))
    self.assertEqual((95, '½X'), self.test_set.GetTestScoreAndDisplayValue(
        'testVisibility', {'testVisibility': 40}))
    self.assertEqual((90, '1X'), self.test_set.GetTestScoreAndDisplayValue(
        'testVisibility', {'testVisibility': 100}))
    self.assertEqual((80, '2X'), self.test_set.GetTestScoreAndDisplayValue(
        'testVisibility', {'testVisibility': 150}))
    self.assertEqual((80, '2X'), self.test_set.GetTestScoreAndDisplayValue(
        'testVisibility', {'testVisibility': 180}))
    self.assertEqual((60, '3X'), self.test_set.GetTestScoreAndDisplayValue(
        'testVisibility', {'testVisibility': 200}))

  def testAdjustResults(self):
    reflow_test_set = test_set.TEST_SET
    results = {
      test_set.BASELINE_TEST_NAME: {'raw_score': 100},
      'testTwo': {'raw_score': 50},
      'testThree': {'raw_score': 150},
      'testThree': {'raw_score': 200},
      }
    parsed_results = reflow_test_set.AdjustResults(results)
    expected_results = {
      test_set.BASELINE_TEST_NAME: {'expando': 100, 'raw_score': 100},
      'testTwo': {'expando': 50, 'raw_score': 50},
      'testThree': {'expando': 150, 'raw_score': 150},
      'testThree': {'expando': 200, 'raw_score': 200},
      }
    self.assertTrue(expected_results == parsed_results)

    results = {
      test_set.BASELINE_TEST_NAME: {'raw_score': 400},
      'testTwo': {'raw_score': 300},
      'testThree': {'raw_score': 276},
      'testThree': {'raw_score': 149},
      }
    parsed_results = reflow_test_set.AdjustResults(results)
    expected_results = {
      test_set.BASELINE_TEST_NAME: {'expando': 400, 'raw_score': 100},
      'testTwo': {'expando': 300, 'raw_score': 75},
      'testThree': {'expando': 276, 'raw_score': 69},
      'testThree': {'expando': 149, 'raw_score': 37},
      }
    self.assertTrue(expected_results == parsed_results)



if __name__ == '__main__':
  unittest.main()
