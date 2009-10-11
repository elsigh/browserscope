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


_CATEGORY = 'security'


class SecurityTest(test_set_base.TestBase):
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
        url=self.TESTS_URL_PATH,
        score_type='boolean',
        doc=doc,
        min_value=0,
        max_value=1)


_TESTS = (
  # key, name, doc
  SecurityTest('postMessage API', 'postMessage API', 'TODO'),
  SecurityTest('JSON.parse API', 'JSON.parse API', 'TODO'),
  SecurityTest('toStaticHTML API', 'toStaticHTML API', 'TODO'),
  SecurityTest('httpOnly cookie API', 'httpOnly cookie API', 'TODO'),
  SecurityTest('Block reflected XSS', 'Block reflected XSS', 'TODO'),
  SecurityTest('Block location spoofing', 'Block location spoofing', 'TODO'),
  SecurityTest('Block window.top spoofing', 'Block window.top spoofing',
               'TODO'),
  SecurityTest('Block JSON hijacking', 'Block JSON hijacking', 'TODO'),
  SecurityTest('Block CSS expressions', 'Block CSS expressions', 'TODO'),
  SecurityTest('Block cross-origin document', 'Block cross-origin document',
               'TODO'),
  SecurityTest('Block cross-origin contentDocument',
               'Block cross-origin contentDocument', 'TODO'),
  SecurityTest('Block UTF-7 sniffing', 'Block UTF-7 sniffing', 'TODO'),
  SecurityTest('Block all UTF-7', 'Block all UTF-7', 'TODO'),
)


class SecurityTestSet(test_set_base.TestSet):

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
    #logging.info('network getrowscore results: %s' % results)

    total_tests = 0
    total_valid_tests = 0
    total_score = 0
    tests = self.tests
    for test in tests:
      total_tests += 1
      if results.has_key(test.key):
        score = results[test.key]['score']
        #logging.info('test: %s, score: %s' % (test.key, score))
        total_valid_tests += 1
        # For booleans, when "score" is 10 that's test_type true.
        if score == 10:
          total_score += 1

    #logging.info('%s, %s, %s' % (total_score, total_tests, total_valid_tests))
    score = int(round(100 * total_score / total_tests))
    display = '%s/%s' % (total_score, total_valid_tests)

    return score, display


TEST_SET = SecurityTestSet(
    category=_CATEGORY,
    category_name='Security',
    tests=_TESTS,
    test_page='/%s/static/%s.html' % (_CATEGORY, _CATEGORY)
)
