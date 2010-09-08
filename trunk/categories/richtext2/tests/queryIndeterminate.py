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

"""queryCommandIndeterminate tests"""

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

QUERYINDETERMINATE_TESTS = {
  'id':            'QI',
  'caption':       'queryCommandIndeterminate Tests',
  'checkAttrs':    False,
  'checkStyle':    False,
  'checkSel':      False,
  'styleWithCSS':  False,

  'Proposed': [
    { 'id':          'B:TEXT-1_SI',
      'desc':        'check whether the "bold" command is indeterminate',
      'qcindeterm':  'bold',
      'pad':         'foo[bar]baz',
      'expected':    False },

    { 'id':          'B:B-1_SI',
      'desc':        'check whether the "bold" command is indeterminate',
      'qcindeterm':  'bold',
      'pad':         '<b>foo[bar]baz</b>',
      'expected':    False },

    { 'id':          'I:TEXT-1_SI',
      'desc':        'check whether the "bold" command is indeterminate',
      'qcindeterm':  'italic',
      'pad':         'foo[bar]baz',
      'expected':    False },

    { 'id':          'I:I-1_SI',
      'desc':        'check whether the "bold" command is indeterminate',
      'qcindeterm':  'italic',
      'pad':         '<i>foo[bar]baz</i>',
      'expected':    False }
  ]
}

QUERYINDETERMINATE_TESTS_CSS = {
  'id':           'QIC',
  'caption':      'queryCommandIndeterminate Tests, using styleWithCSS',
  'checkAttrs':   False,
  'checkStyle':   False,
  'checkSel':     False,
  'styleWithCSS': True,
  
  'Proposed':     QUERYINDETERMINATE_TESTS['Proposed']
}

