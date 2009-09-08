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

"""Test set class."""

__author__ = 'slamm@google.com (Stephen Lamm)'


import logging

from models import result_ranker

class TestBase(object):
  def __init__(self, key, name, url, score_type, doc, min_value, max_value,
               test_set=None):
    self.key = key
    self.name = name
    self.url = url
    self.score_type = score_type
    self.doc = doc
    self.min_value = min_value
    self.max_value = max_value
    self.test_set = test_set


  def GetRanker(self, user_agent_version, params):
    return result_ranker.Factory(
        self.test_set.category, self, user_agent_version, params)


  def GetScoreAndDisplayValue(self, median, medians=None, is_uri_result=False):
    """Custom scoring function.

    Args:
      median: The actual median for this test from all scores.
      medians: A dict of the medians for all tests indexed by key.
      is_uri_result: Boolean, if results are in the url, i.e. home page.
    Returns:
      (score, display)
      Where score is a value between 1-100.
      And display is the text for the cell.
    """
    return (median, median)


class TestSet(object):
  def __init__(self, category, category_name, tests, default_params=None):
    """Initialize a test set.

    A test set has all the tests for a category.

    Args:
      category: a string
      category_name: a string, human-readable
      tests: a list of test instances
    """
    self.category = category
    self.category_name = category_name
    self.tests = tests
    self.default_params = default_params
    self._test_dict = {}
    for test in tests:
      test.test_set = self  # add back pointer to each test
      self._test_dict[test.key] = test


  def GetTest(self, test_key):
    return self._test_dict[test_key]


  def ParseResults(self, results):
    """Rewrite the results dict before saving the results.

    Left to implementations to overload.

    Args:
      results: a list of dictionaries of results.
               i.e. [{'key': test1, 'score': time1},
                     {'key': test2, 'score': time2}]
    Returns:
      A list of dictionaries of results.
    """
    return results


  def GetRowScoreAndDisplayValue(self, results):
    """Get the overall score for this row of results data.
    Args:
      results: A dictionary that looks like:
      {
        'testkey1': {'score': 1-100, 'median': median, 'display': 'celltext'},
        'testkey2': {'score': 1-100, 'median': median, 'display': 'celltext'},
        etc...
      }

    Returns:
      A tuple of (score, display)
      Where score is a value between 1-100.
      And display is the text for the cell.
    """
    #logging.info('%s GetRowScore, results:%s' % (self.category, results))
    return (90, '')

