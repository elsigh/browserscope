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

"""Selection tests"""

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

SELECTION_TESTS = {
  'id':            'S',
  'caption':       'Selection Tests',
  'checkAttrs':    True,
  'checkStyle':    True,
  'checkSel':      True,
  'styleWithCSS':  False,

  'RFC': [
    # selectall
    { 'id':          'ALL:TEXT-1_SI',
      'desc':        'select all, text only',
      'command':     'selectall',
      'pad':         'foo[bar]baz',
      'expected':    [ '[foobarbaz]',
                       '{foobarbaz}' ] },

    { 'id':          'ALL:I-1_SI',
      'desc':        'select all, with outer tags',
      'command':     'selectall',
      'pad':         '<i>foo[bar]baz</i>',
      'expected':    '{<i>foobarbaz</i>}' },

    # unselect
    { 'id':          'UNS:TEXT-1_SI',
      'desc':        'unselect',
      'command':     'unselect',
      'pad':         'foo[bar]baz',
      'expected':    'foobarbaz' },

#    # window.getSelection().selectAllChildren(<element>)
#    { 'id':          'SELALLCHILDREN-DIV',
#      'desc':        'selectAllChildren(<element>) on div',
#      'function':    'window.getSelection().selectAllChildren(document.getElementById("test"));',
#      'pad':         'foo<div id="test">bar <span>baz</span></div>qoz',
#      'expected':    'foo<div id="test">[bar <span>baz</span>]</div>qoz' }
  ]
}

