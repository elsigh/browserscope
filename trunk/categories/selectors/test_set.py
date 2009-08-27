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

"""Test Definitions."""

__author__ = 'elsigh@google.com (Lindsey Simon)'


import logging

from categories import test_set_base


_CATEGORY = 'selectors'


class SelectorsTest(test_set_base.TestBase):
  TESTS_URL_PATH = '/%s/test' % _CATEGORY

  def __init__(self, key, name, doc):
    """Initialze a benchmark test.

    Args:
      key: key for this in dict's
      name: a human readable label for display
      url_name: the name used in the url
      score_type: 'boolean' or 'custom'
      doc: a description of the test
      value_range: (min_value, max_value) as integer values
      is_hidden_stat: whether or not the test shown in the stats table
    """
    test_set_base.TestBase.__init__(
        self,
        key=key,
        name=name,
        doc=doc,
        url=self.TESTS_URL_PATH,
        score_type='custom',
        min_value=0,
        max_value=100)

  def GetScoreAndDisplayValue(self, median, tests=None):
    """Returns a tuple with display text for the cell as well as a 1-100 value.
    """
    if median == None or median == '':
      return 0, ''

    median = int(median)
    score = median
    display = median
    return score, display


_TESTS = (
  # key, name, doc
  SelectorsTest('score', 'Score', 'Selectors API test score'),
  SelectorsTest('passed', 'Passed', 'Selectors API tests passed'),
  SelectorsTest('failed', 'Failed', 'Selectors API tests failed')
)

TEST_SET = test_set_base.TestSet(
    category=_CATEGORY,
    category_name='Selectors API',
    subnav={
      'Test': '/%s/test' % _CATEGORY,
      'About': '/%s/about' % _CATEGORY,
    },
    home_intro = '''<a href="/selectors/about">Read more</a> about the Selectors API test. These tests were written by John Resig and originally published at <a target="_blank" href="http://ejohn.org/apps/selectortest">ejohn.org/apps/selectortest</a>''',
    tests=_TESTS
)
