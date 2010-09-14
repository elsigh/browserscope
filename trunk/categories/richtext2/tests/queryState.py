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

"""queryCommandState tests"""

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

QUERYSTATE_TESTS = {
  'id':            'QS',
  'caption':       'queryCommandState Tests',
  'checkAttrs':    False,
  'checkStyle':    False,
  'checkSel':      False,
  'styleWithCSS':  False,

  'Proposed': [
    # bold
    { 'id':         'B_TEXT_SI',
      'rte1-id':    'q-bold-0',
      'desc':       'query the state of the "bold" command',
      'qcstate':    'bold',
      'pad':        'foo[bar]baz',
      'expected':   False },

    { 'id':         'B_B-1_SI',
      'rte1-id':    'q-bold-1',
      'desc':       'query the state of the "bold" command',
      'qcstate':    'bold',
      'pad':        '<b>foo[bar]baz</b>',
      'expected':   True },

    { 'id':         'B_STRONG-1_SI',
      'rte1-id':    'q-bold-2',
      'desc':       'query the state of the "bold" command',
      'qcstate':    'bold',
      'pad':        '<strong>foo[bar]baz</strong>',
      'expected':   True },

    { 'id':         'B_SPANs:fw:b-1_SI',
      'rte1-id':    'q-bold-3',
      'desc':       'query the state of the "bold" command',
      'qcstate':    'bold',
      'pad':        '<span style="font-weight: bold">foo[bar]baz</span>',
      'expected':   True },

    { 'id':         'B_SPANs:fw:n-1_SI',
      'desc':       'query the state of the "bold" command',
      'qcstate':    'bold',
      'pad':        '<span style="font-weight: normal">foo[bar]baz</span>',
      'expected':   False },

    { 'id':         'B_Bs:fw:n-1_SI',
      'rte1-id':    'q-bold-4',
      'desc':       'query the state of the "bold" command',
      'qcstate':    'bold',
      'pad':        '<span style="font-weight: normal">foo[bar]baz</span>',
      'expected':   False },

    { 'id':         'B_B-SPANs:fw:n-1_SI',
      'rte1-id':    'q-bold-5',
      'desc':       'query the state of the "bold" command',
      'qcstate':    'bold',
      'pad':        '<b><span style="font-weight: normal">foo[bar]baz</span></b>',
      'expected':   False },

    { 'id':         'B_SPAN.b-1-SI',
      'desc':       'query the state of the "bold" command',
      'qcstate':    'bold',
      'pad':        '<span class="b">foo[bar]baz</span>',
      'expected':   True },

    { 'id':         'B_MYB-1-SI',
      'desc':       'query the state of the "bold" command',
      'qcstate':    'bold',
      'pad':        '<myb>foo[bar]baz</myb>',
      'expected':   True },

    # italic
    { 'id':         'I_TEXT_SI',
      'rte1-id':    'q-italic-0',
      'desc':       'query the state of the "italic" command',
      'qcstate':    'italic',
      'pad':        'foo[bar]baz',
      'expected':   False },

    { 'id':         'I_I-1_SI',
      'rte1-id':    'q-italic-1',
      'desc':       'query the state of the "italic" command',
      'qcstate':    'italic',
      'pad':        '<i>foo[bar]baz</i>',
      'expected':   True },

    { 'id':         'I_EM-1_SI',
      'rte1-id':    'q-italic-2',
      'desc':       'query the state of the "italic" command',
      'qcstate':    'italic',
      'pad':        '<em>foo[bar]baz</em>',
      'expected':   True },

    { 'id':         'I_SPANs:fs:i-1_SI',
      'rte1-id':    'q-italic-3',
      'desc':       'query the state of the "italic" command',
      'qcstate':    'italic',
      'pad':        '<span style="font-style: italic">foo[bar]baz</span>',
      'expected':   True },

    { 'id':         'I_SPANs:fs:n-1_SI',
      'desc':       'query the state of the "italic" command',
      'qcstate':    'italic',
      'pad':        '<span style="font-style: normal">foo[bar]baz</span>',
      'expected':   False },

    { 'id':         'I_I-SPANs:fs:n-1_SI',
      'rte1-id':    'q-italic-4',
      'desc':       'query the state of the "italic" command',
      'qcstate':    'italic',
      'pad':        '<i><span style="font-style: normal">foo[bar]baz</span></i>',
      'expected':   False },

    { 'id':         'I_SPAN.i-1-SI',
      'desc':       'query the state of the "italic" command',
      'qcstate':    'italic',
      'pad':        '<span class="i">foo[bar]baz</span>',
      'expected':   True },

    { 'id':         'I_MYI-1-SI',
      'desc':       'query the state of the "italic" command',
      'qcstate':    'italic',
      'pad':        '<myi>foo[bar]baz</myi>',
      'expected':   True },

    # underline
    { 'id':         'U_TEXT_SI',
      'rte1-id':    'q-underline-0',
      'desc':       'query the state of the "underline" command',
      'qcstate':    'underline',
      'pad':        'foo[bar]baz',
      'expected':   False },

    { 'id':         'U_U-1_SI',
      'rte1-id':    'q-underline-1',
      'desc':       'query the state of the "underline" command',
      'qcstate':    'underline',
      'pad':        '<u>foo[bar]baz</u>',
      'expected':   True },

    { 'id':         'U_Us:td:n-1_SI',
      'rte1-id':    'q-underline-4',
      'desc':       'query the state of the "underline" command',
      'qcstate':    'underline',
      'pad':        '<u style="text-decoration: none">foo[bar]baz</u>',
      'expected':   False },

    { 'id':         'U_Ah:url-1_SI',
      'rte1-id':    'q-underline-2',
      'desc':       'query the state of the "underline" command',
      'qcstate':    'underline',
      'pad':        '<a href="http://www.foo.com">foo[bar]baz</a>',
      'expected':   True },

    { 'id':         'U_Ah:url.s:td:n-1_SI',
      'rte1-id':    'q-underline-5',
      'desc':       'query the state of the "underline" command',
      'qcstate':    'underline',
      'pad':        '<a href="http://www.foo.com" style="text-decoration: none">foo[bar]baz</a>',
      'expected':   False },

    { 'id':         'U_SPANs:td:u-1_SI',
      'rte1-id':    'q-underline-3',
      'desc':       'query the state of the "underline" command',
      'qcstate':    'underline',
      'pad':        '<span style="text-decoration: underline">foo[bar]baz</span>',
      'expected':   True },

    { 'id':         'U_SPAN.u-1-SI',
      'desc':       'query the state of the "underline" command',
      'qcstate':    'underline',
      'pad':        '<span class="u">foo[bar]baz</span>',
      'expected':   True },

    { 'id':         'U_MYU-1-SI',
      'desc':       'query the state of the "underline" command',
      'qcstate':    'underline',
      'pad':        '<myu>foo[bar]baz</myu>',
      'expected':   True },

    # strikethrough
    { 'id':         'S_TEXT_SI',
      'rte1-id':    'q-strikethrough-0',
      'desc':       'query the state of the "strikethrough" command',
      'qcstate':    'strikethrough',
      'pad':        'foo[bar]baz',
      'expected':   False },

    { 'id':         'S_S-1_SI',
      'rte1-id':    'q-strikethrough-3',
      'desc':       'query the state of the "strikethrough" command',
      'qcstate':    'strikethrough',
      'pad':        '<s>foo[bar]baz</s>',
      'expected':   True },

    { 'id':         'S_STRIKE-1_SI',
      'rte1-id':    'q-strikethrough-1',
      'desc':       'query the state of the "strikethrough" command',
      'qcstate':    'strikethrough',
      'pad':        '<strike>foo[bar]baz</strike>',
      'expected':   True },

    { 'id':         'S_STRIKEs:td:n-1_SI',
      'rte1-id':    'q-strikethrough-2',
      'desc':       'query the state of the "strikethrough" command',
      'qcstate':    'strikethrough',
      'pad':        '<strike style="text-decoration: none">foo[bar]baz</strike>',
      'expected':   False },

    { 'id':         'S_DEL-1_SI',
      'rte1-id':    'q-strikethrough-4',
      'desc':       'query the state of the "strikethrough" command',
      'qcstate':    'strikethrough',
      'pad':        '<del>foo[bar]baz</del>',
      'expected':   True },

    { 'id':         'S_SPANs:td:lt-1_SI',
      'rte1-id':    'q-strikethrough-5',
      'desc':       'query the state of the "strikethrough" command',
      'qcstate':    'strikethrough',
      'pad':        '<span style="text-decoration: line-through">foo[bar]baz</span>',
      'expected':   True },

    { 'id':         'S_SPAN.s-1-SI',
      'desc':       'query the state of the "strikethrough" command',
      'qcstate':    'strikethrough',
      'pad':        '<span class="s">foo[bar]baz</span>',
      'expected':   True },

    { 'id':         'S_MYS-1-SI',
      'desc':       'query the state of the "strikethrough" command',
      'qcstate':    'strikethrough',
      'pad':        '<mys>foo[bar]baz</mys>',
      'expected':   True },

    # subscript
    { 'id':         'SUB_TEXT_SI',
      'rte1-id':    'q-subscript-0',
      'desc':       'query the state of the "subscript" command',
      'qcstate':    'subscript',
      'pad':        'foo[bar]baz',
      'expected':   False },

    { 'id':         'SUB_SUB-1_SI',
      'rte1-id':    'q-subscript-1',
      'desc':       'query the state of the "subscript" command',
      'qcstate':    'subscript',
      'pad':        '<sub>foo[bar]baz</sub>',
      'expected':   True },

    { 'id':         'SUB_SPAN.sub-1-SI',
      'desc':       'query the state of the "subscript" command',
      'qcstate':    'subscript',
      'pad':        '<span class="sub">foo[bar]baz</span>',
      'expected':   True },

    { 'id':         'SUB_MYSUB-1-SI',
      'desc':       'query the state of the "subscript" command',
      'qcstate':    'subscript',
      'pad':        '<mysub>foo[bar]baz</mysub>',
      'expected':   True },

    # superscript
    { 'id':         'SUP_TEXT_SI',
      'rte1-id':    'q-superscript-0',
      'desc':       'query the state of the "superscript" command',
      'qcstate':    'superscript',
      'pad':        'foo[bar]baz',
      'expected':   False },

    { 'id':         'SUP_SUP-1_SI',
      'rte1-id':    'q-superscript-1',
      'desc':       'query the state of the "superscript" command',
      'qcstate':    'superscript',
      'pad':        '<sup>foo[bar]baz</sup>',
      'expected':   True },

    { 'id':         'IOL_TEXT_SI',
      'desc':       'query the state of the "insertorderedlist" command',
      'qcstate':    'insertorderedlist',
      'pad':        'foo[bar]baz',
      'expected':   False },

    { 'id':         'SUP_SPAN.sup-1-SI',
      'desc':       'query the state of the "superscript" command',
      'qcstate':    'superscript',
      'pad':        '<span class="sup">foo[bar]baz</span>',
      'expected':   True },

    { 'id':         'SUP_MYSUP-1-SI',
      'desc':       'query the state of the "superscript" command',
      'qcstate':    'superscript',
      'pad':        '<mysup>foo[bar]baz</mysup>',
      'expected':   True },

    # insertorderedlist
    { 'id':         'IOL_TEXT-1_SI',
      'rte1-id':    'q-insertorderedlist-0',
      'desc':       'query the state of the "insertorderedlist" command',
      'qcstate':    'insertorderedlist',
      'pad':        'foo[bar]baz',
      'expected':   False },

    { 'id':         'IOL_OL-LI-1_SI',
      'rte1-id':    'q-insertorderedlist-1',
      'desc':       'query the state of the "insertorderedlist" command',
      'qcstate':    'insertorderedlist',
      'pad':        '<ol><li>foo[bar]baz</li></ol>',
      'expected':   True },

    { 'id':         'IOL_UL_LI-1_SI',
      'rte1-id':    'q-insertorderedlist-2',
      'desc':       'query the state of the "insertorderedlist" command',
      'qcstate':    'insertorderedlist',
      'pad':        '<ul><li>foo[bar]baz</li></ul>',
      'expected':   False },

    # insertunorderedlist
    { 'id':         'IUL_TEXT_SI',
      'rte1-id':    'q-insertunorderedlist-0',
      'desc':       'query the state of the "insertunorderedlist" command',
      'qcstate':    'insertunorderedlist',
      'pad':        'foo[bar]baz',
      'expected':   False },

    { 'id':         'IUL_OL-LI-1_SI',
      'rte1-id':    'q-insertunorderedlist-1',
      'desc':       'query the state of the "insertunorderedlist" command',
      'qcstate':    'insertunorderedlist',
      'pad':        '<ol><li>foo[bar]baz</li></ol>',
      'expected':   False },

    { 'id':         'IUL_UL-LI-1_SI',
      'rte1-id':    'q-insertunorderedlist-2',
      'desc':       'query the state of the "insertunorderedlist" command',
      'qcstate':    'insertunorderedlist',
      'pad':        '<ul><li>foo[bar]baz</li></ul>',
      'expected':   True },

    # justifycenter
    { 'id':         'JC_TEXT_SI',
      'rte1-id':    'q-justifycenter-0',
      'desc':       'query the state of the "justifycenter" command',
      'qcstate':    'justifycenter',
      'pad':        'foo[bar]baz',
      'expected':   False },

    { 'id':         'JC_DIVa:c-1_SI',
      'rte1-id':    'q-justifycenter-1',
      'desc':       'query the state of the "justifycenter" command',
      'qcstate':    'justifycenter',
      'pad':        '<div align="center">foo[bar]baz</div>',
      'expected':   True },

    { 'id':         'JC_Pa:c-1_SI',
      'rte1-id':    'q-justifycenter-2',
      'desc':       'query the state of the "justifycenter" command',
      'qcstate':    'justifycenter',
      'pad':        '<p align="center">foo[bar]baz</p>',
      'expected':   True },

    { 'id':         'JC_SPANs:ta:c-1_SI',
      'rte1-id':    'q-justifycenter-3',
      'desc':       'query the state of the "justifycenter" command',
      'qcstate':    'justifycenter',
      'pad':        '<div style="text-align: center">foo[bar]baz</div>',
      'expected':   True },

    { 'id':         'JC_SPAN.jc-1-SI',
      'desc':       'query the state of the "justifycenter" command',
      'qcstate':    'justifycenter',
      'pad':        '<span class="jc">foo[bar]baz</span>',
      'expected':   True },

    { 'id':         'JC_MYJC-1-SI',
      'desc':       'query the state of the "justifycenter" command',
      'qcstate':    'justifycenter',
      'pad':        '<myjc>foo[bar]baz</myjc>',
      'expected':   True },

    # justifyfull
    { 'id':         'JF_TEXT_SI',
      'rte1-id':    'q-justifyfull-0',
      'desc':       'query the state of the "justifyfull" command',
      'qcstate':    'justifyfull',
      'pad':        'foo[bar]baz',
      'expected':   False },

    { 'id':         'JF_DIVa:j-1_SI',
      'rte1-id':    'q-justifyfull-1',
      'desc':       'query the state of the "justifyfull" command',
      'qcstate':    'justifyfull',
      'pad':        '<div align="justify">foo[bar]baz</div>',
      'expected':   True },

    { 'id':         'JF_Pa:j-1_SI',
      'rte1-id':    'q-justifyfull-2',
      'desc':       'query the state of the "justifyfull" command',
      'qcstate':    'justifyfull',
      'pad':        '<p align="justify">foo[bar]baz</p>',
      'expected':   True },

    { 'id':         'JF_SPANs:ta:j-1_SI',
      'rte1-id':    'q-justifyfull-3',
      'desc':       'query the state of the "justifyfull" command',
      'qcstate':    'justifyfull',
      'pad':        '<span style="text-align: justify">foo[bar]baz</span>',
      'expected':   True },

    { 'id':         'JF_SPAN.jf-1-SI',
      'desc':       'query the state of the "justifyfull" command',
      'qcstate':    'justifyfull',
      'pad':        '<span class="jf">foo[bar]baz</span>',
      'expected':   True },

    { 'id':         'JF_MYJF-1-SI',
      'desc':       'query the state of the "justifyfull" command',
      'qcstate':    'justifyfull',
      'pad':        '<myjf>foo[bar]baz</myjf>',
      'expected':   True },

    # justifyleft
    { 'id':         'JL_TEXT_SI',
      'desc':       'query the state of the "justifyleft" command',
      'qcstate':    'justifyleft',
      'pad':        'foo[bar]baz',
      'expected':   False },

    { 'id':         'JL_DIVa:l-1_SI',
      'rte1-id':    'q-justifyleft-0',
      'desc':       'query the state of the "justifyleft" command',
      'qcstate':    'justifyleft',
      'pad':        '<div align="left">foo[bar]baz</div>',
      'expected':   True },

    { 'id':         'JL_Pa:l-1_SI',
      'rte1-id':    'q-justifyleft-1',
      'desc':       'query the state of the "justifyleft" command',
      'qcstate':    'justifyleft',
      'pad':        '<p align="left">foo[bar]baz</p>',
      'expected':   True },

    { 'id':         'JL_SPANs:ta:l-1_SI',
      'rte1-id':    'q-justifyleft-2',
      'desc':       'query the state of the "justifyleft" command',
      'qcstate':    'justifyleft',
      'pad':        '<span style="text-align: left">foo[bar]baz</span>',
      'expected':   True },

    { 'id':         'JL_SPAN.jl-1-SI',
      'desc':       'query the state of the "justifyleft" command',
      'qcstate':    'justifyleft',
      'pad':        '<span class="jl">foo[bar]baz</span>',
      'expected':   True },

    { 'id':         'JL_MYJL-1-SI',
      'desc':       'query the state of the "justifyleft" command',
      'qcstate':    'justifyleft',
      'pad':        '<myjl>foo[bar]baz</myjl>',
      'expected':   True },

    # justifyright
    { 'id':         'JR_TEXT_SI',
      'rte1-id':    'q-justifyright-0',
      'desc':       'query the state of the "justifyright" command',
      'qcstate':    'justifyright',
      'pad':        'foo[bar]baz',
      'expected':   False },

    { 'id':         'JR_DIVa:r-1_SI',
      'rte1-id':    'q-justifyright-1',
      'desc':       'query the state of the "justifyright" command',
      'qcstate':    'justifyright',
      'pad':        '<div align="right">foo[bar]baz</div>',
      'expected':   True },

    { 'id':         'JR_Pa:r-1_SI',
      'rte1-id':    'q-justifyright-2',
      'desc':       'query the state of the "justifyright" command',
      'qcstate':    'justifyright',
      'pad':        '<p align="right">foo[bar]baz</p>',
      'expected':   True },

    { 'id':         'JR_SPANs:ta:r-1_SI',
      'rte1-id':    'q-justifyright-3',
      'desc':       'query the state of the "justifyright" command',
      'qcstate':    'justifyright',
      'pad':        '<span style="text-align: right">foo[bar]baz</span>',
      'expected':   True },

    { 'id':         'JR_SPAN.jr-1-SI',
      'desc':       'query the state of the "justifyright" command',
      'qcstate':    'justifyright',
      'pad':        '<span class="jr">foo[bar]baz</span>',
      'expected':   True },
      
    { 'id':         'JR_MYJR-1-SI',
      'desc':       'query the state of the "justifyright" command',
      'qcstate':    'justifyright',
      'pad':        '<myjr>foo[bar]baz</myjr>',
      'expected':   True }
  ]
}

QUERYSTATE_TESTS_CSS = {
  'id':           'QSC',
  'caption':      'queryCommandState Tests, using styleWithCSS',
  'checkAttrs':   False,
  'checkStyle':   False,
  'checkSel':     False,
  'styleWithCSS': True,
  
  'Proposed':     QUERYSTATE_TESTS['Proposed']
}


