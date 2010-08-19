#!/usr/bin/python2.5
#
# Copyright 2010 Google Inc.
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

"""Rich Text 2 Test Definitions."""

__author__ = 'rolandsteiner@google.com (Roland Steiner)'

import logging

from categories import test_set_base

# common to the RichText2 suite
from categories.richtext2 import common

# tests
from categories.richtext2.tests.apply         import APPLY_TESTS
from categories.richtext2.tests.applyCSS      import APPLY_TESTS_CSS
from categories.richtext2.tests.change        import CHANGE_TESTS
from categories.richtext2.tests.changeCSS     import CHANGE_TESTS_CSS
from categories.richtext2.tests.delete        import DELETE_TESTS
from categories.richtext2.tests.forwarddelete import FORWARDDELETE_TESTS
from categories.richtext2.tests.insert        import INSERT_TESTS
from categories.richtext2.tests.query         import QUERY_TESTS
from categories.richtext2.tests.selection     import SELECTION_TESTS
from categories.richtext2.tests.unapply       import UNAPPLY_TESTS
from categories.richtext2.tests.unapplyCSS    import UNAPPLY_TESTS_CSS

class RichText2Test(test_set_base.TestBase):
  TESTS_URL_PATH = '/%s/test' % common.CATEGORY
  # Categories: None, 'apply', 'applyCSS', 'change', 'changeCSS', 'delete',
  # 'forwarddelete', 'insert', 'query', 'selection', unapply', 'unapplyCSS'
  CATEGORY = None

class CategoryRichText2Test(RichText2Test):
  def __init__(self, key, name, doc):
    """Initialze a test.

    Args:
      key: key for this in dict's
      name: a human readable label for display
      doc: a description of the test
    """
    # This way we can assign tests to a test group, i.e. apply, unapply, etc..
    test_set_base.TestBase.__init__(
        self,
        key=key,
        name=name,
        url=self.TESTS_URL_PATH,
        doc=doc,
        min_value=0,
        max_value=100,
        cell_align='center')

class IndividualRichText2Test(RichText2Test):
  def __init__(self, key, name):
    """Initialze a test.

    Args:
      key: key for this in dict's
      name: a human readable label for display
    """
    test_set_base.TestBase.__init__(
        self,
        key=key,
        name=name,
        url=self.TESTS_URL_PATH,
        doc=None,
        min_value=0,
        max_value=1,
        is_hidden_stat=True)


class SelectionRichText2Test(IndividualRichText2Test):
  CATEGORY = 'selection'

class ApplyRichText2Test(IndividualRichText2Test):
  CATEGORY = 'apply'

class ApplyCSSRichText2Test(IndividualRichText2Test):
  CATEGORY = 'applyCSS'

class ChangeRichText2Test(IndividualRichText2Test):
  CATEGORY = 'change'

class ChangeCSSRichText2Test(IndividualRichText2Test):
  CATEGORY = 'changeCSS'

class UnapplyRichText2Test(IndividualRichText2Test):
  CATEGORY = 'unapply'

class UnapplyCSSRichText2Test(IndividualRichText2Test):
  CATEGORY = 'unapplyCSS'

class DeleteRichText2Test(IndividualRichText2Test):
  CATEGORY = 'delete'

class ForwardDeleteRichText2Test(IndividualRichText2Test):
  CATEGORY = 'forwarddelete'

class InsertRichText2Test(IndividualRichText2Test):
  CATEGORY = 'insert'

class QueryRichText2Test(IndividualRichText2Test):
  CATEGORY = 'query'

CATEGORIES = sorted(['selection', 'apply', 'applyCSS', 'change', 'changeCSS', 'unapply', 'unapplyCSS', 'delete', 'forwarddelete', 'insert', 'query'])

# Category tests:
# key, name, doc

