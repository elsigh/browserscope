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
import re
import sys


_CATEGORY = 'jskb'


class JskbTest(test_set_base.TestBase):
  TESTS_URL_PATH = '/%s/test' % _CATEGORY

  def __init__(self, key, name, doc, is_hidden_stat, group_members=()):
    """Initialze a benchmark test.

    Args:
      key: key for this in dict's
      name: a human readable label for display
      doc: a description of the test
      is_hidden_stat: should it be shown on the summary page
    """
    self.is_hidden_stat = is_hidden_stat
    self.group_members = group_members
    test_set_base.TestBase.__init__(
        self,
        key=key,
        name=name,
        doc=doc,
        url=self.TESTS_URL_PATH,
        score_type='custom',
        min_value=0,
        max_value=2200)  # TODO(mikesamuel): what is a sensible max value?

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

    if len(self.group_members):
      if is_uri_result:
        snippet = ecmascript_snippets.with_name(key)
        medians = {}
        for member in self.group_members:
          medians[member.key] = median % 100
          median /= 100
      if medians is None: return 50, ''
      abbrevs = set()
      total_score = 0
      n_scored = 0
      for member in self.group_members:
        snippet = ecmascript_snippets.with_name(member.key)
        member_median = medians.get(member.key)
        if member_median is not None:
          score, display = member.GetScoreAndDisplayValue(
              member_median, medians, is_uri_result)
          if ecmascript_snippets.ABBREV in snippet:
            abbrev = snippet.get(ecmascript_snippets.ABBREV).get(display)
            if abbrev: abbrevs.add(abbrev)
          total_score += score
          n_scored += 1
      avg_score = (n_scored and int(100 * (total_score / n_scored))) or 50
      abbrevs = list(abbrevs)
      abbrevs.sort()
      return avg_score, ', '.join(abbrevs)

    snippet = ecmascript_snippets.with_name(key)
    # TODO(mikesamuel): a confidence metric around the results.
    int_median = int(round(median))

    display = '?'
    values = snippet[ecmascript_snippets.VALUES]
    if int_median >= 0 and int_median < len(values):
      display = values[int_median]

    return rate_display(display, snippet.get(ecmascript_snippets.GOOD)), display

def rate_display(display, good):
  # TODO(mikesamuel): 3 scores chosen because of the pretty colors they make
  if good is not None:
    if display in good: return 100
    return 50
  return 75

def html(text):
  return re.sub('<', '&lt;', re.sub('>', '&gt;', re.sub('&', '&amp;', text)))

def make_test_list():
  tests = []

  def new_test(test):
    name = test[ecmascript_snippets.NAME]
    code = '<pre>%s</pre>' % html(test[ecmascript_snippets.CODE])
    summary = test.get(ecmascript_snippets.SUMMARY, None)
    doc = test.get(ecmascript_snippets.DOC, None)
    if summary is None:
      summary = test[ecmascript_snippets.CODE]
    elif doc is None:
      doc = code
    else:
      doc = '%s\n%s' % (doc, code)
    return JskbTest(name, summary, doc, True)

  for group in ecmascript_snippets._SNIPPET_GROUPS:
    group_info = group[0]
    group_members = [new_test(test) for test in group[1:]]
    tests.extend(group_members)
    tests.append(JskbTest(group_info[ecmascript_snippets.NAME],
                          group_info[ecmascript_snippets.NAME],
                          group_info[ecmascript_snippets.DOC],
                          False, tuple(group_members)))
  return tests

_TESTS = tuple(make_test_list())

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
