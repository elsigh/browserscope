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


_CATEGORY = 'sunspider'


class SunSpiderTest(test_set_base.TestBase):
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
        max_value=60000)


_TESTS = (
  # key, name, doc
  SunSpiderTest(
    '3d', '3d', '3d'
  ),
  SunSpiderTest(
    'access', 'Access', 'Access'
  ),
  SunSpiderTest(
    'bitops', 'BitOps', 'Bitops'
  ),
  SunSpiderTest(
    'controlflow', 'ControlFlow', 'ControlFlow'
  ),
  SunSpiderTest(
    'crypto', 'Crypto', 'Crypto'
  ),
  SunSpiderTest(
    'date', 'Date', 'Date'
  ),
  SunSpiderTest(
    'math', 'Math', 'Math'
  ),
  SunSpiderTest(
    'regexp', 'RegExp', 'RegExp'
  ),
  SunSpiderTest(
    'string', 'String', 'String'
  ),
  SunSpiderTest(
    'total', 'Total Time', 'The total time of running all SunSpider Benchmark tests'
  ),
)


class SunSpiderTestSet(test_set_base.TestSet):

  def GetTestScoreAndDisplayValue(self, test, raw_scores):
      """Get a normalized score (0 to 100) and a value to output to the display.

    Args:
      test_key: a key for a test_set test.
      raw_scores: a dict of raw_scores indexed by test keys.
    Returns:
      score, display_value
          # score is from 0 to 100.
          # display_value is the text for the cell.
    """
    raw_score = raw_scores.get(test_key, None)
    if raw_score:
      return raw_score, raw_score
    else:
      return 0, ''


TEST_SET = SunSpiderTestSet(
    category=_CATEGORY,
    category_name='SunSpider',
    subnav={
      'Test': '/%s/test' % _CATEGORY,
      'About': '/%s/about' % _CATEGORY,
    },
    home_intro = '''This is SunSpider, a JavaScript benchmark. This benchmark tests the
    core JavaScript language only, not the DOM or other browser APIs. It is designed to
    compare different versions of the same browser, and different browsers to each other.
<a href="/sunspider/about">Read more about the SunSpider benchmark suite tests.</a>''',
    tests=_TESTS
)