_CATEGORIES_TEST_SET = [
  CategoryRichText2Test('selection', 'Selection',
  '''These tests verify that selection commands are honored correctly.
  The expected and actual outputs are shown.'''),

  CategoryRichText2Test('apply', 'Apply Format',
  '''These tests use execCommand to apply formatting to plain text,
  with styleWithCSS being set to false.
  The expected and actual outputs are shown.'''),

  CategoryRichText2Test('applyCSS', 'Apply Format, styleWithCSS',
  '''These tests use execCommand to apply formatting to plain text,
  with styleWithCSS being set to true.
  The expected and actual outputs are shown.'''),

  CategoryRichText2Test('change', 'Change Existing Format',
  '''These tests are similar to the unapply tests, except that they're for
  execCommands which take an argument (fontname, fontsize, etc.). They apply
  the execCommand to text which already has some formatting, in order to change
  it. styleWithCSS is being set to false.
  The expected and actual outputs are shown.'''),

  CategoryRichText2Test('changeCSS', 'Change Existing Format, styleWithCSS',
  '''These tests are similar to the unapply tests, except that they're for
  execCommands which take an argument (fontname, fontsize, etc.). They apply
  the execCommand to text which already has some formatting, in order to change
  it. styleWithCSS is being set to true.
  The expected and actual outputs are shown.'''),

  CategoryRichText2Test('unapply', 'Unapply Format',
  '''These tests put different combinations of HTML into a contenteditable
  iframe, and then run an execCommand to attempt to remove the formatting the
  HTML applies. For example, there are tests to check if
  bold styling from &lt;b&gt;, &lt;strong&gt;, and &lt;span
  style="font-weight:normal"&gt; are all removed by the bold execCommand.
  It is important that browsers can remove all variations of a style, not just
  the variation the browser applies on its own, because it's quite possible
  that a web application could allow editing with multiple browsers, or that
  users could paste content into the contenteditable region.
  For these tests, styleWithCSS is set to false.
  The expected and actual outputs are shown.'''),

  CategoryRichText2Test('unapplyCSS', 'Unapply Format, styleWithCSS',
  '''These tests put different combinations of HTML into a contenteditable
  iframe, and then run an execCommand to attempt to remove the formatting the
  HTML applies. For example, there are tests to check if
  bold styling from &lt;b&gt;, &lt;strong&gt;, and &lt;span
  style="font-weight:normal"&gt; are all removed by the bold execCommand.
  It is important that browsers can remove all variations of a style, not just
  the variation the browser applies on its own, because it's quite possible
  that a web application could allow editing with multiple browsers, or that
  users could paste content into the contenteditable region.
  For these tests, styleWithCSS is set to true.
  The expected and actual outputs are shown.'''),

  CategoryRichText2Test('delete', 'Delete Content',
  '''These tests verify that 'delete' commands are executed correctly.
  Note that 'delete' commands are supposed to have the same result as if the
  user had hit the 'BackSpace' (NOT 'Delete'!) key.
  The expected and actual outputs are shown.'''),

  CategoryRichText2Test('forwarddelete', 'Forward-Delete Content',
  '''These tests verify that 'forwarddelete' commands are executed correctly.
  Note that 'forwarddelete' commands are supposed to have the same result as if
  the user had hit the 'Delete' key.
  The expected and actual outputs are shown.'''),

  CategoryRichText2Test('insert', 'Insert Content',
  '''These tests verify that the various 'insert' and 'create' commands, that
  create a single HTML element, rather than wrapping existing content, are
  executed correctly. (Commands that wrap existing HTML are part of the 'apply'
  and 'applyCSS' categories.)
  The expected and actual outputs are shown.'''),

  CategoryRichText2Test('query', 'Query Functions',
  '''These tests verify that the various 'queryCommand...()' functions return
  a correct result given a certain set-up.
  The expected and actual results are shown.''')
]

def createID(suite, testname):
  return common.TEST_ID_PREFIX + '-' + suite['id'] + '-' + testname;
  
# Individual tests:
# key, name

