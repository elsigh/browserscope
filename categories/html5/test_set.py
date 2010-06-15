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

"""HTML5 Tests Definitions."""

import logging

from categories import test_set_base


_CATEGORY = 'html5'

_TEST_URL = 'http://html5test.com/'

class Html5Test(test_set_base.TestBase):

  def __init__(self, key, name, doc, url=None):
    """Initialze a benchmark test.

    Args:
      key: key for this in dict's
      name: a human readable label for display
      url_name: the name used in the url
      doc: a description of the test
      value_range: (min_value, max_value) as integer values
    """
    test_set_base.TestBase.__init__(
        self,
        key=key,
        name=name,
        url=_TEST_URL,
        doc=doc,
        min_value=0,
        max_value=1)
    self.url = url


_TESTS = (
  # key, name, doc
)


class Html5TestSet(test_set_base.TestSet):

  def GetRowScoreAndDisplayValue(self, results):
    """Get the overall score for this row of results data.

    Args:
      results: {
          'test_key_1': {'score': score_1, 'raw_score': raw_score_1, ...},
          'test_key_2': {'score': score_2, 'raw_score': raw_score_2, ...},
          ...
          }
    Returns:
      score, display_value
          # score is from 0 to 100.
          # display_value is the text for the cell.
    """
    return 100, 'tmp'


TEST_SET = Html5TestSet(
    category=_CATEGORY,
    category_name='HTML5',
    summary_doc='Tests of HTML5 capabilities.',
    tests=_TESTS,
    test_page=_TEST_URL
)
