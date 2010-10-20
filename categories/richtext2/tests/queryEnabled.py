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

"""queryCommandEnabled tests"""

__author__ = 'rolandsteiner@google.com (Roland Steiner)'

# Selection specifications used in 'id':
#
# Caret/collapsed selections:
#
# SC: 'caret'    caret/collapsed selection
# SB: 'before'   caret/collapsed selection before element
# SA: 'after'    caret/collapsed selection after element
# SS: 'start'    caret/collapsed selection at the start of the element (before first child/at text pos. 0)
# SE: 'end'      caret/collapsed selection at the end of the element (after last child/at text pos. n)
# SX: 'betwixt'  collapsed selection between elements
#
# Range selections:
#
# SO: 'outside'  selection wraps element in question
# SI: 'inside'   selection is inside of element in question
# SW: 'wrap'     as SI, but also wraps all children of element
# SL: 'left'     oblique selection - starts outside element and ends inside
# SR: 'right'    oblique selection - starts inside element and ends outside
# SM: 'mixed'    selection starts and ends in different elements
#
# SxR: selection is reversed
#
# Sxn or SxRn    selection applies to element #n of several identical

QUERYENABLED_TESTS = {
  'id':           'QE',
  'caption':      'queryCommandEnabled Tests',
  'pad':          'foo[bar]baz',
  'checkAttrs':   False,
  'checkStyle':   False,
  'styleWithCSS': False,
  'expected':     True,

  'Proposed': [
    { 'id':         'STYLEWITHCSS_TEXT-1',
      'desc':       'check whether the "styleWithCSS" command is enabled',
      'qcenabled':  'styleWithCSS' },

    { 'id':         'CONTENTREADONLY_TEXT-1',
      'desc':       'check whether the "contentreadonly" command is enabled',
      'qcenabled':  'contentreadonly' },

    { 'id':         'BOLD_TEXT-1',
      'desc':       'check whether the "bold" command is enabled',
      'qcenabled':  'bold' },

    { 'id':         'ITALIC_TEXT-1',
      'desc':       'check whether the "italic" command is enabled',
      'qcenabled':  'italic' },

    { 'id':         'UNDERLINE_TEXT-1',
      'desc':       'check whether the "underline" command is enabled',
      'qcenabled':  'underline' },

    { 'id':         'STRIKETHROUGH_TEXT-1',
      'desc':       'check whether the "strikethrough" command is enabled',
      'qcenabled':  'strikethrough' },

    { 'id':         'SUBSCRIPT_TEXT-1',
      'desc':       'check whether the "subscript" command is enabled',
      'qcenabled':  'subscript' },

    { 'id':         'SUPERSCRIPT_TEXT-1',
      'desc':       'check whether the "superscript" command is enabled',
      'qcenabled':  'superscript' },

    { 'id':         'BACKCOLOR_TEXT-1',
      'desc':       'check whether the "backcolor" command is enabled',
      'qcenabled':  'backcolor' },

    { 'id':         'FORECOLOR_TEXT-1',
      'desc':       'check whether the "forecolor" command is enabled',
      'qcenabled':  'forecolor' },

    { 'id':         'HILITECOLOR_TEXT-1',
      'desc':       'check whether the "hilitecolor" command is enabled',
      'qcenabled':  'hilitecolor' },

    { 'id':         'FONTNAME_TEXT-1',
      'desc':       'check whether the "fontname" command is enabled',
      'qcenabled':  'fontname' },

    { 'id':         'FONTSIZE_TEXT-1',
      'desc':       'check whether the "fontsize" command is enabled',
      'qcenabled':  'fontsize' },

    { 'id':         'INCREASEFONTSIZE_TEXT-1',
      'desc':       'check whether the "increasefontsize" command is enabled',
      'qcenabled':  'increasefontsize' },

    { 'id':         'DECREASEFONTSIZE_TEXT-1',
      'desc':       'check whether the "decreasefontsize" command is enabled',
      'qcenabled':  'decreasefontsize' },

    { 'id':         'HEADING_TEXT-1',
      'desc':       'check whether the "heading" command is enabled',
      'qcenabled':  'heading' },

    { 'id':         'FORMATBLOCK_TEXT-1',
      'desc':       'check whether the "formatblock" command is enabled',
      'qcenabled':  'formatblock' },

    { 'id':         'INDENT_TEXT-1',
      'desc':       'check whether the "indent" command is enabled',
      'qcenabled':  'indent' },

    { 'id':         'OUTDENT_TEXT-1',
      'desc':       'check whether the "outdent" command is enabled',
      'qcenabled':  'outdent' },

    { 'id':         'CREATELINK_TEXT-1',
      'desc':       'check whether the "createlink" command is enabled',
      'qcenabled':  'createlink' },

    { 'id':         'UNLINK_TEXT-1',
      'desc':       'check whether the "unlink" command is enabled',
      'qcenabled':  'unlink' },

    { 'id':         'CREATEBOOKMARK_TEXT-1',
      'desc':       'check whether the "createbookmark" command is enabled',
      'qcenabled':  'createbookmark' },

    { 'id':         'UNBOOKMARK_TEXT-1',
      'desc':       'check whether the "unbookmark" command is enabled',
      'qcenabled':  'unbookmark' },

    { 'id':         'JUSTIFYCENTER_TEXT-1',
      'desc':       'check whether the "justifycenter" command is enabled',
      'qcenabled':  'justifycenter' },

    { 'id':         'JUSTIFYFULL_TEXT-1',
      'desc':       'check whether the "justifyfull" command is enabled',
      'qcenabled':  'justifyfull' },

    { 'id':         'JUSTIFYLEFT_TEXT-1',
      'desc':       'check whether the "justifyleft" command is enabled',
      'qcenabled':  'justifyleft' },

    { 'id':         'JUSTIFYRIGHT_TEXT-1',
      'desc':       'check whether the "justifyright" command is enabled',
      'qcenabled':  'justifyright' },

    { 'id':         'DELETE_TEXT-1',
      'desc':       'check whether the "delete" command is enabled',
      'qcenabled':  'delete' },

    { 'id':         'FORWARDDELETE_TEXT-1',
      'desc':       'check whether the "forwarddelete" command is enabled',
      'qcenabled':  'forwarddelete' },

    { 'id':         'INSERTHTML_TEXT-1',
      'desc':       'check whether the "inserthtml" command is enabled',
      'qcenabled':  'inserthtml' },

    { 'id':         'INSERTHORIZONTALRULE_TEXT-1',
      'desc':       'check whether the "inserthorizontalrule" command is enabled',
      'qcenabled':  'inserthorizontalrule' },

    { 'id':         'INSERTIMAGE_TEXT-1',
      'desc':       'check whether the "insertimage" command is enabled',
      'qcenabled':  'insertimage' },

    { 'id':         'INSERTLINEBREAK_TEXT-1',
      'desc':       'check whether the "insertlinebreak" command is enabled',
      'qcenabled':  'insertlinebreak' },

    { 'id':         'INSERTPARAGRAPH_TEXT-1',
      'desc':       'check whether the "insertparagraph" command is enabled',
      'qcenabled':  'insertparagraph' },

    { 'id':         'INSERTORDEREDLIST_TEXT-1',
      'desc':       'check whether the "insertorderedlist" command is enabled',
      'qcenabled':  'insertorderedlist' },

    { 'id':         'INSERTUNORDEREDLIST_TEXT-1',
      'desc':       'check whether the "insertunorderedlist" command is enabled',
      'qcenabled':  'insertunorderedlist' },

    { 'id':         'INSERTTEXT_TEXT-1',
      'desc':       'check whether the "inserttext" command is enabled',
      'qcenabled':  'inserttext' },

    { 'id':         'REMOVEFORMAT_TEXT-1',
      'desc':       'check whether the "removeformat" command is enabled',
      'qcenabled':  'removeformat' },

    { 'id':         'COPY_TEXT-1',
      'desc':       'check whether the "copy" command is enabled',
      'qcenabled':  'copy' },

    { 'id':         'CUT_TEXT-1',
      'desc':       'check whether the "cut" command is enabled',
      'qcenabled':  'cut' },

    { 'id':         'PASTE_TEXT-1',
      'desc':       'check whether the "paste" command is enabled',
      'qcenabled':  'paste' },

    { 'id':         'UNDO_TEXT-1',
      'desc':       'check whether the "undo" command is enabled',
      'qcenabled':  'undo' },

    { 'id':         'REDO_TEXT-1',
      'desc':       'check whether the "redo" command is enabled',
      'qcenabled':  'redo' },

    { 'id':         'SELECTALL_TEXT-1',
      'desc':       'check whether the "selectall" command is enabled',
      'qcenabled':  'selectall' },

    { 'id':         'UNSELECT_TEXT-1',
      'desc':       'check whether the "unselect" command is enabled',
      'qcenabled':  'unselect' },

    { 'id':         'garbage-1_TEXT-1',
      'desc':       'check correct return value with garbage input',
      'qcenabled':  '#!#@7',
      'expected':   False }
  ]
}