_SELECTION_TEST_SET = [
    SelectionRichText2Test(createID(SELECTION_TESTS, t['id']), t['desc'])
        for c in common.CLASSES
            for t in SELECTION_TESTS.get(c, {})
]
_APPLY_TEST_SET = [
    ApplyRichText2Test(createID(APPLY_TESTS, t['id']), t['desc'])
        for c in common.CLASSES
            for t in APPLY_TESTS.get(c, {})
]
_APPLY_CSS_TEST_SET = [
    ApplyCSSRichText2Test(createID(APPLY_TESTS_CSS, t['id']), t['desc'])
        for c in common.CLASSES
            for t in APPLY_TESTS_CSS.get(c, {})
]
_CHANGE_TEST_SET = [
    ChangeRichText2Test(createID(CHANGE_TESTS, t['id']), t['desc'])
        for c in common.CLASSES
            for t in CHANGE_TESTS.get(c, {})
]
_CHANGE_CSS_TEST_SET = [
    ChangeCSSRichText2Test(createID(CHANGE_TESTS_CSS, t['id']), t['desc'])
        for c in common.CLASSES
            for t in CHANGE_TESTS_CSS.get(c, {})
]
_UNAPPLY_TEST_SET = [
    UnapplyRichText2Test(createID(UNAPPLY_TESTS, t['id']), t['desc'])
        for c in common.CLASSES
            for t in UNAPPLY_TESTS.get(c, {})
]
_UNAPPLY_CSS_TEST_SET = [
    UnapplyCSSRichText2Test(createID(UNAPPLY_TESTS_CSS, t['id']), t['desc'])
        for c in common.CLASSES
            for t in UNAPPLY_TESTS_CSS.get(c, {})
]
_DELETE_TEST_SET = [
    DeleteRichText2Test(createID(DELETE_TESTS, t['id']), t['desc'])
        for c in common.CLASSES
            for t in DELETE_TESTS.get(c, {})
]
_FORWARDDELETE_TEST_SET = [
    ForwardDeleteRichText2Test(createID(FORWARDDELETE_TESTS, t['id']), t['desc'])
        for c in common.CLASSES 
            for t in FORWARDDELETE_TESTS.get(c, {})
]
_INSERT_TEST_SET = [
    InsertRichText2Test(createID(INSERT_TESTS, t['id']), t['desc'])
        for c in common.CLASSES
            for t in INSERT_TESTS.get(c, {})
]
_QUERY_TEST_SET = [
    QueryRichText2Test(createID(QUERY_TESTS, t['id']), t['desc'])
        for c in common.CLASSES
            for t in QUERY_TESTS.get(c, {})
]

_FULL_TEST_SET = _CATEGORIES_TEST_SET + \
                 _SELECTION_TEST_SET + \
                 _APPLY_TEST_SET + \
                 _APPLY_CSS_TEST_SET + \
                 _CHANGE_TEST_SET + \
                 _CHANGE_CSS_TEST_SET + \
                 _UNAPPLY_TEST_SET + \
                 _UNAPPLY_CSS_TEST_SET + \
                 _DELETE_TEST_SET + \
                 _FORWARDDELETE_TEST_SET + \
                 _INSERT_TEST_SET + \
                 _QUERY_TEST_SET

class RichText2TestSet(test_set_base.TestSet):

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
    category_tests = self.GetTestsByCategory(test_key)
    num_tests = len(category_tests)
    if sorted(raw_scores.keys()) == CATEGORIES:
      display_score = int(raw_scores[test_key])
    else:
      display_score = 0
      for category_test in category_tests:
        raw_score = raw_scores.get(category_test.key)
        if raw_score is None:
          # This could happen if we don't have any results for a new test.
          num_tests -= 1
        else:
          display_score += raw_score

    if num_tests <= 0:
      # This really should not happen.
      num_tests = 1
      score = 0
    else:
      score = int(round(100.0 * display_score / num_tests))
    display = '%s/%s' % (display_score, num_tests)
    return score, display

  def GetTestsByCategory(self, category):
    return [test for test in self.tests if test.CATEGORY == category]

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
    total_passed = 0
    total_tests = 0
    for test_key, test_results in results.items():
      display = test_results['display']
      if display == '':
        # If we ever see display == '', we know we can just walk away.
        return 0, ''
      passed, total = display.split('/')
      total_passed += int(passed)
      total_tests += int(total)
    score = int(round(100.0 * total_passed / total_tests))
    display = '%s/%s' % (total_passed, total_tests)
    return score, display


TEST_SET = RichText2TestSet(
    category=common.CATEGORY,
    category_name='Rich Text 2',
    summary_doc='New suite of tests to see how well editor controls work with a variety of HTML.',
    tests=_FULL_TEST_SET,
    test_page="richtext2/run",
)
