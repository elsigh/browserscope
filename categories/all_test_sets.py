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

"""Collect all tests."""

__author__ = 'slamm@google.com (Stephen Lamm)'


import logging
import re
import settings

import models.user_test

ALL_CATEGORIES = settings.CATEGORIES + settings.CATEGORIES_BETA
ALL_TEST_SETS = []  # lazy loaded to avoid import loop
CATEGORY_TEST_SETS = {}


def GetAllTestSets():
  if not ALL_TEST_SETS:
    _InitializeLists()
  return ALL_TEST_SETS


def GetVisibleTestSets(forced_categories=None):
  if not ALL_TEST_SETS:
    _InitializeLists()
  visible_categories = settings.CATEGORIES + (forced_categories or [])
  visible_test_sets = [
      ts for ts in ALL_TEST_SETS
      if ts.category in visible_categories or settings.BUILD == 'development']
  return visible_test_sets


def GetTestSet(category):
  # First check to see if this is a user-api test set.
  user_test_set = models.user_test.Test.get_test_set_from_category(category)
  if user_test_set:
    return user_test_set

  if not CATEGORY_TEST_SETS:
    _InitializeLists()
  if settings.BUILD == 'development' and category not in CATEGORY_TEST_SETS:
    try:
      AddTestSet(_ImportTestSet(category))
    except ImportError:
      return None
  return CATEGORY_TEST_SETS.get(category, None)

def AddTestSet(test_set):
  """Add a test_set."""
  global ALL_CATEGORIES
  global ALL_TEST_SETS
  global CATEGORY_TEST_SETS
  ALL_CATEGORIES.append(test_set.category)
  ALL_TEST_SETS.append(test_set)
  CATEGORY_TEST_SETS[test_set.category] = test_set

def RemoveTestSet(test_set):
  """Remove a test_set (for unit tests)."""
  global ALL_CATEGORIES
  global ALL_TEST_SETS
  global CATEGORY_TEST_SETS
  ALL_CATEGORIES.remove(test_set.category)
  ALL_TEST_SETS.remove(test_set)
  del CATEGORY_TEST_SETS[test_set.category]

def _InitializeLists():
  global ALL_TEST_SETS
  global CATEGORY_TEST_SETS
  ALL_TEST_SETS = [_ImportTestSet(c) for c in ALL_CATEGORIES]
  CATEGORY_TEST_SETS = dict(zip(ALL_CATEGORIES, ALL_TEST_SETS))


def _ImportTestSet(category):
  """Modules that define tests must add them."""
  logging.debug('Import category test_set: %s', category)
  return __import__('categories.%s.test_set' % category,
                    globals(), locals(), [category]).TEST_SET
