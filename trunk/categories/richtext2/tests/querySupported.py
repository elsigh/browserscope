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
    { 'id':          'BOLD:TEXT',
      'desc':        'check whether the "bold" command is supported',
      'qcsupported': 'bold' },

    { 'id':          'BOLD:B',
      'desc':        'check whether the "bold" command is supported',
      'qcsupported': 'bold',
      'pad':         '<b>foo[bar]baz</b>' },

    { 'id':          'ITALIC:TEXT',
      'desc':        'check whether the "italic" command is supported',
      'qcsupported': 'italic' },

    { 'id':          'ITALIC:I',
      'desc':        'check whether the "italic" command is supported',
      'qcsupported': 'italic',
      'pad':         '<i>foo[bar]baz</i>' },

    { 'id':          'SUBSCRIPT:TEXT',
      'desc':        'check whether the "subscript" command is supported',
      'qcsupported': 'subscript' },

    { 'id':          'SUPERSCRIPT:TEXT',
      'desc':        'check whether the "superscript" command is supported',
      'qcsupported': 'superscript' },

    { 'id':          'STRIKETHROUGH:TEXT',
      'desc':        'check whether the "strikethrough" command is supported',
      'qcsupported': 'strikethrough' },

    { 'id':          'UNDERLINE:TEXT',
      'desc':        'check whether the "underline" command is supported',
      'qcsupported': 'underline' },

    { 'id':          'CREATELINK:TEXT',
      'desc':        'check whether the "createlink" command is supported',
      'qcsupported': 'createlink' },

    { 'id':          'UNLINK:TEXT',
      'desc':        'check whether the "unlink" command is supported',
      'qcsupported': 'unlink' },

    { 'id':          'DELETE:TEXT',
      'desc':        'check whether the "delete" command is supported',
      'qcsupported': 'delete' },

    { 'id':          'FORWARDDELETE:TEXT',
      'desc':        'check whether the "forwarddelete" command is supported',
      'qcsupported': 'forwarddelete' },

    { 'id':          'FORMATBLOCK:TEXT',
      'desc':        'check whether the "formatblock" command is supported',
      'qcsupported': 'formatblock' },

    { 'id':          'INSERTHTML:TEXT',
      'desc':        'check whether the "inserthtml" command is supported',
      'qcsupported': 'inserthtml' },

    { 'id':          'INSERTIMAGE:TEXT',
      'desc':        'check whether the "insertimage" command is supported',
      'qcsupported': 'insertimage' },

    { 'id':          'INSERTLINEBREAK:TEXT',
      'desc':        'check whether the "insertlinebreak" command is supported',
      'qcsupported': 'insertlinebreak' },

    { 'id':          'INSERTORDEREDLIST:TEXT',
      'desc':        'check whether the "insertorderedlist" command is supported',
      'qcsupported': 'insertorderedlist' },

    { 'id':          'INSERTUNORDEREDLIST:TEXT',
      'desc':        'check whether the "insertunorderedlist" command is supported',
      'qcsupported': 'insertunorderedlist' },

    { 'id':          'INSERTPARAGRAPH:TEXT',
      'desc':        'check whether the "insertparagraph" command is supported',
      'qcsupported': 'insertparagraph' },

    { 'id':          'INSERTTEXT:TEXT',
      'desc':        'check whether the "inserttext" command is supported',
      'qcsupported': 'inserttext' },

    { 'id':          'UNDO:TEXT',
      'desc':        'check whether the "undo" command is supported',
      'qcsupported': 'undo' },

    { 'id':          'REDO:TEXT',
      'desc':        'check whether the "redo" command is supported',
      'qcsupported': 'redo' },

    { 'id':          'SELECTALL:TEXT',
      'desc':        'check whether the "selectall" command is supported',
      'qcsupported': 'selectall' },

    { 'id':          'UNSELECT:TEXT',
      'desc':        'check whether the "unselect" command is supported',
      'qcsupported': 'unselect' }
  ]
}


