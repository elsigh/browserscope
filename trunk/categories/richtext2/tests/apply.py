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

"""Apply tests"""

__author__ = 'rolandsteiner@google.com (Roland Steiner)'

# Result selection should continue to wrap the originally selected HTML (if any).
# Result selection should be inside any newly created element.
# A selection that started as a text selection should remain a text selection.
# Elements that are not or only partially selected should retain their name and attributes.

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

# Non-"styleWithCSS" tests: Newly created elements should NOT create a "style" attribute unless necessary.

APPLY_TESTS = {
  'id':            'A',
  'caption':       'Apply Formatting Tests',
  'checkAttrs':    True,
  'checkStyle':    True,
  'styleWithCSS':  False,

  'Proposed': [
    # bold
    { 'id':          'B:TEXT-1_SI',
      'desc':        'Bold selection',
      'command':     'bold',
      'pad':         'foo[bar]baz',
      'expected':    [ 'foo<b>[bar]</b>baz',
                       'foo<strong>[bar]</strong>baz' ] },

    { 'id':          'B:TEXT-1_SIR',
      'desc':        'Bold reversed selection',
      'command':     'bold',
      'pad':         'foo]bar[baz',
      'expected':    [ 'foo<b>[bar]</b>baz',
                       'foo<strong>[bar]</strong>baz' ] },

    { 'id':          'B:I-1_SL',
      'desc':        'Bold selection, partially including italic',
      'command':     'bold',
      'pad':         'foo[bar<i>baz]qoz</i>quz',
      'expected':    [ 'foo<b>[bar</b><i><b>baz]</b>qoz</i>quz',
                       'foo<b>[bar<i>baz]</i></b><i>qoz</i>quz',
                       'foo<strong>[bar</strong><i><strong>baz]</strong>qoz</i>quz',
                       'foo<strong>[bar<i>baz]</i></strong><i>qoz</i>quz' ] },

    # italic
    { 'id':          'I:TEXT-1_SI',
      'desc':        'Italicize selection',
      'command':     'italic',
      'pad':         'foo[bar]baz',
      'expected':    [ 'foo<i>[bar]</i>baz',
                       'foo<em>[bar]</em>baz' ] },

    # underline
    { 'id':          'U:TEXT-1_SI',
      'desc':        'Underline selection',
      'command':     'underline',
      'pad':         'foo[bar]baz',
      'expected':    'foo<u>[bar]</u>baz' },
      
    # strikethrough
    { 'id':          'S:TEXT-1_SI',
      'desc':        'Strike-through selection',
      'command':     'strikethrough',
      'pad':         'foo[bar]baz',
      'expected':    [ 'foo<s>[bar]</s>baz',
                       'foo<strike>[bar]</strike>baz' ] },
      
    # subscript
    { 'id':          'SUB:TEXT-1_SI',
      'desc':        'Change selection to subscript',
      'command':     'subscript',
      'pad':         'foo[bar]baz',
      'expected':    'foo<sub>[bar]</sub>baz' },

    # superscript
    { 'id':          'SUP:TEXT-1_SI',
      'desc':        'Change selection to superscript',
      'command':     'superscript',
      'pad':         'foo[bar]baz',
      'expected':    'foo<sup>[bar]</sup>baz' },

    # backcolor (noteno non-CSS variant available)
    { 'id':          'BC-blue:TEXT-1_SI',
      'desc':        'Change background color (no non-CSS variant available)',
      'command':     'backcolor',
      'value':       'blue',
      'pad':         'foo[bar]baz',
      'expected':    [ 'foo<span style="background-color: blue">[bar]</span>baz',
                       'foo<font style="background-color: blue">[bar]</font>baz' ] },

    # forecolor
    { 'id':          'FC-blue:TEXT-1_SI',
      'desc':        'Change the text color',
      'command':     'forecolor',
      'value':       'blue',
      'pad':         'foo[bar]baz',
      'expected':    'foo<font color="blue">[bar]</font>baz' },

    # fontname
    { 'id':          'FN-a:TEXT-1_SI',
      'desc':        'Change the font name',
      'command':     'fontname',
      'value':       'arial',
      'pad':         'foo[bar]baz',
      'expected':    'foo<font face="arial">[bar]</font>baz' },

    # fontsize
    { 'id':          'FS-2:TEXT-1_SI',
      'desc':        'Change the font size to "2"',
      'command':     'fontsize',
      'value':       '2',
      'pad':         'foo[bar]baz',
      'expected':    'foo<font size="2">[bar]</font>baz' },

    { 'id':          'FS-18px:TEXT-1_SI',
      'desc':        'Change the font size to "18px"',
      'command':     'fontsize',
      'value':       '18px',
      'pad':         'foo[bar]baz',
      'expected':    'foo<font size="18px">[bar]</font>baz' },

    { 'id':          'FS-l:TEXT-1_SI',
      'desc':        'Change the font size to "large"',
      'command':     'fontsize',
      'value':       'large',
      'pad':         'foo[bar]baz',
      'expected':    'foo<font size="large">[bar]</font>baz' },

    # indent
#    { 'id':          'IND:TEXT-1_SI',
#      'desc':        'Indent the text',
#      'command':     'indent',
#      'pad':         'foo[bar]baz',
#      'checkAttrs':  False,  # FIXME: determine generic way to check indent.
#      'expected':    '<blockquote>foo[bar]baz</blockquote>' },

    # outdent
    { 'id':          'OUTD:BQ-1_SC',
      'desc':        'Outdent the text',
      'command':     'outdent',
      'pad':         '<blockquote>foo^bar</blockquote>',
      'expected':    ['foo^bar',
                      '<p>foo^bar</p>',
                      '<div>foo^bar</div>'] },

    # justifycenter
   { 'id':           'JC:TEXT-1_SC',
      'desc':        'justify the text centrally',
      'command':     'justifycenter',
      'pad':         'foo^bar',
      'expected':    [ '<center>foo^bar</center>',
                       '<p align="center">foo^bar</p>',
                       '<p align="middle">foo^bar</p>',
                       '<div align="center">foo^bar</div>',
                       '<div align="middle">foo^bar</div>' ] },

    # justifyfull
    { 'id':          'JF:TEXT-1_SC',
      'desc':        'justify the text fully',
      'command':     'justifyfull',
      'pad':         'foo^bar',
      'expected':    [ '<p align="justify">foo^bar</p>',
                       '<div align="justify">foo^bar</div>' ] },

    # justifyleft
    { 'id':          'JL:TEXT-1_SC',
      'desc':        'justify the text left',
      'command':     'justifyleft',
      'pad':         'foo^bar',
      'expected':    [ '<p align="left">foo^bar</p>',
                       '<div align="left">foo^bar</div>' ] },

    # justifyright
    { 'id':          'JR:TEXT-1_SC',
      'desc':        'justify the text right',
      'command':     'justifyright',
      'pad':         'foo^bar',
      'expected':    [ '<p align="right">foo^bar</p>',
                       '<div align="right">foo^bar</div>' ] },

    # createlink
    { 'id':          'CL:TEXT-1_SC',
      'desc':        'create a link around the selection',
      'command':     'createlink',
      'value':       '#C-CL-1',
      'pad':         'foo[bar]baz',
      'expected':    'foo<a href="#C-CL-1">[bar]</a>baz' }
  ]
}
