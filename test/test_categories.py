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

"""Test each of settings.CATEGORIES for the required fields."""

__author__ = 'elsigh@google.com (Lindsey Simon)'

import unittest
import logging

from django.test.client import Client

from categories import all_test_sets
import settings

import mock_data

class TestCategories(unittest.TestCase):

  def testCategoriesMatch(self):
    self.assertEqual(settings.CATEGORIES,
                     [x.category for x in all_test_sets.GetTestSets()])

  def testCategoryNamesCapitalized(self):
    for test_set in all_test_sets.GetTestSets():
      # Make sure category name is a string and that it is capitalized.
      self.assertEqual(test_set.category_name.capitalize(),
                       test_set.category_name)

  def testTestsDefinedWithRequireAttributes(self):
    for test_set in all_test_sets.GetTestSets():
      # Make sure category name is a string and that it is capitalized.
      self.assert_(len(test_set.tests))
      for test in test_set.tests:
        for attr in ('key', 'name', 'url', 'score_type', 'doc',
                     'min_value', 'max_value'):
          self.assert_(hasattr(test, attr))

  def testSubnavHasDict(self):
    for test_set in all_test_sets.GetTestSets():
      self.assert_(test_set.subnav.items())

  def testHomeIntroductionDefined(self):
    for test_set in all_test_sets.GetTestSets():
      self.assert_(test_set.home_intro)

class TestCategoriesHandlers(unittest.TestCase):

  def setUp(self):
    self.client = Client()

  def testTestPageWorks(self):
    for category in settings.CATEGORIES:
      response = self.client.get('/%s/test' % category, {},
        **mock_data.UNIT_TEST_UA)
      self.assertEqual(200, response.status_code)

  def testAboutPageWorks(self):
    client = Client()
    for category in settings.CATEGORIES:
      response = self.client.get('/%s/' % category, {},
        **mock_data.UNIT_TEST_UA)
      self.assertEqual(200, response.status_code)

      response = self.client.get('/%s/about' % category, {},
        **mock_data.UNIT_TEST_UA)
      self.assertEqual(200, response.status_code)
