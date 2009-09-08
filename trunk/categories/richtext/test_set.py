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

"""Rich Text Test Definitions."""

__author__ = 'elsigh@google.com (Lindsey Simon)'

import logging

from categories import test_set_base


_CATEGORY = 'richtext'


class RichtextTest(test_set_base.TestBase):
  TESTS_URL_PATH = '/%s/test' % _CATEGORY

  def __init__(self, key, name, doc, is_hidden_stat=True, category=None,
               score_type='boolean'):
    """Initialze a test.

    Args:
      key: key for this in dict's
      name: a human readable label for display
      url_name: the name used in the url
      score_type: 'boolean' or 'custom'
      doc: a description of the test
      value_range: (min_value, max_value) as integer values
      is_hidden_stat: whether or not the test shown in the stats table
      category: the category(aka non-hidden test) this test belongs to.
      score_type: string, boolean or custom.
    """
    self.is_hidden_stat = is_hidden_stat
    # This way we can assign tests to a test group, i.e. apply, unapply, etc..
    self.category = category
    test_set_base.TestBase.__init__(
        self,
        key=key,
        name=name,
        url=self.TESTS_URL_PATH,
        score_type=score_type,
        doc=doc,
        min_value=0,
        max_value=1)


  def GetScoreAndDisplayValue(self, median, medians, is_uri_result=False):
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
    #logging.info('RichTextTest.GetScoreAndDisplayValue '
    #             'test: %s, median: %s, medians: %s, '
    #             'is_uri_result: %s' %
    #             (self.key, median, medians, is_uri_result))

    tests_in_category = self.GetTestsByCategory(self.key)
    num_tests = len(tests_in_category)

    if is_uri_result:
      display_score = int(median)
    else:
      display_score = 0
      for test in tests_in_category:
        test_median = medians[test.key]
        #logging.info('test_median: %s' % test_median)
        # If test_median is None, we need to be fair and decrement num_tests.
        # This could happen if we don't have any results for a new test.
        if test_median is None:
          num_tests -= 1
        else:
          display_score += test_median

    score = int(display_score / num_tests)
    display = '%s/%s' % (display_score, num_tests)
    return score, display


  def GetTestsByCategory(self, category):
    tests = []
    for test in _TESTS:
      if test.category == category:
        tests.append(test)
    return tests

