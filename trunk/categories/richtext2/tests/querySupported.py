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

"""queryCommandSupported tests"""

__author__ = 'rolandsteiner@google.com (Roland Steiner)'

QUERYSUPPORTED_TESTS = {
  'id':            'Q',
  'caption':       'queryCommandSupported Tests',
  'pad':           'foo[bar]baz',
  'checkAttrs':    False,
  'checkStyle':    False,
  'checkSel':      False,
  'styleWithCSS':  False,
  'expected':      True,

  'Proposed': [
    ### queryCommandSupported
    { 'id':          'STYLEWITHCSS_TEXT',
      'desc':        'check whether the "styleWithCSS" command is supported',
      'qcsupported': 'styleWithCSS' },

    { 'id':          'BOLD_TEXT',
      'desc':        'check whether the "bold" command is supported',
      'qcsupported': 'bold' },

    { 'id':          'BOLD_B',
      'desc':        'check whether the "bold" command is supported',
      'qcsupported': 'bold',
      'pad':         '<b>foo[bar]baz</b>' },

    { 'id':          'ITALIC_TEXT',
      'desc':        'check whether the "italic" command is supported',
      'qcsupported': 'italic' },

    { 'id':          'ITALIC_I',
      'desc':        'check whether the "italic" command is supported',
      'qcsupported': 'italic',
      'pad':         '<i>foo[bar]baz</i>' },

    { 'id':          'UNDERLINE_TEXT',
      'desc':        'check whether the "underline" command is supported',
      'qcsupported': 'underline' },

    { 'id':          'STRIKETHROUGH_TEXT',
      'desc':        'check whether the "strikethrough" command is supported',
      'qcsupported': 'strikethrough' },

    { 'id':          'SUBSCRIPT_TEXT',
      'desc':        'check whether the "subscript" command is supported',
      'qcsupported': 'subscript' },

    { 'id':          'SUPERSCRIPT_TEXT',
      'desc':        'check whether the "superscript" command is supported',
      'qcsupported': 'superscript' },

    { 'id':          'BACKCOLOR_TEXT',
      'desc':        'check whether the "backcolor" command is supported',
      'qcsupported': 'backcolor' },

    { 'id':          'FORECOLOR_TEXT',
      'desc':        'check whether the "forecolor" command is supported',
      'qcsupported': 'forecolor' },

    { 'id':          'HILITECOLOR_TEXT',
      'desc':        'check whether the "hilitecolor" command is supported',
      'qcsupported': 'hilitecolor' },

    { 'id':          'FONTNAME_TEXT',
      'desc':        'check whether the "fontname" command is supported',
      'qcsupported': 'fontname' },

    { 'id':          'FONTSIZE_TEXT',
      'desc':        'check whether the "fontsize" command is supported',
      'qcsupported': 'fontsize' },

    { 'id':          'INCREASEFONTSIZE_TEXT',
      'desc':        'check whether the "increasefontsize" command is supported',
      'qcsupported': 'increasefontsize' },

    { 'id':          'DECREASEFONTSIZE_TEXT',
      'desc':        'check whether the "decreasefontsize" command is supported',
      'qcsupported': 'decreasefontsize' },

    { 'id':          'HEADING_TEXT',
      'desc':        'check whether the "heading" command is supported',
      'qcsupported': 'heading' },

    { 'id':          'FORMATBLOCK_TEXT',
      'desc':        'check whether the "formatblock" command is supported',
      'qcsupported': 'formatblock' },

    { 'id':          'INDENT_TEXT',
      'desc':        'check whether the "indent" command is supported',
      'qcsupported': 'indent' },

    { 'id':          'OUTDENT_TEXT',
      'desc':        'check whether the "outdent" command is supported',
      'qcsupported': 'outdent' },

    { 'id':          'CREATELINK_TEXT',
      'desc':        'check whether the "createlink" command is supported',
      'qcsupported': 'createlink' },

    { 'id':          'UNLINK_TEXT',
      'desc':        'check whether the "unlink" command is supported',
      'qcsupported': 'unlink' },

    { 'id':          'CREATEBOOKMARK_TEXT',
      'desc':        'check whether the "createbookmark" command is supported',
      'qcsupported': 'createbookmark' },

    { 'id':          'UNBOOKMARK_TEXT',
      'desc':        'check whether the "unbookmark" command is supported',
      'qcsupported': 'unbookmark' },

    { 'id':          'JUSTIFYCENTER_TEXT',
      'desc':        'check whether the "justifycenter" command is supported',
      'qcsupported': 'justifycenter' },

    { 'id':          'JUSTIFYFULL_TEXT',
      'desc':        'check whether the "justifyfull" command is supported',
      'qcsupported': 'justifyfull' },

    { 'id':          'JUSTIFYLEFT_TEXT',
      'desc':        'check whether the "justifyleft" command is supported',
      'qcsupported': 'justifyleft' },

    { 'id':          'JUSTIFYRIGHT_TEXT',
      'desc':        'check whether the "justifyright" command is supported',
      'qcsupported': 'justifyright' },

    { 'id':          'DELETE_TEXT',
      'desc':        'check whether the "delete" command is supported',
      'qcsupported': 'delete' },

    { 'id':          'FORWARDDELETE_TEXT',
      'desc':        'check whether the "forwarddelete" command is supported',
      'qcsupported': 'forwarddelete' },

    { 'id':          'INSERTHTML_TEXT',
      'desc':        'check whether the "inserthtml" command is supported',
      'qcsupported': 'inserthtml' },

    { 'id':          'INSERTHORIZONTALRULE_TEXT',
      'desc':        'check whether the "inserthorizontalrule" command is supported',
      'qcsupported': 'inserthorizontalrule' },

    { 'id':          'INSERTIMAGE_TEXT',
      'desc':        'check whether the "insertimage" command is supported',
      'qcsupported': 'insertimage' },

    { 'id':          'INSERTLINEBREAK_TEXT',
      'desc':        'check whether the "insertlinebreak" command is supported',
      'qcsupported': 'insertlinebreak' },

    { 'id':          'INSERTPARAGRAPH_TEXT',
      'desc':        'check whether the "insertparagraph" command is supported',
      'qcsupported': 'insertparagraph' },

    { 'id':          'INSERTORDEREDLIST_TEXT',
      'desc':        'check whether the "insertorderedlist" command is supported',
      'qcsupported': 'insertorderedlist' },

    { 'id':          'INSERTUNORDEREDLIST_TEXT',
      'desc':        'check whether the "insertunorderedlist" command is supported',
      'qcsupported': 'insertunorderedlist' },

    { 'id':          'INSERTTEXT_TEXT',
      'desc':        'check whether the "inserttext" command is supported',
      'qcsupported': 'inserttext' },

    { 'id':          'REMOVEFORMAT_TEXT',
      'desc':        'check whether the "removeformat" command is supported',
      'qcsupported': 'removeformat' },

    { 'id':          'UNDO_TEXT',
      'desc':        'check whether the "undo" command is supported',
      'qcsupported': 'undo' },

    { 'id':          'REDO_TEXT',
      'desc':        'check whether the "redo" command is supported',
      'qcsupported': 'redo' },

    { 'id':          'SELECTALL_TEXT',
      'desc':        'check whether the "selectall" command is supported',
      'qcsupported': 'selectall' },

    { 'id':          'UNSELECT_TEXT',
      'desc':        'check whether the "unselect" command is supported',
      'qcsupported': 'unselect' }
  ]
}


