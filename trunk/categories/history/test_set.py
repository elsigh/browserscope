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

"""History Tests Definitions."""

import logging

from categories import test_set_base

from django import shortcuts

_CATEGORY = 'history'


class HistoryTest(test_set_base.TestBase):

  def __init__(self, key, name, url_name, doc, min_value, max_value,
               is_hidden_stat=False, cell_align='center'):
    """Initialze a history test.

    Args:
      key: key for this in dict's
      name: a human readable label for display
      url_name: the name used in the url
      doc: a description of the test
      min_value: an integer
      max_value: an integer
      is_hidden_stat: whether or not the test shown in the stats table
      cell_align: 'right', 'left', or 'center' for output formating
    """
    test_set_base.TestBase.__init__(
        self,
        key=key,
        name=name,
        url=url_name,
        doc=doc,
        min_value=min_value,
        max_value=max_value,
        cell_align=cell_align,
        is_hidden_stat=is_hidden_stat)
    self.url_name = url_name


class BooleanHistoryTest(HistoryTest):
  def __init__(self, key, name, url_name, doc, **kwds):
    """Initialze a boolean history test.

    Args:
      key: key for this in dict's
      name: a human readable label for display
      url_name: the name used in the url
      doc: a description of the test
      kwds: any addition keyword parameters
    """
    HistoryTest.__init__(self, key, name, url_name, doc,
                         min_value=0, max_value=1, **kwds)


_TESTS = (
  # key, name, url_name, score_type, doc
  BooleanHistoryTest(
    'history_hashChange_back_forward', 'hashchange: back/forward', '../../history/static/opener.html?history_hashChange_back_forward',
    '''Pushes some states onto the history stack via location.hash, the navigates back and forward.'''),

  BooleanHistoryTest(
    'history_hashChange_jump', 'hashchange: jump', '../../history/static/opener.html?history_hashChange_jump',
    '''Pushes some states onto the history stack via location.hash, then jump over entries in the stack.'''),

  BooleanHistoryTest(
    'history_hashChange_back_forward_iframe_replace', 'hashchange: back/forward + iframe location.replace', '../../history/static/opener.html?history_hashChange_back_forward_iframe_replace',
    '''Identical to hashChange: back/forward, but adds an iframe whose location is replaced at each hashchange.'''),

  BooleanHistoryTest(
    'history_hashChange_away', 'hashchange: away', '../../history/static/opener.html?history_hashChange_away',
    '''Similar to hashchange: back/forward, but also navigates away from page to ensure history stack is preserved when we navigate back.'''),

  BooleanHistoryTest(
    'history_pushState_back_forward', 'pushState: back/forward', '../../history/static/opener.html?history_pushState_back_forward',
    '''Pushes history state onto the stack, then navigates back / forward.'''),

  BooleanHistoryTest(
    'history_pushState_jump', 'pushState: jump', '../../history/static/opener.html?history_pushState_jump',
    '''Pushes some states onto the history stack, then jump over entries in the stack.'''),

  BooleanHistoryTest(
    'history_pushState_away', 'pushState: away', '../../history/static/opener.html?history_pushState_away',
    '''Pushes history state onto the stack, then navigates away and back.'''),

  BooleanHistoryTest(
    'history_pushState_referrer', 'pushState: referrer', '../../history/static/opener.html?history_pushState_referrer',
    '''Pushes history state onto the stack, then navigates away and verifies the referrer matches the pushed state.'''),

  BooleanHistoryTest(
    'history_pushState_pop_after_load', 'pushState: popstate fires after onload()', '../../history/static/opener.html?history_pushState_pop_after_load',
    '''Pushes history state onto the stack, then navigates away and verifies that subsequent popstates fire after onload().'''),

  BooleanHistoryTest(
    'history_pushState_cross_site', 'pushState: cross site', '../../history/static/opener.html?history_pushState_cross_site',
    '''Attempts to push a cross domain URL onto the history stack.'''),

  BooleanHistoryTest(
    'history_replaceState_away', 'replaceState: away', '../../history/static/opener.html?history_replaceState_away',
    '''Pushes and replaces the URL on the top of the history stack, then navigates away and verifies that subsequent popstates are as expected.'''),

  BooleanHistoryTest(
    'history_replaceState_referrer', 'replaceState: referrer', '../../history/static/opener.html?history_replaceState_referrer',
    '''Replaces the URL on the top of the history stack, then navigates away and verifies the referrer matches the replacement URL.'''),
)


class HistoryTestSet(test_set_base.TestSet):

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
    score = 0
    raw_score = raw_scores.get(test_key, None)
    if raw_score is None:
      return 0, ''
    if test_key == 'hostconn':
      if raw_score > 2:
        score = 100
      elif raw_score == 2:
        score = 50
      elif raw_score == 1:
        score = 1
      else:
        score = 0
    elif test_key == 'maxconn':
      if raw_score > 20:
        score = 100
      elif raw_score >= 10:
        score = 50
      elif raw_score > 1:
        score = 1
      else:
        score = 0
    return score, str(raw_score)

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

    Why do we use totalTests as the divisor for "score", but totalValidTests as the divisor for "display"?
    There are going to be old browsers that are no longer tested. They might have gotten 6/8 (75%)
    back in the old days, but now we've added more tests and they'd be lucky to get 6/12 (50%). If
    we compare 6/8 to newer browsers that get 8/12, the old browser would win, even though it would
    fail in side-by-side testing, so we have to use totalTests as the divisor for "score".
    But we can't misrepresent the actual tests that were performed, so we have to show the user the
    actual number of tests for which we have results, which means using totalValidTests as the divisor
    for "display".
    """
    total_tests = 0
    total_valid_tests = 0
    total_score = 0
    for test in self.VisibleTests():
      total_tests += 1
      if test.key in results and results[test.key]['score'] is not None:
        # For booleans, when "score" is 100 that's test_type true.
        # steve's custom score for hostconn & maxconn map
        # simply to 10 for good, 5 for ok, and 0 for fail, but we only award
        # a point for a 10 on those.
        if results[test.key]['score'] == 100:
          total_score += 1
        total_valid_tests += 1
    score = int(round(100.0 * total_score / total_tests))
    display = '%s/%s' % (total_score, total_valid_tests)
    return score, display


TEST_SET = HistoryTestSet(
    category=_CATEGORY,
    category_name='History',
    summary_doc='Tests that address functional correctness of browser history, as used by web applications.',
    tests=_TESTS,
    test_page='/multi_test_frameset'
)

