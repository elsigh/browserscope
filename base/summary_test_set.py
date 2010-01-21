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

"""Benchmark Tests Definitions."""

import logging

from categories import test_set_base
from categories import all_test_sets


class SummaryTest(test_set_base.TestBase):

  def __init__(self, category, category_name):
    test_set_base.TestBase.__init__(
        self,
        key=category,
        name=category_name,
        url=None,
        doc=None,
        min_value=0,
        max_value=0)


_TESTS = []
for test_set in all_test_sets.GetTestSets():
  _TESTS.append(SummaryTest(test_set.category, test_set.category_name))

class SummaryTestSet(test_set_base.TestSet):

  def GetRowScoreAndDisplayValue(self, results):
    """Get the overall score for this row of results data.
    Args:
      results: A dictionary that looks like:
      {
        'testkey1': {'score': 1-10, 'median': median, 'display': 'celltext'},
        'testkey2': {'score': 1-10, 'median': median, 'display': 'celltext'},
        etc...
      }

    Returns:
      A tuple of (score, display)
      Where score is a value between 1-100.
      And display is the text for the cell.
    """
    logging.info('summary getrowscore results: %s' % results)
    if not results.has_key('score') or results['score']['median'] is None:
      score = 0
    else:
      score = results['score']['median']
    return score, 'yo'


TEST_SET = SummaryTestSet(
    category='summary',
    category_name='Summary',
    tests=_TESTS,
    test_page=''
)
