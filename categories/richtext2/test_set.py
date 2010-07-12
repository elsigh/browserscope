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

"""Rich Text Test Definitions."""

__author__ = 'rolandsteiner@google.com (Roland Steiner)'

import logging

from categories import test_set_base


_CATEGORY = 'richtext2'

class RichText2Test(test_set_base.TestBase):
  TESTS_URL_PATH = '/%s/test' % _CATEGORY
  # Categories: None, 'apply', 'applyCSS', 'change', 'changeCSS', 'delete',
  # 'forwarddelete', 'insert', 'selection', unapply', 'unapplyCSS'
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

class InsertRichText2Test(IndividualRichText2Test):
  CATEGORY = 'insert'

class DeleteRichText2Test(IndividualRichText2Test):
  CATEGORY = 'delete'

class ForwardDeleteRichText2Test(IndividualRichText2Test):
  CATEGORY = 'forwarddelete'

CATEGORIES = sorted(['selection', 'apply', 'applyCSS', 'change', 'changeCSS', 'unapply', 'unapplyCSS', 'delete', 'forwarddelete', 'insert'])

_TESTS = (
  # key, name, doc
  CategoryRichText2Test('selection', 'Test Selection',
  '''These tests verify that selection commands are honored correctly.
  The expected and actual outputs are shown.'''),

  CategoryRichText2Test('apply', 'Apply Formatting',
  '''These tests use execCommand to apply formatting to plain text,
  with styleWithCSS being set to false.
  The expected and actual outputs are shown.'''),

  CategoryRichText2Test('applyCSS', 'Apply Formatting, Using CSS',
  '''These tests use execCommand to apply formatting to plain text,
  with styleWithCSS being set to true.
  The expected and actual outputs are shown.'''),

  CategoryRichText2Test('change', 'Change Existing Formatting',
  '''These tests are similar to the unapply tests, except that they're for
  execCommands which take an argument (fontname, fontsize, etc.). They apply
  the execCommand to text which already has some formatting, in order to change
  it. styleWithCSS is being set to false.
  The expected and actual outputs are shown.'''),

  CategoryRichText2Test('changeCSS', 'Change Existing Formatting, Using CSS',
  '''These tests are similar to the unapply tests, except that they're for
  execCommands which take an argument (fontname, fontsize, etc.). They apply
  the execCommand to text which already has some formatting, in order to change
  it. styleWithCSS is being set to true.
  The expected and actual outputs are shown.'''),

  CategoryRichText2Test('unapply', 'Unapply Formatting',
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

  CategoryRichText2Test('unapplyCSS', 'Unapply Formatting, Using CSS',
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

  # Individual tests
  # key, name
  #
  # VS RegEx to convert from JS files:
  #    Find:     '{[^']+}'\: \{\n:b+desc\::b+{'[^']+'},
  #    Replace: <xyz>RichText2Test('<Short>-\1', \2),
  
  SelectionRichText2Test('S-SELALL-TEXT-1', 'select all, text only'),
  SelectionRichText2Test('S-SELALL-I-1', 'select all, with outer tags'),
  SelectionRichText2Test('S-UNSEL-TEXT-1', 'unselect'),

  ApplyRichText2Test('A-B-TEXT-1', 'Bold selection'),
  ApplyRichText2Test('A-B-TEXT-1-SR', 'Bold reversed selection'),
  ApplyRichText2Test('A-B-MIXED-1', 'Bold selection, partially including italic'),
  ApplyRichText2Test('A-I-TEXT-1', 'Italicize selection'),
  ApplyRichText2Test('A-U-TEXT-1', 'Underline selection'),
  ApplyRichText2Test('A-S-TEXT-1', 'Strike-through selection'),
  ApplyRichText2Test('A-SUB-TEXT-1', 'Change selection to subscript'),
  ApplyRichText2Test('A-SUP-TEXT-1', 'Change selection to superscript'),
  ApplyRichText2Test('A-BC-TEXT-1', 'Change background color (no non-CSS variant available)'),
  ApplyRichText2Test('A-FC-TEXT-1', 'Change the text color'),
  ApplyRichText2Test('A-FN-TEXT-1', 'Change the font name'),
  ApplyRichText2Test('A-FS-TEXT-2', 'Change the font size to "2"'),
  ApplyRichText2Test('A-FS-TEXT-18px', 'Change the font size to "18px"'),
  ApplyRichText2Test('A-FS-TEXT-large', 'Change the font size to "large"'),
  ApplyRichText2Test('A-IND-TEXT-1', 'Indent the text'),
  ApplyRichText2Test('A-OUTD-TEXT-1', 'Outdent the text'),
  ApplyRichText2Test('A-JC-TEXT-1', 'justify the text centrally'),
  ApplyRichText2Test('A-JF-TEXT-1', 'justify the text fully'),
  ApplyRichText2Test('A-JL-TEXT-1', 'justify the text left'),
  ApplyRichText2Test('A-JR-TEXT-1', 'justify the text right'),
  ApplyRichText2Test('A-CL-1', 'create a link around the selection'),

  ApplyCSSRichText2Test('AC-B-TEXT-1', 'Bold selection'),
  ApplyCSSRichText2Test('AC-I-TEXT-1', 'Italicize selection'),
  ApplyCSSRichText2Test('AC-U-TEXT-1', 'Underline selection'),
  ApplyCSSRichText2Test('AC-S-TEXT-1', 'Strike-through selection'),
  ApplyCSSRichText2Test('AC-BC-TEXT-1', 'Change background color'),
  ApplyCSSRichText2Test('AC-FC-TEXT-1', 'Change the text color'),
  ApplyCSSRichText2Test('AC-FN-TEXT-1', 'Change the font name'),
  ApplyCSSRichText2Test('AC-FS-TEXT-2', 'Change the font size to "2"'),
  ApplyCSSRichText2Test('AC-FS-TEXT-18px', 'Change the font size to "18px"'),
  ApplyCSSRichText2Test('AC-FS-TEXT-large', 'Change the font size to "large"'),
  ApplyCSSRichText2Test('AC-JC-TEXT-1', 'justify the text centrally'),
  ApplyCSSRichText2Test('AC-JF-TEXT-1', 'justify the text fully'),
  ApplyCSSRichText2Test('AC-JL-TEXT-1', 'justify the text left'),
  ApplyCSSRichText2Test('AC-JR-TEXT-1', 'justify the text right'),

  ChangeRichText2Test('C-FN-TEXT-1', 'Change existing font name to new font name, not using CSS styling'),
  ChangeRichText2Test('C-FS-TEXT-1', 'Change existing font size to new size, not using CSS styling'),

  ChangeCSSRichText2Test('CC-FN-TEXT-1', 'Change existing font name to new font name, using CSS styling'),
  ChangeCSSRichText2Test('CC-FS-TEXT-1', 'Change existing font size to new size, using CSS styling'),

  UnapplyRichText2Test('U-UNLINK-1', 'unlink wrapped <a> element'),
  UnapplyRichText2Test('U-UNLINK-2', 'unlink <a> element where the selection wraps the full content'),
  UnapplyRichText2Test('U-UNLINK-5', 'unlink wrapped <a> element that has a name and href attribute'),
  UnapplyRichText2Test('U-UNLINK-6', 'unlink contained <a> element'),
  UnapplyRichText2Test('U-UNLINK-7', 'unlink 2 contained <a> elements'),
  UnapplyRichText2Test('U-B-B-SI-1', 'Selection within tags; remove <b> tags'),
  UnapplyRichText2Test('U-B-B-SO-1', 'Selection outside of tags; remove <b> tags'),
  UnapplyRichText2Test('U-B-B-SM-1', 'Selection mixed; remove <b> tags'),
  UnapplyRichText2Test('U-B-B-SM-2', 'Selection mixed; remove <b> tags'),
  UnapplyRichText2Test('U-B-STRONG-SI-1', 'Selection within tags; remove <strong> tags'),
  UnapplyRichText2Test('U-B-STRONG-SO-1', 'Selection outside of tags; remove <strong> tags'),
  UnapplyRichText2Test('U-B-STRONG-SM-1', 'Selection mixed; remove <strong> tags'),
  UnapplyRichText2Test('U-B-STRONG-SM-2', 'Selection mixed; remove <strong> tags'),
  UnapplyRichText2Test('U-B-STYLE-FW-SI-1', 'Selection within tags; remove "font-weight: bold"'),
  UnapplyRichText2Test('U-B-STYLE-FW-SO-1', 'Selection outside of tags; remove "font-weight: bold"'),
  UnapplyRichText2Test('U-B-STYLE-FW-SM-1', 'Selection mixed; remove "font-weight: bold"'),
  UnapplyRichText2Test('U-B-STYLE-FW-SM-2', 'Selection mixed; remove "font-weight: bold"'),
  UnapplyRichText2Test('U-I-I-SI-1', 'Selection within tags; remove <i> tags'),
  UnapplyRichText2Test('U-I-I-SO-1', 'Selection outside of tags; remove <i> tags'),
  UnapplyRichText2Test('U-I-I-SM-1', 'Selection mixed; remove <i> tags'),
  UnapplyRichText2Test('U-I-I-SM-2', 'Selection mixed; remove <i> tags'),
  UnapplyRichText2Test('U-I-EM-SI-1', 'Selection within tags; remove <em> tags'),
  UnapplyRichText2Test('U-I-EM-SO-1', 'Selection outside of tags; remove <em> tags'),
  UnapplyRichText2Test('U-I-EM-SM-1', 'Selection mixed; remove <em> tags'),
  UnapplyRichText2Test('U-I-EM-SM-2', 'Selection mixed; remove <em> tags'),
  UnapplyRichText2Test('U-I-STYLE-FS-SI-1', 'Selection within tags; remove "font-style: italic"'),
  UnapplyRichText2Test('U-I-STYLE-FS-SO-1', 'Selection outside of tags; Italicize "font-style: italic"'),
  UnapplyRichText2Test('U-I-STYLE-FS-SM-1', 'Selection mixed; Italicize "font-style: italic"'),
  UnapplyRichText2Test('U-I-STYLE-FS-SM-2', 'Selection mixed; Italicize "font-style: italic"'),
  UnapplyRichText2Test('U-U-U-SI-1', 'Selection within tags; remove <u> tags'),
  UnapplyRichText2Test('U-U-U-SO-1', 'Selection outside of tags; remove <u> tags'),
  UnapplyRichText2Test('U-U-U-SM-1', 'Selection mixed; remove <u> tags'),
  UnapplyRichText2Test('U-U-U-SM-2', 'Selection mixed; remove <u> tags'),
  UnapplyRichText2Test('U-U-STYLE-TD-SI-1', 'Selection within tags; remove "text-decoration: underline"'),
  UnapplyRichText2Test('U-U-STYLE-TD-SO-1', 'Selection outside of tags; remove "text-decoration: underline"'),
  UnapplyRichText2Test('U-U-STYLE-TD-SM-1', 'Selection mixed; remove "text-decoration: underline"'),
  UnapplyRichText2Test('U-U-STYLE-TD-SM-2', 'Selection mixed; remove "text-decoration: underline"'),
  UnapplyRichText2Test('U-S-S-SI-1', 'Selection within tags; remove <s> tags'),
  UnapplyRichText2Test('U-S-S-SO-1', 'Selection outside of tags; remove <s> tags'),
  UnapplyRichText2Test('U-S-S-SM-1', 'Selection mixed; remove <s> tags'),
  UnapplyRichText2Test('U-S-S-SM-2', 'Selection mixed; remove <s> tags'),
  UnapplyRichText2Test('U-S-STRIKE-SI-1', 'Selection within tags; remove <strike> tags'),
  UnapplyRichText2Test('U-S-STRIKE-SO-1', 'Selection outside of tags; remove <strike> tags'),
  UnapplyRichText2Test('U-S-STRIKE-SM-1', 'Selection mixed; remove <strike> tags'),
  UnapplyRichText2Test('U-S-STRIKE-SM-2', 'Selection mixed; remove <strike> tags'),
  UnapplyRichText2Test('U-S-STYLE-TD-LT-1', 'Selection within tags; remove "text-decoration:line-through"'),
  UnapplyRichText2Test('U-S-STYLE-TD-LT-1', 'Selection outside of tags; Italicize "text-decoration:line-through"'),
  UnapplyRichText2Test('U-S-STYLE-TD-LT-1', 'Selection mixed; Italicize "text-decoration:line-through"'),
  UnapplyRichText2Test('U-S-STYLE-TD-LT-2', 'Selection mixed; Italicize "text-decoration:line-through"'),
  UnapplyRichText2Test('U-UNLINK-3', 'unlink an <a> element that contains the collapsed selection'),
  UnapplyRichText2Test('U-UNLINK-4', 'unlink an <a> element that contains the whole selection'),
  UnapplyRichText2Test('U-UNLINK-SM-1', 'unlink a partially contained <a> element'),
  UnapplyRichText2Test('U-UNLINK-SM-2', 'unlink a partially contained <a> element'),

  UnapplyCSSRichText2Test('UC-B-B-SI-1', 'Selection within tags; remove <b> tags'),
  UnapplyCSSRichText2Test('UC-B-B-SO-1', 'Selection outside of tags; remove <b> tags'),
  UnapplyCSSRichText2Test('UC-B-B-SM-1', 'Selection mixed; remove <b> tags'),
  UnapplyCSSRichText2Test('UC-B-B-SM-2', 'Selection mixed; remove <b> tags'),
  UnapplyCSSRichText2Test('UC-B-STRONG-SI-1', 'Selection within tags; remove <strong> tags'),
  UnapplyCSSRichText2Test('UC-B-STRONG-SO-1', 'Selection outside of tags; remove <strong> tags'),
  UnapplyCSSRichText2Test('UC-B-STRONG-SM-1', 'Selection mixed; remove <strong> tags'),
  UnapplyCSSRichText2Test('UC-B-STRONG-SM-2', 'Selection mixed; remove <strong> tags'),
  UnapplyCSSRichText2Test('UC-B-STYLE-FW-SI-1', 'Selection within tags; remove "font-weight: bold"'),
  UnapplyCSSRichText2Test('UC-B-STYLE-FW-SO-1', 'Selection outside of tags; remove "font-weight: bold"'),
  UnapplyCSSRichText2Test('UC-B-STYLE-FW-SM-1', 'Selection mixed; remove "font-weight: bold"'),
  UnapplyCSSRichText2Test('UC-B-STYLE-FW-SM-2', 'Selection mixed; remove "font-weight: bold"'),
  UnapplyCSSRichText2Test('UC-I-I-SI-1', 'Selection within tags; remove <i> tags'),
  UnapplyCSSRichText2Test('UC-I-I-SO-1', 'Selection outside of tags; remove <i> tags'),
  UnapplyCSSRichText2Test('UC-I-I-SM-1', 'Selection mixed; remove <i> tags'),
  UnapplyCSSRichText2Test('UC-I-I-SM-2', 'Selection mixed; remove <i> tags'),
  UnapplyCSSRichText2Test('UC-I-EM-SI-1', 'Selection within tags; remove <em> tags'),
  UnapplyCSSRichText2Test('UC-I-EM-SO-1', 'Selection outside of tags; remove <em> tags'),
  UnapplyCSSRichText2Test('UC-I-EM-SM-1', 'Selection mixed; remove <em> tags'),
  UnapplyCSSRichText2Test('UC-I-EM-SM-2', 'Selection mixed; remove <em> tags'),
  UnapplyCSSRichText2Test('UC-I-STYLE-FS-SI-1', 'Selection within tags; remove "font-style: italic"'),
  UnapplyCSSRichText2Test('UC-I-STYLE-FS-SO-1', 'Selection outside of tags; Italicize "font-style: italic"'),
  UnapplyCSSRichText2Test('UC-I-STYLE-FS-SM-1', 'Selection mixed; Italicize "font-style: italic"'),
  UnapplyCSSRichText2Test('UC-I-STYLE-FS-SM-2', 'Selection mixed; Italicize "font-style: italic"'),
  UnapplyCSSRichText2Test('UC-U-U-SI-1', 'Selection within tags; remove <u> tags'),
  UnapplyCSSRichText2Test('UC-U-U-SO-1', 'Selection outside of tags; remove <u> tags'),
  UnapplyCSSRichText2Test('UC-U-U-SM-1', 'Selection mixed; remove <u> tags'),
  UnapplyCSSRichText2Test('UC-U-U-SM-2', 'Selection mixed; remove <u> tags'),
  UnapplyCSSRichText2Test('UC-U-STYLE-TD-SI-1', 'Selection within tags; remove "text-decoration: underline"'),
  UnapplyCSSRichText2Test('UC-U-STYLE-TD-SO-1', 'Selection outside of tags; remove "text-decoration: underline"'),
  UnapplyCSSRichText2Test('UC-U-STYLE-TD-SM-1', 'Selection mixed; remove "text-decoration: underline"'),
  UnapplyCSSRichText2Test('UC-U-STYLE-TD-SM-2', 'Selection mixed; remove "text-decoration: underline"'),
  UnapplyCSSRichText2Test('UC-S-S-SI-1', 'Selection within tags; remove <s> tags'),
  UnapplyCSSRichText2Test('UC-S-S-SO-1', 'Selection outside of tags; remove <s> tags'),
  UnapplyCSSRichText2Test('UC-S-S-SM-1', 'Selection mixed; remove <s> tags'),
  UnapplyCSSRichText2Test('UC-S-S-SM-2', 'Selection mixed; remove <s> tags'),
  UnapplyCSSRichText2Test('UC-S-STRIKE-SI-1', 'Selection within tags; remove <strike> tags'),
  UnapplyCSSRichText2Test('UC-S-STRIKE-SO-1', 'Selection outside of tags; remove <strike> tags'),
  UnapplyCSSRichText2Test('UC-S-STRIKE-SM-1', 'Selection mixed; remove <strike> tags'),
  UnapplyCSSRichText2Test('UC-S-STRIKE-SM-2', 'Selection mixed; remove <strike> tags'),
  UnapplyCSSRichText2Test('UC-S-STYLE-TD-LT-1', 'Selection within tags; remove "text-decoration:line-through"'),
  UnapplyCSSRichText2Test('UC-S-STYLE-TD-LT-1', 'Selection outside of tags; Italicize "text-decoration:line-through"'),
  UnapplyCSSRichText2Test('UC-S-STYLE-TD-LT-1', 'Selection mixed; Italicize "text-decoration:line-through"'),
  UnapplyCSSRichText2Test('UC-S-STYLE-TD-LT-2', 'Selection mixed; Italicize "text-decoration:line-through"'),

  DeleteRichText2Test('D-D-CHAR-1', 'Delete 1 character'),
  DeleteRichText2Test('D-D-CHAR-2', 'Delete 1 pre-composed character o with diaeresis'),
  DeleteRichText2Test('D-D-CHAR-3', 'Delete 1 character with combining diaeresis above'),
  DeleteRichText2Test('D-D-CHAR-4', 'Delete 1 character with combining diaeresis below'),
  DeleteRichText2Test('D-D-CHAR-5', 'Delete 1 character with combining diaeresis above and below'),
  DeleteRichText2Test('D-D-CHAR-6', 'Delete 1 character with enclosing square'),
  DeleteRichText2Test('D-D-CHAR-7', 'Delete 1 character with combining long solidus overlay'),
  DeleteRichText2Test('D-D-CHAR-TBL-1', 'Delete from position immediately after table (should have no effect)'),
  DeleteRichText2Test('D-D-CHAR-TBL-2', 'Delete from start of first cell (should have no effect)'),
  DeleteRichText2Test('D-D-CHAR-TBL-3', 'Delete from start of inner cell (should have no effect)'),
  DeleteRichText2Test('D-D-TEXT-1', 'Delete text selection'),
  DeleteRichText2Test('D-D-SPAN-1', 'Delete at start of span'),
  DeleteRichText2Test('D-D-SPAN-2', 'Delete from position after span'),
  DeleteRichText2Test('D-D-SPAN-3', 'Delete oblique selection that starts before span'),
  DeleteRichText2Test('D-D-SPAN-4', 'Delete oblique selection that ends after span'),
  DeleteRichText2Test('D-D-SPAN-5', 'Delete selection that wraps the whole span content'),
  DeleteRichText2Test('D-D-SPAN-6', 'Delete selection that wraps the whole span'),
  DeleteRichText2Test('D-D-SPAN-7', 'Delete oblique selection that starts and ends in different spans'),
  DeleteRichText2Test('D-D-GEN-1', 'Delete at start of span with generated content'),
  DeleteRichText2Test('D-D-GEN-2', 'Delete from position after span with generated content'),
  DeleteRichText2Test('D-D-P-1', 'Delete at start of paragraph - should merge with previous'),
  DeleteRichText2Test('D-D-LI-1', 'Delete fully wrapped list item'),
  DeleteRichText2Test('D-D-LI-2', 'Delete oblique range between list items within same list'),
  DeleteRichText2Test('D-D-LI-3', 'Delete contents of last list item (list should remain)'),
  DeleteRichText2Test('D-D-LI-4', 'Delete last list item of list (should remove entire list)'),
  DeleteRichText2Test('D-D-CHILD-0', 'Delete selection that starts and ends within nodes that don\'t have children'),
  DeleteRichText2Test('D-D-TR-1', 'Delete first table row'),
  DeleteRichText2Test('D-D-TR-2', 'Delete middle table row'),
  DeleteRichText2Test('D-D-TR-3', 'Delete last table row'),
  DeleteRichText2Test('D-D-TR-ROWSPAN2-1', 'Delete first table row where a cell has rowspan 2'),
  DeleteRichText2Test('D-D-TR-ROWSPAN2-2', 'Delete second table row where a cell has rowspan 2'),
  DeleteRichText2Test('D-D-TR-ROWSPAN3-1', 'Delete first table row where a cell has rowspan 3'),
  DeleteRichText2Test('D-D-TR-ROWSPAN3-2', 'Delete middle table row where a cell has rowspan 3'),
  DeleteRichText2Test('D-D-TR-ROWSPAN3-3', 'Delete last table row where a cell has rowspan 3'),

  ForwardDeleteRichText2Test('FD-D-CHAR-1', 'Delete 1 character'),
  ForwardDeleteRichText2Test('FD-D-CHAR-2', 'Delete 1 pre-composed character o with diaeresis'),
  ForwardDeleteRichText2Test('FD-D-CHAR-3', 'Delete 1 character with combining diaeresis above'),
  ForwardDeleteRichText2Test('FD-D-CHAR-4', 'Delete 1 character with combining diaeresis below'),
  ForwardDeleteRichText2Test('FD-D-CHAR-5', 'Delete 1 character with combining diaeresis above and below'),
  ForwardDeleteRichText2Test('FD-D-CHAR-6', 'Delete 1 character with enclosing square'),
  ForwardDeleteRichText2Test('FD-D-CHAR-7', 'Delete 1 character with combining long solidus overlay'),
  ForwardDeleteRichText2Test('FD-D-CHAR-TBL-1', 'Delete from position immediately before table (should have no effect)'),
  ForwardDeleteRichText2Test('FD-D-CHAR-TBL-2', 'Delete from end of last cell (should have no effect)'),
  ForwardDeleteRichText2Test('FD-D-CHAR-TBL-3', 'Delete from end of inner cell (should have no effect)'),
  ForwardDeleteRichText2Test('FD-D-TEXT-1', 'Delete text selection'),
  ForwardDeleteRichText2Test('FD-D-SPAN-1', 'Delete at end of span'),
  ForwardDeleteRichText2Test('FD-D-SPAN-2', 'Delete from position before span'),
  ForwardDeleteRichText2Test('FD-D-SPAN-3', 'Delete oblique selection that starts before span'),
  ForwardDeleteRichText2Test('FD-D-SPAN-4', 'Delete oblique selection that ends after span'),
  ForwardDeleteRichText2Test('FD-D-SPAN-5', 'Delete selection that wraps the whole span content'),
  ForwardDeleteRichText2Test('FD-D-SPAN-6', 'Delete selection that wraps the whole span'),
  ForwardDeleteRichText2Test('FD-D-SPAN-7', 'Delete oblique selection that starts and ends in different spans'),
  ForwardDeleteRichText2Test('FD-D-GEN-1', 'Delete at end of span with generated content'),
  ForwardDeleteRichText2Test('FD-D-DEL-GEN-2', 'Delete from position before span with generated content'),
  ForwardDeleteRichText2Test('FD-D-P-1', 'Delete at end of paragraph - should merge with next'),
  ForwardDeleteRichText2Test('FD-D-LI-1', 'Delete fully wrapped list item'),
  ForwardDeleteRichText2Test('FD-D-LI-2', 'Delete oblique range between list items within same list'),
  ForwardDeleteRichText2Test('FD-D-LI-3', 'Delete contents of last list item (list should remain)'),
  ForwardDeleteRichText2Test('FD-D-LI-4', 'Delete last list item of list (should remove entire list)'),
  ForwardDeleteRichText2Test('FD-D-CHILD-0', 'Delete selection that starts and ends within nodes that don\'t have children'),

  InsertRichText2Test('I-HR-TEXT-1', 'Insert <hr> into text'),
  InsertRichText2Test('I-HR-TEXT-2', 'Insert <hr>, replacing selected text'),
  InsertRichText2Test('I-HR-ELEM-1', 'Insert <hr> between elements'),
  InsertRichText2Test('I-HR-ELEM-2', 'Insert <hr>, replacing a fully wrapped element'),
  InsertRichText2Test('I-HR-SPAN-1', 'Insert <hr> into a span, splitting it'),
  InsertRichText2Test('I-HR-SPAN-2', 'Insert <hr> into a span at the start (should not create an empty span)'),
  InsertRichText2Test('I-HR-SPAN-3', 'Insert <hr> into a span at the end'),
  InsertRichText2Test('I-HR-SPAN-4', 'Insert <hr> with oblique selection starting outside of span'),
  InsertRichText2Test('I-HR-SPAN-4-SR', 'Insert <hr> with oblique reversed selection ending outside of span'),
  InsertRichText2Test('I-HR-SPAN-5', 'Insert <hr> with oblique selection ending outside of span'),
  InsertRichText2Test('I-HR-SPAN-5-SR', 'Insert <hr> with oblique reversed selection starting outside of span'),
  InsertRichText2Test('I-HR-SPAN-6', 'Insert <hr> with oblique selection between different spans'),
  InsertRichText2Test('I-HR-SPAN-6-SR', 'Insert <hr> with reversed oblique selection between different spans'),
  InsertRichText2Test('I-HR-P-1', 'Insert <hr> into a paragraph, splitting it'),
  InsertRichText2Test('I-HR-P-2', 'Insert <hr> into a paragraph at the start (should not create an empty span)'),
  InsertRichText2Test('I-HR-P-3', 'Insert <hr> into a paragraph at the end (should not create an empty span)'),
  InsertRichText2Test('I-P-P-1', 'Split paragraph'),
  InsertRichText2Test('I-P-LI-2', 'Split list item'),
  InsertRichText2Test('I-TEXT-TEXT-1', 'Insert text'),
  InsertRichText2Test('I-TEXT-TEXT-2', 'Insert text, replacing selected text'),
  InsertRichText2Test('I-BR-TEXT-1', 'Insert <br> into text'),
  InsertRichText2Test('I-BR-TEXT-2', 'Insert <br>, replacing selected text'),
  InsertRichText2Test('I-BR-LI-1', 'Insert <br> within list item'),
  InsertRichText2Test('I-IMG-TEXT-1', 'Insert image with URL "http://foo.com/bar.png"'),
  InsertRichText2Test('I-IMG-TEXT-2a', 'Change existing image to new URL, selection on <img>'),
  InsertRichText2Test('I-IMG-TEXT-2b', 'Change existing image to new URL, selection in text surrounding <img>'),
  InsertRichText2Test('I-IMG-TEXT-3a', 'Remove existing image or URL, selection on <img>'),
  InsertRichText2Test('I-IMG-TEXT-3b', 'Remove existing image or URL, selection in text surrounding <img>'),
  InsertRichText2Test('I-OL-SC-1', 'Insert ordered list on collapsed selection'),
  InsertRichText2Test('I-OL-TEXT-1', 'Insert ordered list on selected text'),
  InsertRichText2Test('I-UL-SC-1', 'Insert unordered list on collapsed selection'),
  InsertRichText2Test('I-UL-TEXT-1', 'Insert unordered list on selected text')
)

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
    category=_CATEGORY,
    category_name='Rich Text 2',
    summary_doc='New suite of tests to see how well editor controls work with a variety of HTML.',
    tests=_TESTS,
)
