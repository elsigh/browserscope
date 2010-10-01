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

"""Test each of settings.CATEGORIES for the required fields."""

__author__ = 'elsigh@google.com (Lindsey Simon)'

import unittest
import random
import logging

from google.appengine.ext import db

from django.test.client import Client

from categories import all_test_sets

from models.result import *
import settings

import mock_data

class TestCategories(unittest.TestCase):

  def testCategoriesMatch(self):
    self.assertEqual(settings.CATEGORIES + settings.CATEGORIES_BETA,
                     [x.category for x in all_test_sets.GetAllTestSets()])

  def testCategoryNamesCapitalized(self):
    for test_set in all_test_sets.GetAllTestSets():
      # Make sure category name is a string and that it is capitalized.
      self.assertEqual(
          ' '.join(['%s%s' % (x[0].capitalize(), x[1:])
                    for x in test_set.category_name.split(' ')]),
          test_set.category_name)

  def testTestsDefinedWithRequireAttributes(self):
    for test_set in all_test_sets.GetAllTestSets():
      # Make sure category name is a string and that it is capitalized.
      self.assert_(len(test_set.tests))
      for test in test_set.tests:
        for attr in ('key', 'name', 'url', 'score_type', 'doc',
                     'min_value', 'max_value'):
          self.assert_(hasattr(test, attr))


class TestCategoriesHandlers(unittest.TestCase):

  def setUp(self):
    self.client = Client()

  def testTestPageWorks(self):
    for test_set in all_test_sets.GetAllTestSets():
      response = self.client.get('/%s/test' % test_set.category, {},
        **mock_data.UNIT_TEST_UA)
      self.assertEqual(200, response.status_code)

  def testAboutPageWorks(self):
    client = Client()
    for test_set in all_test_sets.GetAllTestSets():
      category = test_set.category
      logging.info('category: %s' % category)
      response = self.client.get('/%s/about' % category, {},
          **mock_data.UNIT_TEST_UA)
      self.assertEqual(200, response.status_code, 'No about for %s' % category)


class TestCanBeacon(unittest.TestCase):

  def setUp(self):
    self.client = Client()

  def testBeacon(self):
    for test_set in all_test_sets.GetAllTestSets():
      # Don't test our larger (and therefore serially slower) tests in the SDK.
      if len(test_set.tests) > 100:
        continue

      category = test_set.category
      csrf_token = self.client.get('/get_csrf').content
      # Constructs a reasonably random result set
      results = [
          '%s=%s' % (test.key, random.randrange(test.min_value, test.max_value))
          for test in test_set.tests]
      params = {
        'category': category,
        'results': ','.join(results),
        'csrf_token': csrf_token,
      }
      logging.info('params: %s' % params)
      response = self.client.get('/beacon', params, **mock_data.UNIT_TEST_UA)
      self.assertEqual('', response.content)
      self.assertEqual(204, response.status_code)

      # Did a ResultParent get created?
      query = db.Query(ResultParent)
      query.filter('category =', category)
      result_parent = query.get()
      self.assertNotEqual(result_parent, None)

      # Were the right number of ResultTimes created?
      result_times = result_parent.GetResultTimes()
      self.assertEqual(len(test_set.tests), len(result_times))
