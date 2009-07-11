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
from settings import *


REQUIRED = ['CATEGORY', 'CATEGORY_NAME', 'TESTS',
            'CustomTestsFunction', 'HOME_INTRO']

class TestCategories(unittest.TestCase):


  def test_categories(self):

    passed = []
    failed = []
    # Creates a list of tuples categories and their ui names.
    for category in CATEGORIES:
      _mod = __import__('%s.%s' % (CONTROLLERS_MODULE, category),
                        globals(), locals(), [category])
      for required in REQUIRED:
        value = hasattr(_mod, required)
        if value:
          passed.append((required, value))
        else:
          failed.append((category, required))

    if len(failed) > 0:
      for category, required in failed:
        raise AssertionError('%s.%s has no value' % (category, required))
