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

  def GetScoreAndDisplayValue(self, median, user_agent, params=None,
                              is_uri_result=False):
    """Returns a tuple with display text for the cell as well as a 1-100 value.
    """
    if self.key == 'score':
      return (90,'whatever man')
    else:
      return (median, median)


_TESTS = (
  # key, name, doc
  SelectorsTest('score', 'Score', 'Selectors API test score'),
  SelectorsTest('passed', 'Passed', 'Selectors API tests passed'),
  SelectorsTest('failed', 'Failed', 'Selectors API tests failed')
)

TEST_SET = test_set_base.TestSet(
    category=_CATEGORY,
    category_name='Selectors API',
    tests=_TESTS
)
