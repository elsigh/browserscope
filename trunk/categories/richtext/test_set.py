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

"""Rich Text Test Definitions."""

__author__ = 'elsigh@google.com (Lindsey Simon)'

import logging

from categories import test_set_base


_CATEGORY = 'richtext'

class RichtextTest(test_set_base.TestBase):
  TESTS_URL_PATH = '/%s/test' % _CATEGORY
  CATEGORY = None  # None, 'apply', 'unapply', 'query', or 'change'

class CategoryRichtextTest(RichtextTest):
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

class IndividualRichtextTest(RichtextTest):
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


class ApplyRichtextTest(IndividualRichtextTest):
  CATEGORY = 'apply'

class UnapplyRichtextTest(IndividualRichtextTest):
  CATEGORY = 'unapply'

class QueryRichtextTest(IndividualRichtextTest):
  CATEGORY = 'query'

class ChangeRichtextTest(IndividualRichtextTest):
  CATEGORY = 'change'

CATEGORIES = sorted(['apply', 'unapply', 'query', 'change'])

_TESTS = (
  # key, name, doc
  CategoryRichtextTest('apply', 'Apply Formatting',
  '''These tests use execCommand to apply formatting to plain text.
  They simply run the execCommand and check if any HTML is generated around the
  selected text. They do not make a judgement call as to what the correct HTML
  should be, only that the given visual style is applied. So &lt;b&gt;,
  &lt;STRONG&gt;, and &lt;span style="font-weight:bold"&gt; are all considered
  valid output of the bold execCommand. The reason for this is that these tests
  are for WYSIWYG editing, not semantic editing. There are many execCommands
  which are not tested here; only the most commonly used commands for rich
  text editing are included. The output of the execCommand is shown in the last
  column of the test output.'''),
  CategoryRichtextTest('unapply', 'Unapply Formatting',
  '''These tests put different combinations of HTML into a contenteditable
  iframe, and then run an execCommand to attempt to remove the formatting the
  HTML applies. For example, there are tests to check if
  bold styling from &lt;b&gt;, &lt;strong&gt;, and &lt;span
  style="font-weight:normal"&gt; are all removed by the bold execCommand.
  It is important that browsers can remove all variations of a style, not just
  the variation the browser applies on its own, because it's quite possible
  that a web application could allow editing with multiple browsers, or that
  users could paste content into the contenteditable region.
  These tests currently only run with styleWithCSS set to false. Any HTML
  which remains after the execCommand runs is shown in the last column of the
  test output.'''),
  CategoryRichtextTest('change', 'Change Existing Formatting',
  '''These tests are similar to the unapply tests, except that they're for
  execCommands which take an argument (fontname, fontsize, etc.). They apply
  the execCommand to text which already has some formatting, in order to change
  it. After the execCommand runs, the tests find the text node which was
  selected, and climb up its ancestor chain to check that the given formatting
  is only applied once, and that it's the new format and not the old one. The
  last column of the test output shows the resulting HTML after applying the
  execCommand.'''),
  CategoryRichtextTest('query', 'Query Formatting State and Value',
  '''These tests run queryCommandState (for execCommands with no argument)
  and queryCommandValue (for execCommands with an argument) on HTML with
  various types of formatting.'''),

  # Individual tests
  # key, name
  ApplyRichtextTest('a-backcolor-0', 'backcolor execCommand on plaintext'),
  ApplyRichtextTest('a-backcolor-1', 'backcolor execCommand on plaintext, styleWithCSS=true'),
  ApplyRichtextTest('a-bold-0', 'bold execCommand on plaintext'),
  ApplyRichtextTest('a-bold-1', 'bold execCommand on plaintext, styleWithCSS=true'),
  ApplyRichtextTest('a-createbookmark-0', 'createbookmark execCommand on plaintext'),
  ApplyRichtextTest('a-createlink-0', 'createlink execCommand on plaintext'),
  ApplyRichtextTest('a-decreasefontsize-0', 'decreasefontsize execCommand on plaintext'),
  ApplyRichtextTest('a-fontname-0', 'fontname execCommand on plaintext'),
  ApplyRichtextTest('a-fontname-1', 'fontname execCommand on plaintext, styleWithCSS=true'),
  ApplyRichtextTest('a-fontsize-0', 'fontsize execCommand on plaintext'),
  ApplyRichtextTest('a-fontsize-1', 'fontsize execCommand on plaintext, styleWithCSS=true'),
  ApplyRichtextTest('a-forecolor-0', 'forecolor execCommand on plaintext'),
  ApplyRichtextTest('a-forecolor-1', 'forecolor execCommand on plaintext, styleWithCSS=true'),
  ApplyRichtextTest('a-formatblock-0', 'formatblock execCommand on plaintext'),
  ApplyRichtextTest('a-hilitecolor-0', 'hilitecolor execCommand on plaintext'),
  ApplyRichtextTest('a-hilitecolor-1', 'hilitecolor execCommand on plaintext, styleWithCSS=true'),
  ApplyRichtextTest('a-indent-0', 'indent execCommand on plaintext'),
  ApplyRichtextTest('a-indent-1', 'indent execCommand on plaintext, styleWithCSS=true'),
  ApplyRichtextTest('a-inserthorizontalrule-0', 'inserthorizontalrule execCommand on plaintext'),
  ApplyRichtextTest('a-inserthtml-0', 'inserthtml execCommand on plaintext'),
  ApplyRichtextTest('a-insertimage-0', 'insertimage execCommand on plaintext'),
  ApplyRichtextTest('a-insertorderedlist-0', 'insertorderedlist execCommand on plaintext'),
  ApplyRichtextTest('a-insertunorderedlist-0', 'insertunorderedlist execCommand on plaintext'),
  ApplyRichtextTest('a-italic-0', 'italic execCommand on plaintext'),
  ApplyRichtextTest('a-italic-1', 'italic execCommand on plaintext, styleWithCSS=true'),
  ApplyRichtextTest('a-justifycenter-0', 'justifycenter execCommand on plaintext'),
  ApplyRichtextTest('a-justifycenter-1', 'justifycenter execCommand on plaintext, styleWithCSS=true'),
  ApplyRichtextTest('a-justifyfull-0', 'justifyfull execCommand on plaintext'),
  ApplyRichtextTest('a-justifyfull-1', 'justifyfull execCommand on plaintext, styleWithCSS=true'),
  ApplyRichtextTest('a-justifyleft-0', 'justifyleft execCommand on plaintext'),
  ApplyRichtextTest('a-justifyleft-1', 'justifyleft execCommand on plaintext, styleWithCSS=true'),
  ApplyRichtextTest('a-justifyright-0', 'justifyright execCommand on plaintext'),
  ApplyRichtextTest('a-justifyright-1', 'justifyright execCommand on plaintext, styleWithCSS=true'),
  ApplyRichtextTest('a-strikethrough-0', 'strikethrough execCommand on plaintext'),
  ApplyRichtextTest('a-strikethrough-1', 'strikethrough execCommand on plaintext, styleWithCSS=true'),
  ApplyRichtextTest('a-subscript-0', 'subscript execCommand on plaintext'),
  ApplyRichtextTest('a-subscript-1', 'subscript execCommand on plaintext, styleWithCSS=true'),
  ApplyRichtextTest('a-superscript-0', 'superscript execCommand on plaintext'),
  ApplyRichtextTest('a-superscript-1', 'superscript execCommand on plaintext, styleWithCSS=true'),
  ApplyRichtextTest('a-underline-0', 'underline execCommand on plaintext'),
  ApplyRichtextTest('a-underline-1', 'underline execCommand on plaintext, styleWithCSS=true'),

  UnapplyRichtextTest('u-bold-0', 'bold execCommand on text surrounded by <b> tags'),
  UnapplyRichtextTest('u-bold-1', 'bold execCommand on text surrounded by <STRONG> tags'),
  UnapplyRichtextTest('u-bold-2', 'bold execCommand on text surrounded by font-weight:bold style'),
  UnapplyRichtextTest('u-italic-0', 'italic execCommand on text surrounded by <i> tags'),
  UnapplyRichtextTest('u-italic-1', 'italic execCommand on text surrounded by <EM> tags'),
  UnapplyRichtextTest('u-italic-2', 'italic execCommand on text surrounded by font-style:italic style'),
  UnapplyRichtextTest('u-outdent-0', 'outdent execCommand on blockquote generated by Firefox indent'),
  UnapplyRichtextTest('u-outdent-1', 'outdent execCommand on blockquote generated by webkit indent execCommand'),
  UnapplyRichtextTest('u-outdent-2', 'outdent execCommand on unordered list'),
  UnapplyRichtextTest('u-outdent-3', 'outdent execCommand on ordered list'),
  UnapplyRichtextTest('u-outdent-4', 'outdent execCommand on blockquote generated by Firefox indent (styleWithCSS on),'),
  UnapplyRichtextTest('u-removeformat-0', 'removeformat execCommand on text surrounded by <b> tags'),
  UnapplyRichtextTest('u-removeformat-1', 'removeformat execCommand on text surrounded by <a> tags'),
  UnapplyRichtextTest('u-removeformat-2', 'removeformat execCommand on text in table'),
  UnapplyRichtextTest('u-strikethrough-0', 'strikethrough execCommand on text surrounded by <strike> tag'),
  UnapplyRichtextTest('u-strikethrough-1', 'strikethrough execCommand on text surrounded by <s> tag'),
  UnapplyRichtextTest('u-strikethrough-2', 'strikethrough execCommand on text surrounded by <del> tag'),
  UnapplyRichtextTest('u-strikethrough-3', 'strikethrough execCommand on text surrounded by text-decoration:linethrough style'),
  UnapplyRichtextTest('u-subscript-0', 'subscript execCommand on text surrounded by <sub> tag'),
  UnapplyRichtextTest('u-subscript-1', 'subscript execCommand on text surrounded by vertical-align:sub style'),
  UnapplyRichtextTest('u-superscript-0', 'superscript execCommand on text surrounded by <sup> tag'),
  UnapplyRichtextTest('u-superscript-1', 'superscript execCommand on text surrounded by vertical-align:super style'),
  UnapplyRichtextTest('u-unbookmark-0', 'unbookmark execCommand on a bookmark created with createbookmark in IE'),
  UnapplyRichtextTest('u-underline-0', 'underline execCommand on text surrounded by <u> tags'),
  UnapplyRichtextTest('u-underline-1', 'underline execCommand on text surrounded by text-decoration:underline style'),
  UnapplyRichtextTest('u-unlink-0', 'unlink execCommand on a link created with createlink in IE'),

  QueryRichtextTest('q-backcolor-0', 'queryCommandValue for backcolor on <font> tag with background-color style'),
  QueryRichtextTest('q-backcolor-1', 'queryCommandValue for backcolor on <span> tag with background-color style generated by webkit'),
  QueryRichtextTest('q-backcolor-2', 'queryCommandValue for backcolor on <span> tag with background-color style'),
  QueryRichtextTest('q-bold-0', 'queryCommandState for bold on plain text'),
  QueryRichtextTest('q-bold-1', 'queryCommandState for bold on text surrounded by <b> tags'),
  QueryRichtextTest('q-bold-2', 'queryCommandState for bold on text surrounded by <STRONG> tags'),
  QueryRichtextTest('q-bold-3', 'queryCommandState for bold on text surrounded by font-weight:bold style'),
  QueryRichtextTest('q-bold-4', 'queryCommandState for bold on text surrounded by font-weight:normal style'),
  QueryRichtextTest('q-bold-5', 'queryCommandState for bold on text surrounded by b tag with font-weight:bold style'),
  QueryRichtextTest('q-fontname-0', 'queryCommandValue for fontname on <font> tag face attribute'),
  QueryRichtextTest('q-fontname-1', 'queryCommandValue for fontname on font-family style'),
  QueryRichtextTest('q-fontname-2', 'queryCommandValue for fontname on <font> tag with face attribute AND font-family style'),
  QueryRichtextTest('q-fontname-3', 'queryCommandValue for fontname on nested <font> tags with different face attributes'),
  QueryRichtextTest('q-fontname-4', 'queryCommandValue for fontname on <font> tag with face attribute surrounded by font-family style'),
  QueryRichtextTest('q-fontsize-0', 'queryCommandValue for fontsize on <font> tag size attribute'),
  QueryRichtextTest('q-fontsize-1', 'queryCommandValue for fontsize on font-size style'),
  QueryRichtextTest('q-fontsize-2', 'queryCommandValue for fontsize on <font> tag with size attribute AND font-size style'),
  QueryRichtextTest('q-forecolor-0', 'queryCommandValue for forecolor on <font> tag color attribute'),
  QueryRichtextTest('q-forecolor-1', 'queryCommandValue for forecolor on color style'),
  QueryRichtextTest('q-forecolor-2', 'queryCommandValue for forecolor on <font> tag with color attribute AND color style'),
  QueryRichtextTest('q-hilitecolor-0', 'queryCommandValue for hilitecolor on <font> tag with background-color style'),
  QueryRichtextTest('q-hilitecolor-1', 'queryCommandValue for hilitecolor on <span> tag with background-color style generated by webkit'),
  QueryRichtextTest('q-hilitecolor-2', 'queryCommandValue for hilitecolor on <span> tag with background-color style'),
  QueryRichtextTest('q-insertorderedlist-0', 'queryCommandState for insertorderedlist on plain text'),
  QueryRichtextTest('q-insertorderedlist-1', 'queryCommandState for insertorderedlist on ordered list'),
  QueryRichtextTest('q-insertorderedlist-2', 'queryCommandState for insertorderedlist on undordered list'),
  QueryRichtextTest('q-insertunorderedlist-0', 'queryCommandState for insertunorderedlist on plain text'),
  QueryRichtextTest('q-insertunorderedlist-1', 'queryCommandState for insertunorderedlist on ordered list'),
  QueryRichtextTest('q-insertunorderedlist-2', 'queryCommandState for insertunorderedlist on undordered list'),
  QueryRichtextTest('q-italic-0', 'queryCommandState for italic on plain text'),
  QueryRichtextTest('q-italic-1', 'queryCommandState for italic on text surrounded by <i> tags'),
  QueryRichtextTest('q-italic-2', 'queryCommandState for italic on text surrounded by <EM> tags'),
  QueryRichtextTest('q-italic-3', 'queryCommandState for italic on text surrounded by font-style:italic style'),
  QueryRichtextTest('q-italic-4', 'queryCommandState for italic on text surrounded by font-style:normal style italic tag'),
  QueryRichtextTest('q-justifycenter-0', 'queryCommandState for justifycenter on plain text'),
  QueryRichtextTest('q-justifycenter-1', 'queryCommandState for justifycenter on text centered by Firefox'),
  QueryRichtextTest('q-justifycenter-2', 'queryCommandState for justifycenter on text centered by IE'),
  QueryRichtextTest('q-justifycenter-3', 'queryCommandState for justifycenter on text centered by webkit'),
  QueryRichtextTest('q-justifyfull-0', 'queryCommandState for justifyfull on plain text'),
  QueryRichtextTest('q-justifyfull-1', 'queryCommandState for justifyfull on text justified by Firefox'),
  QueryRichtextTest('q-justifyfull-2', 'queryCommandState for justifyfull on text justified by IE'),
  QueryRichtextTest('q-justifyfull-3', 'queryCommandState for justifyfull on text justified by webkit'),
  QueryRichtextTest('q-justifyleft-0', 'queryCommandState for justifyleft on text left-aligned by Firefox'),
  QueryRichtextTest('q-justifyleft-1', 'queryCommandState for justifyleft on text left-aligned by IE'),
  QueryRichtextTest('q-justifyleft-2', 'queryCommandState for justifyleft on text left-aligned by webkit'),
  QueryRichtextTest('q-justifyright-0', 'queryCommandState for justifyright on plain text'),
  QueryRichtextTest('q-justifyright-1', 'queryCommandState for justifyright on text right-aligned by Firefox'),
  QueryRichtextTest('q-justifyright-2', 'queryCommandState for justifyright on text right-aligned by IE'),
  QueryRichtextTest('q-justifyright-3', 'queryCommandState for justifyright on text right-aligned by webkit'),
  QueryRichtextTest('q-strikethrough-0', 'queryCommandState for strikethrough on plain text'),
  QueryRichtextTest('q-strikethrough-1', 'queryCommandState for strikethrough on text surrounded by <strike> tag'),
  QueryRichtextTest('q-strikethrough-2', 'queryCommandState for strikethrough on text surrounded by <strike> tag with text-decoration:none style'),
  QueryRichtextTest('q-strikethrough-3', 'queryCommandState for strikethrough on text surrounded by <s> tag'),
  QueryRichtextTest('q-strikethrough-4', 'queryCommandState for strikethrough on text surrounded by <del> tag'),
  QueryRichtextTest('q-strikethrough-5', 'queryCommandState for strikethrough on text surrounded by b tag with text-decoration:line-through style'),
  QueryRichtextTest('q-subscript-0', 'queryCommandState for subscript on plain text'),
  QueryRichtextTest('q-subscript-1', 'queryCommandState for subscript on text surrounded by <sub> tag'),
  QueryRichtextTest('q-superscript-0', 'queryCommandState for superscript on plain text'),
  QueryRichtextTest('q-superscript-1', 'queryCommandState for superscript on text surrounded by <sup> tag'),
  QueryRichtextTest('q-underline-0', 'queryCommandState for underline on plain text'),
  QueryRichtextTest('q-underline-1', 'queryCommandState for underline on text surrounded by <u> tag'),
  QueryRichtextTest('q-underline-2', 'queryCommandState for underline on text surrounded by <a> tag'),
  QueryRichtextTest('q-underline-3', 'queryCommandState for underline on text surrounded by text-deocoration:undeline style'),
  QueryRichtextTest('q-underline-4', 'queryCommandState for underline on text surrounded by <u> tag with text-decoration:none style'),
  QueryRichtextTest('q-underline-5', 'queryCommandState for underline on text surrounded by <a> tag with text-decoration:none style'),

  ChangeRichtextTest('c-backcolor-0', 'backcolor execCommand on text surrounded by <font> tag with background-color style'),
  ChangeRichtextTest('c-backcolor-1', 'backcolor execCommand on text with background-color style generated by webkit'),
  ChangeRichtextTest('c-backcolor-2', 'backcolor execCommand on text with background-color style'),
  ChangeRichtextTest('c-fontname-0', 'fontname execCommand on text surrounded by <font> tag with face attribute'),
  ChangeRichtextTest('c-fontname-1', 'fontname execCommand on text with font-family style'),
  ChangeRichtextTest('c-fontname-2', 'fontname execCommand on text surrounded by <font> tag with face attribute AND font-family style'),
  ChangeRichtextTest('c-fontname-3', 'fontname execCommand on text surrounded by nested <font> tags with face attributes'),
  ChangeRichtextTest('c-fontname-4', 'fontname execCommand on text surrounded by <font> tag with face attribute inside font-family style'),
  ChangeRichtextTest('c-fontsize-0', 'fontsize execCommand on text surrounded by <font> tag with size attribute'),
  ChangeRichtextTest('c-fontsize-1', 'fontsize execCommand on text with font-size style'),
  ChangeRichtextTest('c-fontsize-2', 'fontsize execCommand on text surrounded by <font> tag with size attribute AND font-size style'),
  ChangeRichtextTest('c-forecolor-0', 'forecolor execCommand on text surrounded by <font> tag with color attribute'),
  ChangeRichtextTest('c-forecolor-1', 'forecolor execCommand on text with color style'),
  ChangeRichtextTest('c-forecolor-2', 'forecolor execCommand on text surrounded by <font> tag with color attribute AND color style'),
  ChangeRichtextTest('c-hilitecolor-0', 'hilitecolor execCommand on text surrounded by <font> tag with background-color style'),
  ChangeRichtextTest('c-hilitecolor-1', 'hilitecolor execCommand on text with background-color style generated by webkit'),
  ChangeRichtextTest('c-hilitecolor-2', 'hilitecolor execCommand on text with background-color style'),
)


class RichTextTestSet(test_set_base.TestSet):

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


TEST_SET = RichTextTestSet(
    category=_CATEGORY,
    category_name='Rich Text',
    summary_doc='Tests to see how well editor controls work with a variety of HTML.',
    tests=_TESTS,
)
