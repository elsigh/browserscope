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


from categories.jskb import ecmascript_snippets
from categories import test_set_base


_CATEGORY = 'jskb'


class JskbTest(test_set_base.TestBase):
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
    key = self.key
    snippet = ecmascript_snippets.with_name(key)
    # TODO(mikesamuel): a confidence metric around the results.
    int_median = int(round(median))

    display = '?'
    values = snippet[ecmascript_snippets.VALUES]
    if int_median >= 0 and int_median < len(values):
      display = values[int_median]

    good = snippet.get(ecmascript_snippets.GOOD)
    # TODO(mikesamuel): 3 scores chosen because of the pretty colors they make
    if good is not None:
      if display in good:
        score = 100
      else:
        score = 50
    else:
      score = 75
    return score, display


def new_test(test):
  name = test['name']
  code = '<pre>%s</pre>' % test['code']
  summary = test.get('summary', None)
  doc = test.get('doc', None)
  if summary is None:
    summary = test['code']
  elif doc is None:
    doc = code
  else:
    doc = '%s\n%s' % (doc, code)
  return JskbTest(name, summary, doc)

_TESTS = tuple([new_test(test) for test in ecmascript_snippets._SNIPPETS])


class JskbTestSet(test_set_base.TestSet):

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
    if (not results.has_key('passed') or results['passed']['median']
        or results['failed']['median'] is None):
      score = 0
      display = ''
    else:
      score = str(int(100.0 * results['passed']['median'] /
          (results['passed']['median'] + results['failed']['median'])))

      num = round(100.0 * results['passed']['median'] /
                  (results['passed']['median'] + results['failed']['median']),
                  1)
      score = int(num)
      if score == 0:
        score = 10
        display = '0%'
      else:
        display = str(num) + '%'
    return score, display

TEST_SET = JskbTestSet(
    category=_CATEGORY,
    category_name='JSKB',
    tests=_TESTS,
    test_page='/%s/environment-checks' % _CATEGORY
)
