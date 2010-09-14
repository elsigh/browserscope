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
    # bold
    { 'id':         'B_TEXT_SI',
      'desc':       'query the value of the "bold" command',
      'qcvalue':    'bold',
      'pad':        'foo[bar]baz',
      'expected':   'false' },

    { 'id':         'B_B-1_SI',
      'desc':       'query the value of the "bold" command',
      'qcvalue':    'bold',
      'pad':        '<b>foo[bar]baz</b>',
      'expected':   'true' },

    { 'id':         'B_STRONG-1_SI',
      'desc':       'query the value of the "bold" command',
      'qcvalue':    'bold',
      'pad':        '<strong>foo[bar]baz</strong>',
      'expected':   'true' },

    { 'id':         'B_SPANs:fw:b-1_SI',
      'desc':       'query the value of the "bold" command',
      'qcvalue':    'bold',
      'pad':        '<span style="font-weight: bold">foo[bar]baz</span>',
      'expected':   'true' },

    { 'id':         'B_SPANs:fw:n-1_SI',
      'desc':       'query the value of the "bold" command',
      'qcvalue':    'bold',
      'pad':        '<span style="font-weight: normal">foo[bar]baz</span>',
      'expected':   'false' },

    { 'id':         'B_Bs:fw:n-1_SI',
      'desc':       'query the value of the "bold" command',
      'qcvalue':    'bold',
      'pad':        '<b><span style="font-weight: normal">foo[bar]baz</span></b>',
      'expected':   'false' },

    { 'id':         'B_SPAN.b-1_SI',
      'desc':       'query the value of the "bold" command',
      'qcvalue':    'bold',
      'pad':        '<span class="b">foo[bar]baz</span>',
      'expected':   'true' },

    { 'id':         'B_MYB-1-SI',
      'desc':       'query the state of the "bold" command',
      'qcvalue':    'bold',
      'pad':        '<myb>foo[bar]baz</myb>',
      'expected':   'true' },

    # italic
    { 'id':         'I_TEXT_SI',
      'desc':       'query the value of the "bold" command',
      'qcvalue':    'italic',
      'pad':        'foo[bar]baz',
      'expected':   'false' },

    { 'id':         'I_I-1_SI',
      'desc':       'query the value of the "bold" command',
      'qcvalue':    'italic',
      'pad':        '<i>foo[bar]baz</i>',
      'expected':   'true' },

    { 'id':         'I_EM-1_SI',
      'desc':       'query the value of the "bold" command',
      'qcvalue':    'italic',
      'pad':        '<em>foo[bar]baz</em>',
      'expected':   'true' },

    { 'id':         'I_SPANs:fs:i-1_SI',
      'desc':       'query the value of the "bold" command',
      'qcvalue':    'italic',
      'pad':        '<span style="font-style: italic">foo[bar]baz</span>',
      'expected':   'true' },

    { 'id':         'I_SPANs:fs:n-1_SI',
      'desc':       'query the value of the "bold" command',
      'qcvalue':    'italic',
      'pad':        '<span style="font-style: normal">foo[bar]baz</span>',
      'expected':   'false' },

    { 'id':         'I_I-SPANs:fs:n-1_SI',
      'desc':       'query the value of the "bold" command',
      'qcvalue':    'italic',
      'pad':        '<i><span style="font-style: normal">foo[bar]baz</span></i>',
      'expected':   'false' },

    { 'id':         'I_SPAN.i-1_SI',
      'desc':       'query the value of the "italic" command',
      'qcvalue':    'italic',
      'pad':        '<span class="i">foo[bar]baz</span>',
      'expected':   'true' },

    { 'id':         'I_MYI-1-SI',
      'desc':       'query the state of the "italic" command',
      'qcvalue':    'italic',
      'pad':        '<myi>foo[bar]baz</myi>',
      'expected':   'true' },

    # fontname
    { 'id':         'FN_FONTf:a-1_SI',
      'rte1-id':    'q-fontname-0',
      'desc':       'query the value of the "fontname" command',
      'qcvalue':    'fontname',
      'pad':        '<font face="arial">foo[bar]baz</font>',
      'expected':   'arial' },

    { 'id':         'FN_SPANs:ff:a-1_SI',
      'rte1-id':    'q-fontname-1',
      'desc':       'query the value of the "fontname" command',
      'qcvalue':    'fontname',
      'pad':        '<span style="font-family: arial">foo[bar]baz</span>',
      'expected':   'arial' },

    { 'id':         'FN_FONTf:a.s:ff:c-1_SI',
      'rte1-id':    'q-fontname-2',
      'desc':       'query the value of the "fontname" command',
      'qcvalue':    'fontname',
      'pad':        '<font face="arial" style="font-family: courier">foo[bar]baz</font>',
      'expected':   'courier' },

    { 'id':         'FN_FONTf:a-FONTf:c-1_SI',
      'rte1-id':    'q-fontname-3',
      'desc':       'query the value of the "fontname" command',
      'qcvalue':    'fontname',
      'pad':        '<font face="arial"><font face="courier">foo[bar]baz</font></font>',
      'expected':   'courier' },

    { 'id':         'FN_SPANs:ff:c-FONTf:a-1_SI',
      'rte1-id':    'q-fontname-4',
      'desc':       'query the value of the "fontname" command',
      'qcvalue':    'fontname',
      'pad':        '<span style="font-family: courier"><font face="arial">foo[bar]baz</font></span>',
      'expected':   'arial' },

    { 'id':         'FN_SPAN.fs18px-1_SI',
      'desc':       'query the value of the "fontname" command',
      'qcvalue':    'fontname',
      'pad':        '<span class="courier">foo[bar]baz</span>',
      'expected':   'courier' },

    { 'id':         'FN_MYCOURIER-1-SI',
      'desc':       'query the state of the "fontname" command',
      'qcvalue':    'fontname',
      'pad':        '<mycourier>foo[bar]baz</mycourier>',
      'expected':   'courier' },

    # fontsize
    { 'id':         'FS_FONTsz:4-1_SI',
      'rte1-id':    'q-fontsize-0',
      'desc':       'query the value of the "fontsize" command',
      'qcvalue':    'fontsize',
      'pad':        '<font size=4>foo[bar]baz</font>',
      'expected':   '18px' },

    { 'id':         'FS_FONTs:fs:l-1_SI',
      'desc':       'query the value of the "fontsize" command',
      'qcvalue':    'fontsize',
      'pad':        '<font style="font-size: large">foo[bar]baz</font>',
      'expected':   '18px' },

    { 'id':         'FS_FONT.ass.s:fs:l-1_SI',
      'rte1-id':    'q-fontsize-1',
      'desc':       'query the value of the "fontsize" command',
      'qcvalue':    'fontsize',
      'pad':        '<font class="Apple-style-span" style="font-size: large">foo[bar]baz</font>',
      'expected':   '18px' },

    { 'id':         'FS_FONTsz:1.s:fs:xl-1_SI',
      'rte1-id':    'q-fontsize-2',
      'desc':       'query the value of the "fontsize" command',
      'qcvalue':    'fontsize',
      'pad':        '<font size=1 style="font-size: x-large">foo[bar]baz</font>',
      'expected':   '24px' },

    { 'id':         'FS_SPAN.large-1_SI',
      'desc':       'query the value of the "fontsize" command',
      'qcvalue':    'fontsize',
      'pad':        '<span class="large">foo[bar]baz</span>',
      'expected':   'large' },

    { 'id':         'FS_SPAN.fs18px-1_SI',
      'desc':       'query the value of the "fontsize" command',
      'qcvalue':    'fontsize',
      'pad':        '<span class="fs18px">foo[bar]baz</span>',
      'expected':   '18px' },

    { 'id':         'FA_MYLARGE-1-SI',
      'desc':       'query the state of the "fontsize" command',
      'qcvalue':    'fontsize',
      'pad':        '<mylarge>foo[bar]baz</mylarge>',
      'expected':   'large' },

    { 'id':         'FA_MYFS18PX-1-SI',
      'desc':       'query the state of the "fontsize" command',
      'qcvalue':    'fontsize',
      'pad':        '<myfs18px>foo[bar]baz</myfs18px>',
      'expected':   '18px' },

    # backcolor
    { 'id':         'BC_FONTs:bc:fca-1_SI',
      'rte1-id':    'q-backcolor-0',
      'desc':       'query the value of the "backcolor" command',
      'qcvalue':    'backcolor',
      'pad':        '<font style="background-color: #ffccaa">foo[bar]baz</font>',
      'expected':   '#ffccaa' },

    { 'id':         'BC_SPANs:bc:abc-1_SI',
      'rte1-id':    'q-backcolor-2',
      'desc':       'query the value of the "backcolor" command',
      'qcvalue':    'backcolor',
      'pad':        '<span style="background-color: #aabbcc">foo[bar]baz</span>',
      'expected':   '#aabbcc' },

    { 'id':         'BC_FONTs:bc:084-SPAN-1_SI',
      'desc':       'query the value of the "backcolor" command, where the color was set on an ancestor',
      'qcvalue':    'backcolor',
      'pad':        '<font style="background-color: #008844"><span>foo[bar]baz</span></font>',
      'expected':   '#008844' },

    { 'id':         'BC_SPANs:bc:cde-SPAN-1_SI',
      'desc':       'query the value of the "backcolor" command, where the color was set on an ancestor',
      'qcvalue':    'backcolor',
      'pad':        '<span style="background-color: #ccddee"><span>foo[bar]baz</span></span>',
      'expected':   '#ccddee' },

    { 'id':         'BC_SPAN.ass.s:bc:rgb-1_SI',
      'rte1-id':    'q-backcolor-1',
      'desc':       'query the value of the "backcolor" command',
      'qcvalue':    'backcolor',
      'pad':        '<span class="Apple-style-span" style="background-color: rgb(255, 0, 0)">foo[bar]baz</span>',
      'expected':   '#ff0000' },

    { 'id':         'BC_SPAN.bcred-1_SI',
      'desc':       'query the value of the "backcolor" command',
      'qcvalue':    'backcolor',
      'pad':        '<span class="bcred">foo[bar]baz</span>',
      'expected':   'red' },

    { 'id':         'BC_MYBCRED-1-SI',
      'desc':       'query the state of the "backcolor" command',
      'qcvalue':    'backcolor',
      'pad':        '<mybcred>foo[bar]baz</mybcred>',
      'expected':   'red' },

    # forecolor
    { 'id':         'FC_FONTc:f00-1_SI',
      'rte1-id':    'q-forecolor-0',
      'desc':       'query the value of the "forecolor" command',
      'qcvalue':    'forecolor',
      'pad':        '<font color="#ff0000">foo[bar]baz</font>',
      'expected':   '#ff0000' },

    { 'id':         'FC_SPANs:c:0f0-1_SI',
      'rte1-id':    'q-forecolor-1',
      'desc':       'query the value of the "forecolor" command',
      'qcvalue':    'forecolor',
      'pad':        '<span style="color: #00ff00">foo[bar]baz</span>',
      'expected':   '#00ff00' },

    { 'id':         'FC_FONTc:333.s:c:999-1_SI',
      'rte1-id':    'q-forecolor-2',
      'desc':       'query the value of the "forecolor" command',
      'qcvalue':    'forecolor',
      'pad':        '<font color="#333333" style="color: #999999">foo[bar]baz</font>',
      'expected':   '#999999' },

    { 'id':         'FC_FONTc:641-SPAN-1_SI',
      'desc':       'query the value of the "forecolor" command, where the color was set on an ancestor',
      'qcvalue':    'forecolor',
      'pad':        '<font color="#664411"><span>foo[bar]baz</span></font>',
      'expected':   '#664411' },

    { 'id':         'FC_SPANs:c:d95-SPAN-1_SI',
      'desc':       'query the value of the "forecolor" command, where the color was set on an ancestor',
      'qcvalue':    'forecolor',
      'pad':        '<span style="color: #dd9955"><span>foo[bar]baz</span></span>',
      'expected':   '#dd9955' },

    { 'id':         'FC_SPAN.red-1_SI',
      'desc':       'query the value of the "forecolor" command',
      'qcvalue':    'forecolor',
      'pad':        '<span class="red">foo[bar]baz</span>',
      'expected':   'red' },

    { 'id':         'FC_MYRED-1-SI',
      'desc':       'query the state of the "forecolor" command',
      'qcvalue':    'forecolor',
      'pad':        '<myred>foo[bar]baz</myred>',
      'expected':   'red' },

    # hilitecolor
    { 'id':         'HC_FONTs:bc:fc0-1_SI',
      'rte1-id':    'q-hilitecolor-0',
      'desc':       'query the value of the "hilitecolor" command',
      'qcvalue':    'hilitecolor',
      'pad':        '<font style="background-color: #ffcc00">foo[bar]baz</font>',
      'expected':   '#ffcc00' },

    { 'id':         'HC_SPANs:bc:a0c-1_SI',
      'rte1-id':    'q-hilitecolor-2',
      'desc':       'query the value of the "hilitecolor" command',
      'qcvalue':    'hilitecolor',
      'pad':        '<span style="background-color: #aa00cc">foo[bar]baz</span>',
      'expected':   '#aa00cc' },

    { 'id':         'HC_SPAN.ass.s:bc:rgb-1_SI',
      'rte1-id':    'q-hilitecolor-1',
      'desc':       'query the value of the "hilitecolor" command',
      'qcvalue':    'hilitecolor',
      'pad':        '<span class="Apple-style-span" style="background-color: rgb(255, 0, 0)">foo[bar]baz</span>',
      'expected':   '#ff0000' },

    { 'id':         'HC_FONTs:bc:83e-SPAN-1_SI',
      'desc':       'query the value of the "hilitecolor" command, where the color was set on an ancestor',
      'qcvalue':    'hilitecolor',
      'pad':        '<font style="background-color: #8833ee"><span>foo[bar]baz</span></font>',
      'expected':   '#8833ee' },

    { 'id':         'HC_SPANs:bc:b12-SPAN-1_SI',
      'desc':       'query the value of the "hilitecolor" command, where the color was set on an ancestor',
      'qcvalue':    'hilitecolor',
      'pad':        '<span style="background-color: #bb1122"><span>foo[bar]baz</span></span>',
      'expected':   '#bb1122' },

    { 'id':         'HC_SPAN.bcred-1_SI',
      'desc':       'query the value of the "hilitecolor" command',
      'qcvalue':    'hilitecolor',
      'pad':        '<span class="bcred">foo[bar]baz</span>',
      'expected':   'red' },

    { 'id':         'HC_MYBCRED-1-SI',
      'desc':       'query the state of the "hilitecolor" command',
      'qcvalue':    'hilitecolor',
      'pad':        '<mybcred>foo[bar]baz</mybcred>',
      'expected':   'red' }
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




