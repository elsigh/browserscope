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
    self.group_members = group_members
    test_set_base.TestBase.__init__(
        self,
        key=key,
        name=name,
        doc=doc,
        url=self.TESTS_URL_PATH,
        min_value=0,
        max_value=2200,  # TODO(mikesamuel): what is a sensible max value?
        is_hidden_stat=is_hidden_stat)

def rate_display(display, good):
  # TODO(mikesamuel): 3 scores chosen because of the pretty colors they make
  if good is not None:
    if display in good:
      return 100
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
    return JskbTest(name, summary, doc, is_hidden_stat=True)

  for group in ecmascript_snippets.SNIPPET_GROUPS:
    group_info = group[0]
    group_members = [new_test(test) for test in group[1:]]
    tests.extend(group_members)
    tests.append(JskbTest(group_info[ecmascript_snippets.NAME],
                          group_info[ecmascript_snippets.NAME],
                          group_info[ecmascript_snippets.DOC],
                          is_hidden_stat=False,
                          group_members=tuple(group_members)))
  return tests

_TESTS = tuple(make_test_list())

class JskbTestSet(test_set_base.TestSet):

  def ParseResults(self, results_str, ignore_key_errors=False):
    """Parses a results string.

    Args:
      results_str: a string like 'test_1=raw_score_1,test_2=raw_score_2, ...'.
      ignore_key_errors: if true, skip checking keys with list of tests
    Returns:
      {test_1: {'raw_score': score_1}, test_2: {'raw_score': score_2}, ...}
    """
    test_scores = [x.split('=') for x in str(results_str).split(',')]
    test_keys = sorted([x[0] for x in test_scores])
    group_keys = sorted(group[0][ecmascript_snippets.NAME]
                        for group in ecmascript_snippets.SNIPPET_GROUPS)
    if test_keys == group_keys:
      # A packed format is used for showing results on the home page.
      parsed_results = {}
      for group_key, values in test_scores:
        group = self.GetTest(group_key)
        values = int(values)
        parsed_results[group_key] = {'raw_score': values}
        for member in group.group_members:
          parsed_results[member.key] = {'raw_score': values % 100}
          values /= 100
    elif test_keys == self._test_keys:
      try:
        parsed_results = dict([(key, {'raw_score': int(score)})
                               for key, score in test_scores])
      except ValueError:
        raise test_set_base.ParseResultsValueError
    else:
      raise test_set_base.ParseResultsKeyError(expected=self._test_keys,
                                               actual=test_keys)
    return parsed_results

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
    group_members = test.group_members
    if len(group_members):
      if raw_scores is None:
        return 50, ''
      abbrevs = set()
      total_score = 0
      n_scored = 0
      for member in group_members:
        snippet = ecmascript_snippets.with_name(member.key)
        member_median = raw_scores.get(member.key)
        if member_median is not None:
          score, display = self.GetTestScoreAndDisplayValue(
              member.key, raw_scores)
          if ecmascript_snippets.ABBREV in snippet:
            abbrev = snippet.get(ecmascript_snippets.ABBREV).get(display)
            if abbrev:
              abbrevs.add(abbrev)
          total_score += score
          n_scored += 1
      avg_score = (n_scored and int(total_score / n_scored)) or 60
      abbrevs = list(abbrevs)
      abbrevs.sort()
      return avg_score, ', '.join(abbrevs)

    snippet = ecmascript_snippets.with_name(test_key)
    median = raw_scores[test_key]
    # TODO(mikesamuel): a confidence metric around the results.
    int_median = int(round(median))
    
    display = '?'
    values = snippet[ecmascript_snippets.VALUES]
    if int_median >= 0 and int_median < len(values):
      display = values[int_median]

    return rate_display(display, snippet.get(ecmascript_snippets.GOOD)), display

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
