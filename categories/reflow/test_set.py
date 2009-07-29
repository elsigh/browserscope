#!/usr/bin/python2.4
#
# Copyright 2009 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the 'License')
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Reflow Test Definitions."""

__author__ = 'elsigh@google.com (Lindsey Simon)'


from categories import test_set_base


_CATEGORY = 'reflow'


class ReflowTest(test_set_base.TestBase):
  TESTS_URL_PATH = '/%s/test' % _CATEGORY
  def __init__(self, key, name, doc):
    test_set_base.TestBase.__init__(
        self,
        key=key,
        name=name,
        url='%s?t=%s' % (self.TESTS_URL_PATH, key),
        score_type='custom',
        doc=doc,
        min_value=0,
        max_value=60000)

  def ParseResults(self, results):
    """Normalizes the raw scores before sending them to the median trees.
    Args:
      results: A results dict. See util.ParseResults
    Returns:
      A results dict suitable for models.ResultParent.AddResults
    """



  def GetScoreAndDisplayValue(self, median):
    """Returns a tuple with display text for the cell as well as a 1-100 value.
    i.e. ('1X', 95)
    Args:
      median: The test median.
    Returns:
      A tuple of display, score
    """
    # We'll give em the benefit of the doubt here.
    if median == None or median == '':
      return 90, ''

    median = round(float(median))

    if self.key is 'testDisplay':
      # This is the benchmark test, so everything should be green here.
      bench = 100
    elif self.key is 'testVisibility':
      bench = 50
    elif self.key is 'testNonMatchingClass':
      # Since our supposition is that the test is 70% layout 30% selector,
      # We'll go with 50% here as an A
      bench = 50
    elif self.key is 'testFourClassReflows':
      bench = 120
    elif self.key is 'testFourScriptReflows':
      bench = 120
    elif self.key is 'testTwoScriptReflows':
      bench = 120
    elif self.key is 'testPaddingPx':
      bench = 120
    elif self.key is 'testPaddingLeftPx':
      bench = 120
    elif self.key is 'testFontSizeEm':
      bench = 120
    elif self.key is 'testWidthPercent':
      bench = 120
    elif self.key is 'testBackground':
      bench = 50
    elif self.key is 'testOverflowHidden':
      bench = 50
    elif self.key is 'testGetOffsetHeight':
      # Should we be pickier here that this should really be 0?
      bench = 50

    half = bench/2
    a = bench * 1.4
    b = bench * 2.4
    c = bench * 3.4
    d = bench * 4.4

    if median <= half:
      score = 100
      display = '0X'
    elif half < median <= a:
      score = 90
      display = '1X'
    elif a < median <= b:
      score = 80
      display = '2X'
    elif b < median <= c:
      score = 70
      display = '3X'
    elif c < median <= d:
      score = 60
      display = '4X'
    else:
     score = 50
     display = '>4X'
    #logging.info('%s, %s, %s' % (median, score, display))

    return score, display



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

  def ParseResults(self, results):
    """Re-scores the actual value against a baseline score for reflow.

    Sets the 1x reflow time for this test run and compares other times
    against that. This is to try to account for issues around selection
    bias, processor speed, etc...
    We'll preserve the original millisecond time as an expando value in case
    we want to do some calculations with it later.

    Args:
      results: a list of dicts.

    Returns:
      results: a list of dicts (with an expando key).
    """
    baseline_score = 0
    for result in results:
      if result['key'] == BASELINE_TEST_NAME:
        baseline_score = int(result['score'])
        break
    # Turn all values into some computed percentage of the baseline score.
    # This resets the score in the dict, but adds an expando to preserve the
    # original score's milliseconds value.
    for result in results:
      result['expando'] = int(result['score'])
      result['score'] = int(round(int(result['score']) / baseline_score) * 100)
    return results

TEST_SET = ReflowTestSet(
  category=_CATEGORY,
  category_name='Reflow',
  tests=_TESTS,
  subnav={
    'Test': '/%s/test' % _CATEGORY,
    'About': '/%s/about' % _CATEGORY
  },
  home_intro='''Reflow in a web browser refers to the process whereby the render engine calculates positions and geometries of elements in the document for purpose of drawing, or re-drawing, the visual presentation. Because reflow is a user-blocking operation in the browser, it is useful for developers to understand how to improve reflow times and also to understand the effects of various document properties (DOM nesting, CSS specificity, types of style changes) on reflow. <a href="/reflow/about">Read more about reflow and these tests.</a>''',
  # default_params=[
  # 'nested_anchors', 'num_elements=400', 'num_nest=4',
  # 'css_selector=%23g-content%20*', 'num_css_rules=1000',
  # 'css_text=border%3A%201px%20solid%20%230C0%3B%20padding%3A%208px%3B'],
  default_params=['acid1', 'num_elements=300'],
)
