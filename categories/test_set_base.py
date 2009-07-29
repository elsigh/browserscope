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


class TestSet(object):
  def __init__(self, category, category_name, tests, subnav, home_intro,
               default_params=None):
    """Initialize a test set.

    A test set has all the tests for a category.

    Args:
      category: a string
      category_name: a string, human-readable
      tests: a list of test instances
      subnav: a dict of labels to urls
      home_intro: a string, possibly HTML, to give an introduction
    """
    self.category = category
    self.category_name = category_name
    self.tests = tests
    self.subnav = subnav
    self.home_intro = home_intro
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

