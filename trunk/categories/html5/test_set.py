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
from models import user_test

_CATEGORY = 'html5'

# Niels' User Test record.
_USER_TEST_CATEGORY = 'usertest_agt1YS1wcm9maWxlcnINCxIEVGVzdBis_8gBDA'

_TEST_URL = 'http://html5test.com/'

class Html5Test(test_set_base.TestBase):

  def __init__(self, key, name, doc, out_of_total):
    """Initialze a benchmark test.

    Args:
      key: key for this in dict's
      name: a human readable label for display
      url_name: the name used in the url
      doc: a description of the test
      out_of_total: i.e. 11 for "Parsing rules" for foo/11
    """
    test_set_base.TestBase.__init__(
        self,
        key=key,
        name=name,
        url=None,
        doc=doc,
        min_value=0,
        max_value=user_test.MAX_VALUE)
    self.out_of_total = out_of_total

_TESTS = (
  Html5Test('Audio', 'Audio', '', 20),
  Html5Test('Canvas', 'Canvas', '', 20),
  Html5Test('Communication', 'Communication', '', 25),
  Html5Test('Elements', 'Elements', '', 30),
  Html5Test('Files', 'Files', '', 10),
  Html5Test('Forms', 'Forms', '', 38),
  Html5Test('Geolocation', 'Geolocation', '', 10),
  Html5Test('Local devices', 'Local devices', '', 20),
  Html5Test('Microdata', 'Microdata', '', 10),
  Html5Test('Parsing rules', 'Parsing rules', '', 11),
  Html5Test('Storage', 'Storage', '', 20),
  Html5Test('User interaction', 'User interaction', '', 25),
  Html5Test('Video', 'Video', '', 27),
  Html5Test('Web applications', 'Web applications', '', 14),
  Html5Test('WebGL', 'WebGL', '', 10),
  Html5Test('Workers', 'Workers', '', 10),
  Html5Test('Bonus points', 'Bonus points', '', None),
)


class Html5TestSet(test_set_base.TestSet):
  def __init__(self):
    test_set_base.TestSet.__init__(self,
      category=_CATEGORY,
      category_name='HTML5',
      summary_doc='Tests of HTML5 capabilities.',
      tests=_TESTS,
      test_page=_TEST_URL)
    self.user_test_category = _USER_TEST_CATEGORY


  def GetTestScoreAndDisplayValue(self, test_key, raw_scores):
    """Get a normalized score (0 to 100) and a value to output to the display.

    Args:
      test_key: a key for a test_set test.
      raw_scores: a dict of raw_scores indexed by test keys.
    Returns:
      score, display_value
          # score is from 0 to 100.
          # display_value is the text for the cell.
    """
    test = self.GetTest(test_key)
    test_score = raw_scores[test_key]
    if test_key == 'Bonus points':
      if test_score > 0:
        score = 100
        display = test_score
      else:
        score = 0
        display = ''
      logging.info('Bonus points: %s, %s %s' % (test_score, score, display))
    else:
      if test_score > 0:
        score = int(round(float(test_score / float('%d.0' % test.out_of_total)) * 100))
        display = '%s/%s' % (test_score, test.out_of_total)
      else:
        score = 0
        display = ''
      logging.info('%s: %s, %s %s' % (test_key, test_score, score, display))

    return score, display


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
    PERFECT_SCORE = 300
    total_score = 0
    for test_key, result in results.items():
      logging.info('rowscore for %s, raw: %s, score:%s' % (test_key, result['raw_score'], result['score']))
      if result['score']:
        total_score += result['raw_score']

    if total_score > 0:
      score = int(round(float(total_score / float('%d.0' % PERFECT_SCORE)) * 100))
      display = '%s/%s' % (total_score, PERFECT_SCORE)
    else:
      score = 0
      display = ''
    return score, display


TEST_SET = Html5TestSet()
