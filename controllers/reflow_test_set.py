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


from controllers import test_set_base


_CATEGORY = 'reflow'


class ReflowTest(object):
  TESTS_URL_PATH = '/%s/test' % _CATEGORY
  def __init__(self, key, name, doc):
    self.key = key
    self.name = name
    self.url = '%s?t=%s' % (self.TESTS_URL_PATH, key)
    self.score_type = 'custom'
    self.doc = doc
    self.min_value, self.max_value = 0, 60000

  def GetScoreAndDisplayValue(self, median):
    """Returns a tuple with display text for the cell as well as a 1-100 value.
    i.e. ('1X', 95)
    Args:
      median: The test median.
    Returns:
      A tuple of display, score
    """
    if not median:
      return 0, '0.0'
    time = round(float(median) / 1000.0, 1)
    abc = (1, 2, 3, 4)
    if self.key is 'testDisplay':
      abc = (.3, .5, 1, 1.5)
    elif self.key is 'testVisibility':
      abc = (.4, .7, 1.1, 1.6)
    elif self.key is 'testNonMatchingClass':
      abc = (.6, 1, 2, 3)
    elif self.key is 'testFourClassReflows':
      abc = (.6, 1, 2, 3)
    elif self.key is 'testFourScriptReflows':
      abc = (.6, 1, 2, 3)
    elif self.key is 'testTwoScriptReflows':
      abc = (.6, 1, 2, 3)
    elif self.key is 'testPaddingPx':
      abc = (.6, 1, 2, 3)
    elif self.key is 'testPaddingLeftPx':
      abc = (.6, 1, 1.5, 2)
    elif self.key is 'testFontSizeEm':
      abc = (.6, 1, 2, 3)
    elif self.key is 'testWidthPercent':
      abc = (.6, 1, 2, 3)
    elif self.key is 'testBackground':
      abc = (.6, 1, 2, 3)
    elif self.key is 'testOverflowHidden':
      abc = (.6, 1, 2, 3)
    elif self.key is 'testSelectorMatchTime':
      abc = (.6, 1, 1.5, 2)
    elif self.key is 'testGetOffsetHeight':
      abc = (.1, .2, .3, .4)
    score = self._GetScore(time, abc)
    #logging.info('CustomTestsFunction w/ %s, %s' % (test, median))
    #logging.info('TEST!! %s, %s, %s' % (test, time, score))
    return score, str(time)

  @staticmethod
  def _GetScore(time, abc):
    """Computes an A/B/C/D/F-like score out of 100.

    Args:
      time: a float to score
      abc: (a_cutoff, b_cutoff, c_cutoff, d_cutoff)
    """
    # Make the score proportional to where the time falls in the abc ranges.
    if time <= abc[0]:
      score = int(round(90.0 + (abc[0] - time) / abc[0] * 10))             # A
    elif abc[0] < time <= abc[1]:
      score = int(round(80.0 + (abc[1] - time) / (abc[1] - abc[0]) * 10))  # B
    elif abc[1] < time <= abc[2]:
      score = int(round(70.0 + (abc[2] - time) / (abc[2] - abc[1]) * 10))  # C
    elif abc[2] < time <= abc[3]:
      score = int(round(60.0 + (abc[3] - time) / (abc[3] - abc[2]) * 10))  # D
    else:
      score = 10  # F
    return score


_TESTS = (
  # key, name, doc
  ReflowTest('testDisplay', 'Display Block',
    '''This test takes an element and sets its
    style.display="none". According to our friends at Mozilla this has
    the effect of taking an element out of the browser's "render tree" -
    the in-memory representation of all of results of
    geometry/positioning calculations for that particular
    element. Setting an element to display="none" has the additional
    effect of removing all of an elements children from the render tree
    as well. Next, the test resets the element's style.display="", which
    sets the element's display back to its original value. Our thinking
    was that this operation ought to approximate the cost of reflowing
    an element on a particular page since the browser would have to
    recalculate all the positions and sizes for every child within the
    element as well as make any changes to the overall document that
    this change would cause to parents and ancestors. This was
    originally the only test that the Reflow Timer performed, but as you
    can see from the results, we discovered that not all render engines
    work like Gecko's and so we began adding more tests.'''),
  ReflowTest('testVisibility', 'Visiblility None',
    '''Much like the display test above, this test sets an element's
    style.visibility="hidden" and then resets it back to its default,
    which is visible. Visually this has the same effect as setting
    display="none", however this change should be significantly less
    costly for the browser to perform as it should not need be purging
    the element from the render tree and recalculating
    geometries.'''),
  ReflowTest('testNonMatchingClass', 'Non Matching by Class',
    '''This test adds a class name to an element, and more specifically a
    class name which is not present in the document's CSS object
    model.'''),
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
  ReflowTest('testSelectorMatchTime', 'Selector Match Time',
    '''In the world of reflow, one of the possible operations that can
    eat up time occurs when an element gets a new class name and the
    render engine has to look through the CSSOM to see if this element
    now matches some CSS declaration. The goal of this test is to try
    to cause this match operation without causing any change to the
    render tree. The test is much like the Non-Matching Class test,
    except that instead of flushing the render queue before this test,
    we try to simply flush any style computations. The way it works is
    to make a CSS rule that can get activated by virtue of an
    attribute selector but which will never cause reflow because it
    will never match any element in the render tree. For instance
    "body[bogusattr='bogusval'] html {color:pink}". We note that this
    test seems not to work in engines other than Gecko at this
    time.'''),
  ReflowTest('testGetOffsetHeight', 'Do Nothing / OffsetHeight',
    '''This test does nothing other than the request for offsetHeight
    after already having done so. Theoretically, this test is
    something like a control for our test and should have a 0 or very
    low time.'''),
)


TEST_SET = test_set_base.TestSet(
    category=_CATEGORY,
    category_name='Reflow',
    tests=_TESTS,
    subnav={
      'Test': '/%s/test' % _CATEGORY,
      'About': '/%s/about' % _CATEGORY
    },
    home_intro='''Reflow in a web browser refers to the process whereby the render engine calculates positions and geometries of elements in the document for purpose of drawing, or re-drawing, the visual presentation. Because reflow is a user-blocking operation in the browser, it is useful for developers to understand how to improve reflow times and also to understand the effects of various document properties (DOM nesting, CSS specificity, types of style changes) on reflow. <a href="/reflow/about">Read more about reflow and these tests.</a>''',
    default_params=[
    'nested_anchors', 'num_elements=400', 'num_nest=4',
    'css_selector=%23g-content%20*', 'num_css_rules=1000',
    'css_text=border%3A%201px%20solid%20%230C0%3B%20padding%3A%208px%3B'],
)
