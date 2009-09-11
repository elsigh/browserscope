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

"""Test test_set_base."""

__author__ = 'slamm@google.com (Stephen Lamm)'


import unittest

import mock_data
from categories import test_set_base

class TestParseResults(unittest.TestCase):
  def testValidResultsStringGivesExpectedResults(self):
    results_str = 'testDisplay=5,testVisibility=10'
    expected_results = [('testDisplay', 5), ('testVisibility', 10)]
    test_set = mock_data.MockTestSet('cat1')
    results = test_set.ParseResults(results_str)
    # Flatten the results because assertEqual cannot handle it otherwise.
    actual_results = [(x['key'], x['score']) for x in results]
    self.assertEqual(expected_results, actual_results)


  def testNonIntegerValueRaises(self):
    results_str = 'testDisplay=5,testVisibility=10.00001'
    test_set = mock_data.MockTestSet('cat1')
    self.assertRaises(test_set_base.ParseResultsValueError,
                      test_set.ParseResults, results_str)

  def testMissingKeyRaises(self):
    results_str = 'testDisplay=5'
    test_set = mock_data.MockTestSet('cat1')
    self.assertRaises(test_set_base.ParseResultsKeyError,
                      test_set.ParseResults, results_str)

  def testKeyTypoRaises(self):
    results_str = 'testDisplay=5,TeStvIsIbIlItY=10'
    test_set = mock_data.MockTestSet('cat1')
    self.assertRaises(test_set_base.ParseResultsKeyError,
                      test_set.ParseResults, results_str)
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

"""Test test_set_base."""

__author__ = 'slamm@google.com (Stephen Lamm)'


import unittest

import mock_data
from categories import test_set_base

class TestParseResults(unittest.TestCase):
  def testValidResultsStringGivesExpectedResults(self):
    results_str = 'testDisplay=5,testVisibility=10'
    expected_results = [('testDisplay', 5), ('testVisibility', 10)]
    test_set = mock_data.MockTestSet('cat1')
    results = test_set.ParseResults(results_str)
    # Flatten the results because assertEqual cannot handle it otherwise.
    actual_results = [(x['key'], x['score']) for x in results]
    self.assertEqual(expected_results, actual_results)


  def testNonIntegerValueRaises(self):
    results_str = 'testDisplay=5,testVisibility=10.00001'
    test_set = mock_data.MockTestSet('cat1')
    self.assertRaises(test_set_base.ParseResultsValueError,
                      test_set.ParseResults, results_str)

  def testMissingKeyRaises(self):
    results_str = 'testDisplay=5'
    test_set = mock_data.MockTestSet('cat1')
    self.assertRaises(test_set_base.ParseResultsKeyError,
                      test_set.ParseResults, results_str)

  def testKeyTypoRaises(self):
    results_str = 'testDisplay=5,TeStvIsIbIlItY=10'
    test_set = mock_data.MockTestSet('cat1')
    self.assertRaises(test_set_base.ParseResultsKeyError,
                      test_set.ParseResults, results_str)
