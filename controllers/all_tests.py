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


from settings import *

CATEGORY_TESTS = {}
def GetTests(category):
  if category not in CATEGORY_TESTS:
    _AddTests(category)
  return CATEGORY_TESTS[category]

ALL_TESTS = {}
def GetTest(category, test_key):
  if category, test_key not in ALL_TESTS:
    _AddTests(category)
  return ALL_TESTS[(category, test_key)]

def _AddTests(category):
  """Modules that define tests must add them."""
  mod = __import__(
      '%s.%s' % (CONTROLLERS_MODULE, category), globals(), locals(), [category])
    global CATEGORY_TESTS
    CATEGORY_TESTS[category] = mod.TESTS
    global ALL_TESTS
    ALL_TESTS.update(((category, test.key), test) for test in mod.TESTS)
