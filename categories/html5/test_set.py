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


class Html5Test(test_set_base.TestBase):
  TESTS_URL_PATH = '/%s/test' % _CATEGORY

  def __init__(self, key, name, doc, url=None):
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
    self.url = url


_TESTS = (
  # key, name, doc
  Html5Test('testCanvas', 'Canvas Tag',
  'Support for <code>&lt;canvas&gt;</code>'),
  Html5Test('testVideo', 'Video Tag',
  'Support for <code>&lt;video&gt;</code>'),
  Html5Test('testLocalStorage', 'Local Storage',
  'Support for local storage',
  'http://dev.w3.org/html5/webstorage/'),
  Html5Test('testWebWorkers', 'Web Workers',
  'Support for Web Workers',
  'http://www.whatwg.org/specs/web-workers/current-work/'),
  Html5Test('testOffline', 'Offline',
  'Support for offline Web applications',
  'http://www.whatwg.org/specs/web-apps/current-work/multipage/offline.html#offline'),
  Html5Test('testGeolocation', 'Geolocation',
  'Support for Geolocation API',
  'http://www.w3.org/TR/geolocation-API/'),
  Html5Test('testInputSearch', 'Search <input>',
  'Support for <code>&lt;input type="search"&gt;</code>'),
  Html5Test('testInputNumber', 'Number <input>',
  'Support for <code>&lt;input type="number"&gt;</code>'),
  Html5Test('testInputRange', 'Range <input>',
  'Support for <code>&lt;input type="range"&gt;</code>'),
  Html5Test('testInputColor', 'Color <input>',
  'Support for <code>&lt;input type="color"&gt;</code>'),
  Html5Test('testInputTel', 'Tel <input>',
  'Support for <code>&lt;input type="tel"&gt;</code>'),
  Html5Test('testInputUrl', 'URL <input>',
  'Support for <code>&lt;input type="url"&gt;</code>'),
  Html5Test('testInputEmail', 'Email <input>',
  'Support for <code>&lt;input type="email"&gt;</code>'),
  Html5Test('testInputDate', 'Date <input>',
  'Support for <code>&lt;input type="date"&gt;</code>'),
  Html5Test('testInputMonth', 'Month <input>',
  'Support for <code>&lt;input type="month"&gt;</code>'),
  Html5Test('testInputWeek', 'Week <input>',
  'Support for <code>&lt;input type="week"&gt;</code>'),
  Html5Test('testInputTime', 'Time <input>',
  'Support for <code>&lt;input type="time"&gt;</code>'),
  Html5Test('testInputDateTime', 'DateTime <input>',
  'Support for <code>&lt;input type="datetime"&gt;</code>'),
  Html5Test('testInputDateTimeLocal', 'DateTimeLocal <input>',
  'Support for <code>&lt;input type="datetime-local"&gt;</code>'),
  Html5Test('testInputPlaceholderText', 'Placeholder Text',
  'Support for <code>placeholder</code> text in <code>&lt;input&gt;</code>'),
  Html5Test('testInputAutofocus', 'Autofocus',
  'Support for <code>autofocus</code> in <code>&lt;input&gt;</code>',
  'http://www.whatwg.org/specs/web-apps/current-work/multipage/forms.html#autofocusing-a-form-control'),

)


class Html5TestSet(test_set_base.TestSet):

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


TEST_SET = Html5TestSet(
    category=_CATEGORY,
    category_name='HTML5',
    tests=_TESTS,
    test_page='/%s/static/%s.html' % (_CATEGORY, _CATEGORY)
)
