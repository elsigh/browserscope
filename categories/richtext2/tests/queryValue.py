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

"""queryCommandValue tests"""

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

QUERYVALUE_TESTS = {
  'id':            'QV',
  'caption':       'queryCommandValue Tests',
  'checkAttrs':    False,
  'checkStyle':    False,
  'checkSel':      False,
  'styleWithCSS':  False,

  'Proposed': [
    { 'id':          'B:TEXT_SI',
      'desc':        'query the value of the "bold" command',
      'qcvalue':     'bold',
      'pad':         'foo[bar]baz',
      'expected':    'false' },

    { 'id':          'B:B-1_SI',
      'desc':        'query the value of the "bold" command',
      'qcvalue':     'bold',
      'pad':         '<b>foo[bar]baz</b>',
      'expected':    'true' },

    { 'id':          'B:STRONG-1_SI',
      'desc':        'query the value of the "bold" command',
      'qcvalue':     'bold',
      'pad':         '<strong>foo[bar]baz</strong>',
      'expected':    'true' },

    { 'id':          'B:SPANs:fw:b-1_SI',
      'desc':        'query the value of the "bold" command',
      'qcvalue':     'bold',
      'pad':         '<span style="font-weight: bold">foo[bar]baz</span>',
      'expected':    'true' },

    { 'id':          'B:SPANs:fw:n-1_SI',
      'desc':        'query the value of the "bold" command',
      'qcvalue':     'bold',
      'pad':         '<span style="font-weight: normal">foo[bar]baz</span>',
      'expected':    'false' },

    { 'id':          'B:Bs:fw:n-1_SI',
      'desc':        'query the value of the "bold" command',
      'qcvalue':     'bold',
      'pad':         '<b><span style="font-weight: normal">foo[bar]baz</span></b>',
      'expected':    'false' },

    { 'id':          'I:TEXT_SI',
      'desc':        'query the value of the "bold" command',
      'qcvalue':     'italic',
      'pad':         'foo[bar]baz',
      'expected':    'false' },

    { 'id':          'I:I-1_SI',
      'desc':        'query the value of the "bold" command',
      'qcvalue':     'italic',
      'pad':         '<i>foo[bar]baz</i>',
      'expected':    'true' },

    { 'id':          'I:EM-1_SI',
      'desc':        'query the value of the "bold" command',
      'qcvalue':     'italic',
      'pad':         '<em>foo[bar]baz</em>',
      'expected':    'true' },

    { 'id':          'I:SPANs:fs:i-1_SI',
      'desc':        'query the value of the "bold" command',
      'qcvalue':     'italic',
      'pad':         '<span style="font-style: italic">foo[bar]baz</span>',
      'expected':    'true' },

    { 'id':          'I:SPANs:fs:n-1_SI',
      'desc':        'query the value of the "bold" command',
      'qcvalue':     'italic',
      'pad':         '<span style="font-style: normal">foo[bar]baz</span>',
      'expected':    'false' },

    { 'id':          'I:I-SPANs:fs:n-1_SI',
      'desc':        'query the value of the "bold" command',
      'qcvalue':     'italic',
      'pad':         '<i><span style="font-style: normal">foo[bar]baz</span></i>',
      'expected':    'false' },

    { 'id':          'FN:FONTf:a-1_SI',
      'desc':        'query the value of the "fontname" command',
      'qcvalue':     'fontname',
      'pad':         '<font face="Arial">foo[bar]baz</font>',
      'expected':    'Arial' },

    { 'id':          'FN:SPANs:ff:a-1_SI',
      'desc':        'query the value of the "fontname" command',
      'qcvalue':     'fontname',
      'pad':         '<span style="font-family: Arial">foo[bar]baz</span>',
      'expected':    'Arial' },

    { 'id':          'FN:FONTf:a.s:ff:c-1_SI',
      'desc':        'query the value of the "fontname" command',
      'qcvalue':     'fontname',
      'pad':         '<font face="Arial" style="font-family: Courier">foo[bar]baz</font>',
      'expected':    'Courier' },

    { 'id':          'FN:FONTf:a-FONTf:c-1_SI',
      'desc':        'query the value of the "fontname" command',
      'qcvalue':     'fontname',
      'pad':         '<font face="Arial"><font face="Courier">foo[bar]baz</font></font>',
      'expected':    'Courier' },

    { 'id':          'FN:SPANs:ff:c-FONTf:a-1_SI',
      'desc':        'query the value of the "fontname" command',
      'qcvalue':     'fontname',
      'pad':         '<span style="font-family: Courier"><font face="Arial">foo[bar]baz</font></span>',
      'expected':    'Arial' },

    { 'id':          'FS:FONTsz:4-1_SI',
      'desc':        'query the value of the "fontsize" command',
      'qcvalue':     'fontsize',
      'pad':         '<font size=4>foo[bar]baz</font>',
      'expected':    '18px' },

    { 'id':          'FS:FONTs:fs:l-1_SI',
      'desc':        'query the value of the "fontsize" command',
      'qcvalue':     'fontsize',
      'pad':         '<font style="font-size: large">foo[bar]baz</font>',
      'expected':    '18px' },

    { 'id':          'FS:FONTsz:1.s:fs:xl-1_SI',
      'desc':        'query the value of the "fontsize" command',
      'qcvalue':     'fontsize',
      'pad':         '<font size=1 style="font-size: x-large">foo[bar]baz</font>',
      'expected':    '24px' },

    { 'id':          'BC:FONTs:bc:fca-1_SI',
      'desc':        'query the value of the "backcolor" command',
      'qcvalue':     'backcolor',
      'pad':         '<font style="background-color: #ffccaa">foo[bar]baz</font>',
      'expected':    '#ffccaa' },

    { 'id':          'BC:SPANs:bc:abc-1_SI',
      'desc':        'query the value of the "backcolor" command',
      'qcvalue':     'backcolor',
      'pad':         '<span style="background-color: #aabbcc">foo[bar]baz</span>',
      'expected':    '#aabbcc' },

    { 'id':          'BC:FONTs:bc:084-SPAN-1_SI',
      'desc':        'query the value of the "backcolor" command, where the color was set on an ancestor',
      'qcvalue':     'backcolor',
      'pad':         '<font style="background-color: #008844"><span>foo[bar]baz</span></font>',
      'expected':    '#008844' },

    { 'id':          'BC:SPANs:bc:cde-SPAN-1_SI',
      'desc':        'query the value of the "backcolor" command, where the color was set on an ancestor',
      'qcvalue':     'backcolor',
      'pad':         '<span style="background-color: #ccddee"><span>foo[bar]baz</span></span>',
      'expected':    '#ccddee' },

    { 'id':          'FC:FONTc:f00-1_SI',
      'desc':        'query the value of the "forecolor" command',
      'qcvalue':     'forecolor',
      'pad':         '<font color="#ff0000">foo[bar]baz</font>',
      'expected':    '#ff0000' },

    { 'id':          'FC:SPANs:c:0f0-1_SI',
      'desc':        'query the value of the "forecolor" command',
      'qcvalue':     'forecolor',
      'pad':         '<span style="color: #00ff00">foo[bar]baz</span>',
      'expected':    '#00ff00' },

    { 'id':          'FC:FONTc:333.s:c:999-1_SI',
      'desc':        'query the value of the "forecolor" command',
      'qcvalue':     'forecolor',
      'pad':         '<font color="#333333" style="color: #999999">foo[bar]baz</font>',
      'expected':    '#999999' },

    { 'id':          'FC:FONTc:641-SPAN-1_SI',
      'desc':        'query the value of the "forecolor" command, where the color was set on an ancestor',
      'qcvalue':     'forecolor',
      'pad':         '<font color="#664411"><span>foo[bar]baz</span></font>',
      'expected':    '#664411' },

    { 'id':          'FC:SPANs:c:d95-SPAN-1_SI',
      'desc':        'query the value of the "forecolor" command, where the color was set on an ancestor',
      'qcvalue':     'forecolor',
      'pad':         '<span style="color: #dd9955"><span>foo[bar]baz</span></span>',
      'expected':    '#dd9955' },

    { 'id':          'HC:FONTs:bc:fc0-1_SI',
      'desc':        'query the value of the "hilitecolor" command',
      'qcvalue':     'hilitecolor',
      'pad':         '<font style="background-color: #ffcc00">foo[bar]baz</font>',
      'expected':    '#ffcc00' },

    { 'id':          'HC:SPANs:bc:a0c-1_SI',
      'desc':        'query the value of the "hilitecolor" command',
      'qcvalue':     'hilitecolor',
      'pad':         '<span style="background-color: #aa00cc">foo[bar]baz</span>',
      'expected':    '#aa00cc' },

    { 'id':          'HC:FONTs:bc:83e-SPAN-1_SI',
      'desc':        'query the value of the "hilitecolor" command, where the color was set on an ancestor',
      'qcvalue':     'hilitecolor',
      'pad':         '<font style="background-color: #8833ee"><span>foo[bar]baz</span></font>',
      'expected':    '#8833ee' },

    { 'id':          'HC:SPANs:bc:b12-SPAN-1_SI',
      'desc':        'query the value of the "hilitecolor" command, where the color was set on an ancestor',
      'qcvalue':     'hilitecolor',
      'pad':         '<span style="background-color: #bb1122"><span>foo[bar]baz</span></span>',
      'expected':    '#bb1122' }
  ]
}

QUERYVALUE_TESTS_CSS = {
  'id':           'QVC',
  'caption':      'queryCommandValue Tests, using styleWithCSS',
  'checkAttrs':   False,
  'checkStyle':   False,
  'checkSel':     False,
  'styleWithCSS': True,
  
  'Proposed':     QUERYVALUE_TESTS['Proposed']
}

