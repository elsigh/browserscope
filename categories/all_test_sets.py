#!/usr/bin/python2.4
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


import settings


def GetTestSets():
  for category in settings.CATEGORIES:
    yield GetTestSet(category)


CATEGORY_TEST_SETS = {}
def GetTestSet(category):
  if category not in CATEGORY_TEST_SETS:
    AddTestSet(_ImportTestSet(category))
  return CATEGORY_TEST_SETS[category]

def HasTestSet(category):
  try:
    GetTestSet(category)
  except ImportError:
    return False
  return True

def AddTestSet(test_set):
  """Add a test_set."""
  global CATEGORY_TEST_SETS
  CATEGORY_TEST_SETS[test_set.category] = test_set


def _ImportTestSet(category):
  """Modules that define tests must add them."""
  return __import__('categories.%s.test_set' % category,
                    globals(), locals(), [category]).TEST_SET
