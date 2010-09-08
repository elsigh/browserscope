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
    { 'id':          'B:TEXT_SI',
      'desc':        'query the state of the "bold" command',
      'qcstate':     'bold',
      'pad':         'foo[bar]baz',
      'expected':    False },

    { 'id':          'B:B-1_SI',
      'desc':        'query the state of the "bold" command',
      'qcstate':     'bold',
      'pad':         '<b>foo[bar]baz</b>',
      'expected':    True },

    { 'id':          'B:STRONG-1_SI',
      'desc':        'query the state of the "bold" command',
      'qcstate':     'bold',
      'pad':         '<strong>foo[bar]baz</strong>',
      'expected':    True },

    { 'id':          'B:SPANs:fw:b-1_SI',
      'desc':        'query the state of the "bold" command',
      'qcstate':     'bold',
      'pad':         '<span style="font-weight: bold">foo[bar]baz</span>',
      'expected':    True },

    { 'id':          'B:SPANs:fw:n-1_SI',
      'desc':        'query the state of the "bold" command',
      'qcstate':     'bold',
      'pad':         '<span style="font-weight: normal">foo[bar]baz</span>',
      'expected':    False },

    { 'id':          'B:Bs:fw:n-1_SI',
      'desc':        'query the state of the "bold" command',
      'qcstate':     'bold',
      'pad':         '<b><span style="font-weight: normal">foo[bar]baz</span></b>',
      'expected':    False },

    { 'id':          'I:TEXT_SI',
      'desc':        'query the state of the "bold" command',
      'qcstate':     'italic',
      'pad':         'foo[bar]baz',
      'expected':    False },

    { 'id':          'I:I-1_SI',
      'desc':        'query the state of the "bold" command',
      'qcstate':     'italic',
      'pad':         '<i>foo[bar]baz</i>',
      'expected':    True },

    { 'id':          'I:EM-1_SI',
      'desc':        'query the state of the "bold" command',
      'qcstate':     'italic',
      'pad':         '<em>foo[bar]baz</em>',
      'expected':    True },

    { 'id':          'I:SPANs:fs:i-1_SI',
      'desc':        'query the state of the "bold" command',
      'qcstate':     'italic',
      'pad':         '<span style="font-style: italic">foo[bar]baz</span>',
      'expected':    True },

    { 'id':          'I:SPANs:fs:n-1_SI',
      'desc':        'query the state of the "bold" command',
      'qcstate':     'italic',
      'pad':         '<span style="font-style: normal">foo[bar]baz</span>',
      'expected':    False },

    { 'id':          'I:I-SPANs:fs:n-1_SI',
      'desc':        'query the state of the "bold" command',
      'qcstate':     'italic',
      'pad':         '<i><span style="font-style: normal">foo[bar]baz</span></i>',
      'expected':    False },

    { 'id':          'IOL:TEXT_SI',
      'desc':        'query the state of the "insertorderedlist" command',
      'qcstate':     'insertorderedlist',
      'pad':         'foo[bar]baz',
      'expected':    False },

    { 'id':          'IOL:OL-LI-1_SI',
      'desc':        'query the state of the "insertorderedlist" command',
      'qcstate':     'insertorderedlist',
      'pad':         '<ol><li>foo[bar]baz</li></ol>',
      'expected':    True },

    { 'id':          'IOL:UL_LI-1_SI',
      'desc':        'query the state of the "insertorderedlist" command',
      'qcstate':     'insertorderedlist',
      'pad':         '<ul><li>foo[bar]baz</li></ul>',
      'expected':    False },

    { 'id':          'IUL:TEXT_SI',
      'desc':        'query the state of the "insertunorderedlist" command',
      'qcstate':     'insertunorderedlist',
      'pad':         'foo[bar]baz',
      'expected':    False },

    { 'id':          'IUL:OL-LI-1_SI',
      'desc':        'query the state of the "insertunorderedlist" command',
      'qcstate':     'insertunorderedlist',
      'pad':         '<ol><li>foo[bar]baz</li></ol>',
      'expected':    False },

    { 'id':          'IUL:UL-LI-1_SI',
      'desc':        'query the state of the "insertunorderedlist" command',
      'qcstate':     'insertunorderedlist',
      'pad':         '<ul><li>foo[bar]baz</li></ul>',
      'expected':    True },

    { 'id':          'JC:TEXT_SI',
      'desc':        'query the state of the "justifycenter" command',
      'qcstate':     'justifycenter',
      'pad':         'foo[bar]baz',
      'expected':    False },

    { 'id':          'JC:DIVa:c-1_SI',
      'desc':        'query the state of the "justifycenter" command',
      'qcstate':     'justifycenter',
      'pad':         '<div align="center">foo[bar]baz</div>',
      'expected':    True },

    { 'id':          'JC:Pa:c-1_SI',
      'desc':        'query the state of the "justifycenter" command',
      'qcstate':     'justifycenter',
      'pad':         '<p align="center">foo[bar]baz</p>',
      'expected':    True },

    { 'id':          'JC:SPANs:ta:c-1_SI',
      'desc':        'query the state of the "justifycenter" command',
      'qcstate':     'justifycenter',
      'pad':         '<span style="text-align: center">foo[bar]baz</span>',
      'expected':    True },

    { 'id':          'JF:TEXT_SI',
      'desc':        'query the state of the "justifyfull" command',
      'qcstate':     'justifyfull',
      'pad':         'foo[bar]baz',
      'expected':    False },

    { 'id':          'JF:DIVa:j-1_SI',
      'desc':        'query the state of the "justifyfull" command',
      'qcstate':     'justifyfull',
      'pad':         '<div align="justify">foo[bar]baz</div>',
      'expected':    True },

    { 'id':          'JF:Pa:j-1_SI',
      'desc':        'query the state of the "justifyfull" command',
      'qcstate':     'justifyfull',
      'pad':         '<p align="justify">foo[bar]baz</p>',
      'expected':    True },

    { 'id':          'JF:SPANs:ta:j-1_SI',
      'desc':        'query the state of the "justifyfull" command',
      'qcstate':     'justifyfull',
      'pad':         '<span style="text-align: justify">foo[bar]baz</span>',
      'expected':    True },

    { 'id':          'JL:TEXT_SI',
      'desc':        'query the state of the "justifyleft" command',
      'qcstate':     'justifyleft',
      'pad':         'foo[bar]baz',
      'expected':    False },

    { 'id':          'JL:DIVa:l-1_SI',
      'desc':        'query the state of the "justifyleft" command',
      'qcstate':     'justifyleft',
      'pad':         '<div align="left">foo[bar]baz</div>',
      'expected':    True },

    { 'id':          'JL:Pa:l-1_SI',
      'desc':        'query the state of the "justifyleft" command',
      'qcstate':     'justifyleft',
      'pad':         '<p align="left">foo[bar]baz</p>',
      'expected':    True },

    { 'id':          'JL:SPANs:ta:l-1_SI',
      'desc':        'query the state of the "justifyleft" command',
      'qcstate':     'justifyleft',
      'pad':         '<span style="text-align: left">foo[bar]baz</span>',
      'expected':    True },

    { 'id':          'JR:TEXT_SI',
      'desc':        'query the state of the "justifyright" command',
      'qcstate':     'justifyright',
      'pad':         'foo[bar]baz',
      'expected':    False },

    { 'id':          'JR:DIVa:r-1_SI',
      'desc':        'query the state of the "justifyright" command',
      'qcstate':     'justifyright',
      'pad':         '<div align="right">foo[bar]baz</div>',
      'expected':    True },

    { 'id':          'JR:Pa:r-1_SI',
      'desc':        'query the state of the "justifyright" command',
      'qcstate':     'justifyright',
      'pad':         '<p align="right">foo[bar]baz</p>',
      'expected':    True },

    { 'id':          'JR:SPANs:ta:r-1_SI',
      'desc':        'query the state of the "justifyright" command',
      'qcstate':     'justifyright',
      'pad':         '<span style="text-align: right">foo[bar]baz</span>',
      'expected':    True },

    { 'id':          'S:TEXT_SI',
      'desc':        'query the state of the "strikethrough" command',
      'qcstate':     'strikethrough',
      'pad':         'foo[bar]baz',
      'expected':    False },

    { 'id':          'S:S-1_SI',
      'desc':        'query the state of the "strikethrough" command',
      'qcstate':     'strikethrough',
      'pad':         '<s>foo[bar]baz</s>',
      'expected':    True },

    { 'id':          'S:STRIKE-1_SI',
      'desc':        'query the state of the "strikethrough" command',
      'qcstate':     'strikethrough',
      'pad':         '<strike>foo[bar]baz</strike>',
      'expected':    True },

    { 'id':          'S:STRIKEs:td:n-1_SI',
      'desc':        'query the state of the "strikethrough" command',
      'qcstate':     'strikethrough',
      'pad':         '<strike style="text-decoration: none">foo[bar]baz</strike>',
      'expected':    False },

    { 'id':          'S:DEL-1_SI',
      'desc':        'query the state of the "strikethrough" command',
      'qcstate':     'strikethrough',
      'pad':         '<del>foo[bar]baz</del>',
      'expected':    True },

    { 'id':          'S:SPANs:td:lt-1_SI',
      'desc':        'query the state of the "strikethrough" command',
      'qcstate':     'strikethrough',
      'pad':         '<span style="text-decoration: line-through">foo[bar]baz</span>',
      'expected':    True },

    { 'id':          'SUB:TEXT_SI',
      'desc':        'query the state of the "subscript" command',
      'qcstate':     'subscript',
      'pad':         'foo[bar]baz',
      'expected':    False },

    { 'id':          'SUB:SUB-1_SI',
      'desc':        'query the state of the "subscript" command',
      'qcstate':     'subscript',
      'pad':         '<sub>foo[bar]baz</sub>',
      'expected':    True },

    { 'id':          'SUP:TEXT_SI',
      'desc':        'query the state of the "superscript" command',
      'qcstate':     'superscript',
      'pad':         'foo[bar]baz',
      'expected':    False },

    { 'id':          'SUP:SUP-1_SI',
      'desc':        'query the state of the "superscript" command',
      'qcstate':     'superscript',
      'pad':         '<sup>foo[bar]baz</sup>',
      'expected':    True },

    { 'id':          'U:TEXT_SI',
      'desc':        'query the state of the "underline" command',
      'qcstate':     'underline',
      'pad':         'foo[bar]baz',
      'expected':    False },

    { 'id':          'U:U-1_SI',
      'desc':        'query the state of the "underline" command',
      'qcstate':     'underline',
      'pad':         '<u>foo[bar]baz</u>',
      'expected':    True },

    { 'id':          'U:Us:td:n-1_SI',
      'desc':        'query the state of the "underline" command',
      'qcstate':     'underline',
      'pad':         '<u style="text-decoration: none">foo[bar]baz</u>',
      'expected':    False },

    { 'id':          'U:Ah:url-1_SI',
      'desc':        'query the state of the "underline" command',
      'qcstate':     'underline',
      'pad':         '<a href="http://www.foo.com">foo[bar]baz</a>',
      'expected':    True },

    { 'id':          'U:Ah:url.s:td:n-1_SI',
      'desc':        'query the state of the "underline" command',
      'qcstate':     'underline',
      'pad':         '<a href="http://www.foo.com" style="text-decoration: none">foo[bar]baz</a>',
      'expected':    False },

    { 'id':          'U:SPANs:td:u-1_SI',
      'desc':        'query the state of the "underline" command',
      'qcstate':     'underline',
      'pad':         '<span style="text-decoration: underline">foo[bar]baz</span>',
      'expected':    True }
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