_TESTS = (
  # key, name, doc
  RichtextTest('apply', 'Apply Formatting',
  '''These tests use execCommand to apply formatting to plain text.
  They simply run the execCommand and check if any HTML is generated around the
  selected text. They do not make a judgement call as to what the correct HTML
  should be, only that the given visual style is applied. So &lt;b&gt;,
  &lt;STRONG&gt;, and &lt;span style="font-weight:bold"&gt; are all considered
  valid output of the bold execCommand. The reason for this is that these tests
  are for WYSIWYG editing, not semantic editing. There are many execCommands
  which are not tested here; only the most commonly used commands for rich
  text editing are included. The output of the execCommand is shown in the last
  column of the test output.''',
  is_hidden_stat=False, score_type='custom'),
  RichtextTest('unapply', 'Un-Apply Formatting',
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
  test output.''',
  is_hidden_stat=False, score_type='custom'),
  RichtextTest('change', 'Change Existing Formatting',
  '''These tests are similar to the unapply tests, except that they're for
  execCommands which take an argument (fontname, fontsize, etc.). They apply
  the execCommand to text which already has some formatting, in order to change
  it. After the execCommand runs, the tests find the text node which was
  selected, and climb up its ancestor chain to check that the given formatting
  is only applied once, and that it's the new format and not the old one. The
  last column of the test output shows the resulting HTML after applying the
  execCommand.''',
  is_hidden_stat=False, score_type='custom'),
  RichtextTest('query', 'Query State and Value',
  '''These tests run queryCommandState (for execCommands with no argument)
  and queryCommandValue (for execCommands with an argument) on HTML with
  various types of formatting.''',
  is_hidden_stat=False, score_type='custom'),
  # Individual tests
  RichtextTest('a-backcolor-0', 'backcolor execCommand on plaintext', None, category='apply'),
  RichtextTest('a-backcolor-1', 'backcolor execCommand on plaintext, styleWithCSS=true', None, category='apply'),
  RichtextTest('a-bold-0', 'bold execCommand on plaintext', None, category='apply'),
  RichtextTest('a-bold-1', 'bold execCommand on plaintext, styleWithCSS=true', None, category='apply'),
  RichtextTest('a-createbookmark-0', 'createbookmark execCommand on plaintext', None, category='apply'),
  RichtextTest('a-createlink-0', 'createlink execCommand on plaintext', None, category='apply'),
  RichtextTest('a-decreasefontsize-0', 'decreasefontsize execCommand on plaintext', None, category='apply'),
  RichtextTest('a-fontname-0', 'fontname execCommand on plaintext', None, category='apply'),
  RichtextTest('a-fontname-1', 'fontname execCommand on plaintext, styleWithCSS=true', None, category='apply'),
  RichtextTest('a-fontsize-0', 'fontsize execCommand on plaintext', None, category='apply'),
  RichtextTest('a-fontsize-1', 'fontsize execCommand on plaintext, styleWithCSS=true', None, category='apply'),
  RichtextTest('a-forecolor-0', 'forecolor execCommand on plaintext', None, category='apply'),
  RichtextTest('a-forecolor-1', 'forecolor execCommand on plaintext, styleWithCSS=true', None, category='apply'),
  RichtextTest('a-formatblock-0', 'formatblock execCommand on plaintext', None, category='apply'),
  RichtextTest('a-hilitecolor-0', 'hilitecolor execCommand on plaintext', None, category='apply'),
  RichtextTest('a-hilitecolor-1', 'hilitecolor execCommand on plaintext, styleWithCSS=true', None, category='apply'),
  RichtextTest('a-indent-0', 'indent execCommand on plaintext', None, category='apply'),
  RichtextTest('a-indent-1', 'indent execCommand on plaintext, styleWithCSS=true', None, category='apply'),
  RichtextTest('a-inserthorizontalrule-0', 'inserthorizontalrule execCommand on plaintext', None, category='apply'),
  RichtextTest('a-inserthtml-0', 'inserthtml execCommand on plaintext', None, category='apply'),
  RichtextTest('a-insertimage-0', 'insertimage execCommand on plaintext', None, category='apply'),
  RichtextTest('a-insertorderedlist-0', 'insertorderedlist execCommand on plaintext', None, category='apply'),
  RichtextTest('a-insertunorderedlist-0', 'insertunorderedlist execCommand on plaintext', None, category='apply'),
  RichtextTest('a-insertparagraph-0', 'insertparagraph execCommand on plaintext', None, category='apply'),
  RichtextTest('a-italic-0', 'italic execCommand on plaintext', None, category='apply'),
  RichtextTest('a-italic-1', 'italic execCommand on plaintext, styleWithCSS=true', None, category='apply'),
  RichtextTest('a-justifycenter-0', 'justifycenter execCommand on plaintext', None, category='apply'),
  RichtextTest('a-justifycenter-1', 'justifycenter execCommand on plaintext, styleWithCSS=true', None, category='apply'),
  RichtextTest('a-justifyfull-0', 'justifyfull execCommand on plaintext', None, category='apply'),
  RichtextTest('a-justifyfull-1', 'justifyfull execCommand on plaintext, styleWithCSS=true', None, category='apply'),
  RichtextTest('a-justifyleft-0', 'justifyleft execCommand on plaintext', None, category='apply'),
  RichtextTest('a-justifyleft-1', 'justifyleft execCommand on plaintext, styleWithCSS=true', None, category='apply'),
  RichtextTest('a-justifyright-0', 'justifyright execCommand on plaintext', None, category='apply'),
  RichtextTest('a-justifyright-1', 'justifyright execCommand on plaintext, styleWithCSS=true', None, category='apply'),
  RichtextTest('a-strikethrough-0', 'strikethrough execCommand on plaintext', None, category='apply'),
  RichtextTest('a-strikethrough-1', 'strikethrough execCommand on plaintext, styleWithCSS=true', None, category='apply'),
  RichtextTest('a-subscript-0', 'subscript execCommand on plaintext', None, category='apply'),
  RichtextTest('a-subscript-1', 'subscript execCommand on plaintext, styleWithCSS=true', None, category='apply'),
  RichtextTest('a-superscript-0', 'superscript execCommand on plaintext', None, category='apply'),
  RichtextTest('a-superscript-1', 'superscript execCommand on plaintext, styleWithCSS=true', None, category='apply'),
  RichtextTest('a-underline-0', 'underline execCommand on plaintext', None, category='apply'),
  RichtextTest('a-underline-1', 'underline execCommand on plaintext, styleWithCSS=true', None, category='apply'),
  RichtextTest('u-bold-0', 'bold execCommand on text surrounded by <b> tags', None, category='unapply'),
  RichtextTest('u-bold-1', 'bold execCommand on text surrounded by <STRONG> tags', None, category='unapply'),
  RichtextTest('u-bold-2', 'bold execCommand on text surrounded by font-weight:bold style', None, category='unapply'),
  RichtextTest('u-italic-0', 'italic execCommand on text surrounded by <i> tags', None, category='unapply'),
  RichtextTest('u-italic-1', 'italic execCommand on text surrounded by <EM> tags', None, category='unapply'),
  RichtextTest('u-italic-2', 'italic execCommand on text surrounded by font-style:italic style', None, category='unapply'),
  RichtextTest('u-outdent-0', 'outdent execCommand on blockquote generated by Firefox indent', None, category='unapply'),
  RichtextTest('u-outdent-1', 'outdent execCommand on blockquote generated by webkit indent execCommand', None, category='unapply'),
  RichtextTest('u-outdent-2', 'outdent execCommand on unordered list', None, category='unapply'),
  RichtextTest('u-outdent-3', 'outdent execCommand on ordered list', None, category='unapply'),
  RichtextTest('u-outdent-4', 'outdent execCommand on blockquote generated by Firefox indent (styleWithCSS on),', None, category='unapply'),
  RichtextTest('u-removeformat-0', 'removeformat execCommand on text surrounded by <b> tags', None, category='unapply'),
  RichtextTest('u-removeformat-1', 'removeformat execCommand on text surrounded by <a> tags', None, category='unapply'),
  RichtextTest('u-removeformat-2', 'removeformat execCommand on text in table', None, category='unapply'),
  RichtextTest('u-strikethrough-0', 'strikethrough execCommand on text surrounded by <strike> tag', None, category='unapply'),
  RichtextTest('u-strikethrough-1', 'strikethrough execCommand on text surrounded by <s> tag', None, category='unapply'),
  RichtextTest('u-strikethrough-2', 'strikethrough execCommand on text surrounded by <del> tag', None, category='unapply'),
  RichtextTest('u-strikethrough-3', 'strikethrough execCommand on text surrounded by text-decoration:linethrough style', None, category='unapply'),
  RichtextTest('u-subscript-0', 'subscript execCommand on text surrounded by <sub> tag', None, category='unapply'),
  RichtextTest('u-subscript-1', 'subscript execCommand on text surrounded by vertical-align:sub style', None, category='unapply'),
  RichtextTest('u-superscript-0', 'superscript execCommand on text surrounded by <sup> tag', None, category='unapply'),
  RichtextTest('u-superscript-1', 'superscript execCommand on text surrounded by vertical-align:super style', None, category='unapply'),
  RichtextTest('u-unbookmark-0', 'unbookmark execCommand on a bookmark created with createbookmark in IE', None, category='unapply'),
  RichtextTest('u-underline-0', 'underline execCommand on text surrounded by <u> tags', None, category='unapply'),
  RichtextTest('u-underline-1', 'underline execCommand on text surrounded by text-decoration:underline style', None, category='unapply'),
  RichtextTest('u-unlink-0', 'unlink execCommand on a link created with createlink in IE', None, category='unapply'),
  RichtextTest('q-backcolor-0', 'queryCommandValue for backcolor on <font> tag with background-color style', None, category='query'),
  RichtextTest('q-backcolor-1', 'queryCommandValue for backcolor on <span> tag with background-color style generated by webkit', None, category='query'),
  RichtextTest('q-backcolor-2', 'queryCommandValue for backcolor on <span> tag with background-color style', None, category='query'),
  RichtextTest('q-bold-0', 'queryCommandState for bold on plain text', None, category='query'),
  RichtextTest('q-bold-1', 'queryCommandState for bold on text surrounded by <b> tags', None, category='query'),
  RichtextTest('q-bold-2', 'queryCommandState for bold on text surrounded by <STRONG> tags', None, category='query'),
  RichtextTest('q-bold-3', 'queryCommandState for bold on text surrounded by font-weight:bold style', None, category='query'),
  RichtextTest('q-bold-4', 'queryCommandState for bold on text surrounded by font-weight:normal style', None, category='query'),
  RichtextTest('q-bold-5', 'queryCommandState for bold on text surrounded by b tag with font-weight:bold style', None, category='query'),
  RichtextTest('q-fontname-0', 'queryCommandValue for fontname on <font> tag face attribute', None, category='query'),
  RichtextTest('q-fontname-1', 'queryCommandValue for fontname on font-family style', None, category='query'),
  RichtextTest('q-fontname-2', 'queryCommandValue for fontname on <font> tag with face attribute AND font-family style', None, category='query'),
  RichtextTest('q-fontname-3', 'queryCommandValue for fontname on nested <font> tags with different face attributes', None, category='query'),
  RichtextTest('q-fontname-4', 'queryCommandValue for fontname on <font> tag with face attribute surrounded by font-family style', None, category='query'),
  RichtextTest('q-fontsize-0', 'queryCommandValue for fontsize on <font> tag size attribute', None, category='query'),
  RichtextTest('q-fontsize-1', 'queryCommandValue for fontsize on font-size style', None, category='query'),
  RichtextTest('q-fontsize-2', 'queryCommandValue for fontsize on <font> tag with size attribute AND font-size style', None, category='query'),
  RichtextTest('q-forecolor-0', 'queryCommandValue for forecolor on <font> tag color attribute', None, category='query'),
  RichtextTest('q-forecolor-1', 'queryCommandValue for forecolor on color style', None, category='query'),
  RichtextTest('q-forecolor-2', 'queryCommandValue for forecolor on <font> tag with color attribute AND color style', None, category='query'),
  RichtextTest('q-hilitecolor-0', 'queryCommandValue for hilitecolor on <font> tag with background-color style', None, category='query'),
  RichtextTest('q-hilitecolor-1', 'queryCommandValue for hilitecolor on <span> tag with background-color style generated by webkit', None, category='query'),
  RichtextTest('q-hilitecolor-2', 'queryCommandValue for hilitecolor on <span> tag with background-color style', None, category='query'),
  RichtextTest('q-insertorderedlist-0', 'queryCommandState for insertorderedlist on plain text', None, category='query'),
  RichtextTest('q-insertorderedlist-1', 'queryCommandState for insertorderedlist on ordered list', None, category='query'),
  RichtextTest('q-insertorderedlist-2', 'queryCommandState for insertorderedlist on undordered list', None, category='query'),
  RichtextTest('q-insertunorderedlist-0', 'queryCommandState for insertunorderedlist on plain text', None, category='query'),
  RichtextTest('q-insertunorderedlist-1', 'queryCommandState for insertunorderedlist on ordered list', None, category='query'),
  RichtextTest('q-insertunorderedlist-2', 'queryCommandState for insertunorderedlist on undordered list', None, category='query'),
  RichtextTest('q-italic-0', 'queryCommandState for italic on plain text', None, category='query'),
  RichtextTest('q-italic-1', 'queryCommandState for italic on text surrounded by <i> tags', None, category='query'),
  RichtextTest('q-italic-2', 'queryCommandState for italic on text surrounded by <EM> tags', None, category='query'),
  RichtextTest('q-italic-3', 'queryCommandState for italic on text surrounded by font-style:italic style', None, category='query'),
  RichtextTest('q-italic-4', 'queryCommandState for italic on text surrounded by font-style:normal style italic tag', None, category='query'),
  RichtextTest('q-justifycenter-0', 'queryCommandState for justifycenter on plain text', None, category='query'),
  RichtextTest('q-justifycenter-1', 'queryCommandState for justifycenter on text centered by Firefox', None, category='query'),
  RichtextTest('q-justifycenter-2', 'queryCommandState for justifycenter on text centered by IE', None, category='query'),
  RichtextTest('q-justifycenter-3', 'queryCommandState for justifycenter on text centered by webkit', None, category='query'),
  RichtextTest('q-justifyfull-0', 'queryCommandState for justifyfull on plain text', None, category='query'),
  RichtextTest('q-justifyfull-1', 'queryCommandState for justifyfull on text justified by Firefox', None, category='query'),
  RichtextTest('q-justifyfull-2', 'queryCommandState for justifyfull on text justified by IE', None, category='query'),
  RichtextTest('q-justifyfull-3', 'queryCommandState for justifyfull on text justified by webkit', None, category='query'),
  RichtextTest('q-justifyleft-0', 'queryCommandState for justifyleft on plain text', None, category='query'),
  RichtextTest('q-justifyleft-1', 'queryCommandState for justifyleft on text left-aligned by Firefox', None, category='query'),
  RichtextTest('q-justifyleft-2', 'queryCommandState for justifyleft on text left-aligned by IE', None, category='query'),
  RichtextTest('q-justifyleft-3', 'queryCommandState for justifyleft on text left-aligned by webkit', None, category='query'),
  RichtextTest('q-justifyright-0', 'queryCommandState for justifyright on plain text', None, category='query'),
  RichtextTest('q-justifyright-1', 'queryCommandState for justifyright on text right-aligned by Firefox', None, category='query'),
  RichtextTest('q-justifyright-2', 'queryCommandState for justifyright on text right-aligned by IE', None, category='query'),
  RichtextTest('q-justifyright-3', 'queryCommandState for justifyright on text right-aligned by webkit', None, category='query'),
  RichtextTest('q-strikethrough-0', 'queryCommandState for strikethrough on plain text', None, category='query'),
  RichtextTest('q-strikethrough-1', 'queryCommandState for strikethrough on text surrounded by <strike> tag', None, category='query'),
  RichtextTest('q-strikethrough-2', 'queryCommandState for strikethrough on text surrounded by <strike> tag with text-decoration:none style', None, category='query'),
  RichtextTest('q-strikethrough-3', 'queryCommandState for strikethrough on text surrounded by <s> tag', None, category='query'),
  RichtextTest('q-strikethrough-4', 'queryCommandState for strikethrough on text surrounded by <del> tag', None, category='query'),
  RichtextTest('q-strikethrough-5', 'queryCommandState for strikethrough on text surrounded by b tag with text-decoration:line-through style', None, category='query'),
  RichtextTest('q-subscript-0', 'queryCommandState for subscript on plain text', None, category='query'),
  RichtextTest('q-subscript-1', 'queryCommandState for subscript on text surrounded by <sub> tag', None, category='query'),
  RichtextTest('q-superscript-0', 'queryCommandState for superscript on plain text', None, category='query'),
  RichtextTest('q-superscript-1', 'queryCommandState for superscript on text surrounded by <sup> tag', None, category='query'),
  RichtextTest('q-underline-0', 'queryCommandState for underline on plain text', None, category='query'),
  RichtextTest('q-underline-1', 'queryCommandState for underline on text surrounded by <u> tag', None, category='query'),
  RichtextTest('q-underline-2', 'queryCommandState for underline on text surrounded by <a> tag', None, category='query'),
  RichtextTest('q-underline-3', 'queryCommandState for underline on text surrounded by text-deocoration:undeline style', None, category='query'),
  RichtextTest('q-underline-4', 'queryCommandState for underline on text surrounded by <u> tag with text-decoration:none style', None, category='query'),
  RichtextTest('q-underline-5', 'queryCommandState for underline on text surrounded by <a> tag with text-decoration:none style', None, category='query'),
  RichtextTest('c-backcolor-0', 'backcolor execCommand on text surrounded by <font> tag with background-color style', None, category='change'),
  RichtextTest('c-backcolor-1', 'backcolor execCommand on text with background-color style generated by webkit', None, category='change'),
  RichtextTest('c-backcolor-2', 'backcolor execCommand on text with background-color style', None, category='change'),
  RichtextTest('c-fontname-0', 'fontname execCommand on text surrounded by <font> tag with face attribute', None, category='change'),
  RichtextTest('c-fontname-1', 'fontname execCommand on text with font-family style', None, category='change'),
  RichtextTest('c-fontname-2', 'fontname execCommand on text surrounded by <font> tag with face attribute AND font-family style', None, category='change'),
  RichtextTest('c-fontname-3', 'fontname execCommand on text surrounded by nested <font> tags with face attributes', None, category='change'),
  RichtextTest('c-fontname-4', 'fontname execCommand on text surrounded by <font> tag with face attribute inside font-family style', None, category='change'),
  RichtextTest('c-fontsize-0', 'fontsize execCommand on text surrounded by <font> tag with size attribute', None, category='change'),
  RichtextTest('c-fontsize-1', 'fontsize execCommand on text with font-size style', None, category='change'),
  RichtextTest('c-fontsize-2', 'fontsize execCommand on text surrounded by <font> tag with size attribute AND font-size style', None, category='change'),
  RichtextTest('c-forecolor-0', 'forecolor execCommand on text surrounded by <font> tag with color attribute', None, category='change'),
  RichtextTest('c-forecolor-1', 'forecolor execCommand on text with color style', None, category='change'),
  RichtextTest('c-forecolor-2', 'forecolor execCommand on text surrounded by <font> tag with color attribute AND color style', None, category='change'),
  RichtextTest('c-hilitecolor-0', 'hilitecolor execCommand on text surrounded by <font> tag with background-color style', None, category='change'),
  RichtextTest('c-hilitecolor-1', 'hilitecolor execCommand on text with background-color style generated by webkit', None, category='change'),
  RichtextTest('c-hilitecolor-2', 'hilitecolor execCommand on text with background-color style', None, category='change'),
)



class RichTextTestSet(test_set_base.TestSet):

  def GetRowScoreAndDisplayValue(self, results):
    """Get the overall score for this row of results data.
    Args:
      results: A dictionary that looks like:
      {
        'testkey1': {'score': 1-100, 'median': median, 'display': 'celltext'},
        'testkey2': {'score': 1-100, 'median': median, 'display': 'celltext'},
        etc...
      }

    Returns:
      A tuple of (score, display)
      Where score is a value between 1-100.
      And display is the text for the cell.
    """
    #logging.info('%s GetRowScore, results:%s' % (self.category, results))
    return (90, 'x/x')


TEST_SET = RichTextTestSet(
    category=_CATEGORY,
    category_name='Rich Text',
    tests=_TESTS,
)
