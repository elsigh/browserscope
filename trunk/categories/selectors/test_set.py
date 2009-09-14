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


from decimal import Decimal
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
        max_value=2200)

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
    score = median
    display = median
    if self.key == 'passed':
      if median >= 2100:
        score = 95
      elif median >= 2000:
        score = 85
      elif median >= 1950:
        score = 75
      elif median >= 1800:
        score = 65
      else:
        score = 50
    elif self.key == 'failed':
      if median == 0:
        score = 95
      elif median <= 5:
        score = 85
      elif median <= 20:
        score = 75
      else:
        score = 50
    #logging.info('score %s, display %s' % (score, display))
    return score, display


_TESTS = (
  # key, name, doc
  #SelectorsTest('score', 'Score', 'Selectors API test score'),
  SelectorsTest('passed', 'Passed', 'Selectors API tests passed'),
  SelectorsTest('failed', 'Failed', 'Selectors API tests failed')
)


class SelectorsTestSet(test_set_base.TestSet):

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
    #logging.info('%s GetRowScore, results:%s' % (self.category, results))
    if (not results.has_key('passed') or results['passed']['median'] is None or
        results['failed']['median'] is None):
      score = 0
      display = ''
    else:
      score = str(int(100.0 * results['passed']['median'] /
          (results['passed']['median'] + results['failed']['median'])))

      num = round(100.0 * results['passed']['median'] /
                                    (results['passed']['median'] + results['failed']['median']),
                                    1)
      #logging.info('num: %s', num)
      #percent = str(Decimal(str()))
      score = int(num)
      if score == 0:
        score = 10
        display = '0%'
      else:
        display = str(num) + '%'
    #logging.info('Row score: %s' % score)
    return score, display

TEST_SET = SelectorsTestSet(
    category=_CATEGORY,
    category_name='Selectors API',
    tests=_TESTS
)
