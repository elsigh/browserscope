#!/usr/bin/python2.5
# -*- coding: utf-8 -*-
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


"""Reflow Test Definitions."""

__author__ = 'elsigh@google.com (Lindsey Simon)'


import logging

from categories import test_set_base
from categories import test_set_params


_CATEGORY = 'reflow'


class ReflowTest(test_set_base.TestBase):
  TESTS_URL_PATH = '/%s/test' % _CATEGORY
  def __init__(self, key, name, doc):
    test_set_base.TestBase.__init__(
        self,
        key=key,
        name=name,
        url='%s?t=%s' % (self.TESTS_URL_PATH, key),
        doc=doc,
        min_value=0,
        max_value=60000)


_TESTS = (
  # key, name, doc
  ReflowTest('testDisplay', 'Display Block',
    '''This test takes an element and sets its
    style.display="none". According to the folks at Mozilla this has
    the effect of taking an element out of the browser's "render tree"
    (the in-memory representation of all of results of
    geometry/positioning calculations for that particular
    element). Setting an element to display="none" has the additional
    effect of removing all of an element's children from the render tree
    as well. Next, the test resets the element's style.display="", which
    sets the element's display back to its original value. Our thinking
    was that this operation ought to approximate the max cost of reflowing
    an element on a page since the browser has to
    recalculate all positions and sizes for every child within the
    element as well as any changes to the overall document.'''),
  ReflowTest('testVisibility', 'Visiblility None',
    '''Much like the display test above, this test sets an element's
    style.visibility="hidden" and then resets it back to its default,
    which is "visible". This change should be less costly than
    changing display from "none" to the default since the browser
    should not be purging the element from the render tree.'''),
  ReflowTest('testNonMatchingClass', 'Non Matching Class',
    '''This test adds a class name to an element where that
    class name is not present in the document's CSS object
    model. This tests CSS selector match time, and more specifically
    against selectors with classnames.'''),
  ReflowTest('testFourClassReflows', 'Four Reflows by Class',
    '''This test adds a class name to an element that will match a
    previously added CSS declaration added to the CSSOM. This
    declaration is set with four property value pairs which should in
    and of themselves be capable of causing a 1x reflow time. For
    instance, "font-size: 20px; line-height: 10px; padding-left: 10px;
    margin-top: 7px;". This test aims to test whether reflow
    operations occur in a single queue flush or if they are performed
    one at a time when these changes are made via a CSS
    classname. This test is a sort of opposite to the Four Reflows By
    Script.'''),
  ReflowTest('testFourScriptReflows', 'Four Reflows by Script',
    '''Like the Four Reflows By Class test, but instead this test has
    four lines of Javascript, each of which alters the style object
    with a property/value that by itself could cause a 1x reflow
    time.'''),
  ReflowTest('testTwoScriptReflows', 'Two Reflows by Script',
    '''Like the Four Reflows By Script test, except with only two lines
    of Javascript.'''),
  ReflowTest('testPaddingPx', 'Padding px',
    '''This test sets style.padding="FOOpx", aka padding on all sides of
    the box model.'''),
  ReflowTest('testPaddingLeftPx', 'Padding Left px',
    '''This test sets style.paddingLeft="FOOpx", aka padding on only the
    left side of the box.'''),
  ReflowTest('testFontSizeEm', 'Font Size em',
    '''This test changes an element's style.fontSize to an em-based
    value.'''),
  ReflowTest('testWidthPercent', 'Width %',
    '''This test sets an element's style.width="FOO%"'''),
  ReflowTest('testBackground', 'Background Color',
    '''This test sets an element's style.background="#FOO", aka a
    hexadecimal color.'''),
  ReflowTest('testOverflowHidden', 'Overflow Hidden',
    '''This test sets an element's style.overflow="hidden" and then back
    again, timing the cost of an element returning to the default
    overflow which is "visible"'''),
  ReflowTest('testGetOffsetHeight', 'Do Nothing / OffsetHeight',
    '''This test does nothing other than the request for offsetHeight
    after already having done so. Theoretically, this test is
    something like a control for our test and should have a 0 or very
    low time.'''),
)

BASELINE_TEST_NAME = 'testDisplay'
class ReflowTestSet(test_set_base.TestSet):

  def AdjustResults(self, results):
    """Re-scores the actual value against a baseline score for reflow.

    Sets the 1x reflow time for this test run and compares other times
    against that. This is to try to account for issues around selection
    bias, processor speed, etc...
    We'll preserve the original millisecond time as an expando value in case
    we want to do some calculations with it later.

    Args:
      results: {
          test_key_1: {'raw_score': raw_score_1},
          test_key_2: {'raw_score': raw_score_2},
          ...
          }
    Returns:
        { test_key_1: {'raw_score': adjusted_raw_score_1, 'expando': score_1},
          test_key_2: {'raw_score': adjusted_raw_score_2, 'expando': score_2},
          ...
          }
    """
    if BASELINE_TEST_NAME not in results:
      raise NameError('No baseline score found in the test results')
    baseline_score = float(results[BASELINE_TEST_NAME]['raw_score'])

    # Turn all values into some computed percentage of the baseline score.
    # This resets the score in the dict, but adds an expando to preserve the
    # original score's milliseconds value.
    for result in results.values():
      result['expando'] = result['raw_score']
      result['raw_score'] = int(100.0 * result['raw_score'] / baseline_score)
    return results

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
    raw_score = raw_scores.get(test_key, None)
    if raw_score in (None, ''):
      # We'll give em the benefit of the doubt here.
      return 90, ''

    raw_score = int(raw_score)
    if raw_score <= 10:
      score, display = 100, '0X'
    elif raw_score <= 35:
      score, display = 97, '¼X'
    elif raw_score <= 65:
      score, display = 95, '½X'
    elif raw_score <= 85:
      score, display = 93, '¾X'
    elif raw_score <= 110:
      score, display = 90, '1X'
    elif raw_score <= 180:
      score, display = 80, '2X'
    else:
      score, display = 60, '3X'
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
    return 90, ''


TEST_SET = ReflowTestSet(
  category=_CATEGORY,
  category_name='Reflow',
  summary_doc='Tests of reflow time for different CSS selectors.',
  tests=_TESTS,
  # default_params=Params(
  # 'nested_anchors', 'num_elements=400', 'num_nest=4',
  # 'css_selector=#g-content *', 'num_css_rules=1000',
  # 'css_text=border: 1px solid #0C0; padding: 8px;'),
 default_params=test_set_params.Params('acid1', 'num_elements=300'),
 test_page='/%s/test_acid1' % _CATEGORY
)
