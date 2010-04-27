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

"""Benchmark Tests Definitions."""

import logging

from categories import test_set_base


_CATEGORY = 'acid3'


class Acid3Test(test_set_base.TestBase):
  TESTS_URL_PATH = '/%s/test' % _CATEGORY

  def __init__(self, key, name, doc):
    """Initialze a benchmark test.

    Args:
      key: key for this in dict's
      name: a human readable label for display
      doc: a description of the test
    """
    test_set_base.TestBase.__init__(
        self,
        key=key,
        name=name,
        url=self.TESTS_URL_PATH,
        doc=doc,
        min_value=0,
        max_value=100)


_TESTS = (
  # key, name, doc
  Acid3Test(
    'score', 'Score', 'Acid3 test score'
  ),
)


class Acid3TestSet(test_set_base.TestSet):

  def GetTestScoreAndDisplayValue(self, test_key, raw_scores):
    """Get a normalized score (0 to 100) and a value to output to the display.

    Args:
      test_key: a key for a test_set test.
      raw_scores: a dict of raw_scores indexed by key.
    Returns:
      score, display_value
          # score is an integer in 0 to 100.
          # display_value is the text for the cell.
    """
    raw_score = raw_scores.get(test_key, 0)
    if raw_score:
      return raw_score, '%s/100' % raw_score
    else:
      return 0, ''

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
    test_key = 'score'
    score = results.get(test_key, {}).get('score', None) or 0
    return score, ''


TEST_SET = Acid3TestSet(
    category=_CATEGORY,
    category_name='Acid3',
    summary_doc='Tests of dynamic browser capabilities to encourage browser interoperability.',
    tests=_TESTS,
    test_page='/%s/%s.html' % (_CATEGORY, _CATEGORY)
)
