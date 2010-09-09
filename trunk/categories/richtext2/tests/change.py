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

"""Change tests"""

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

# Non-"styleWithCSS" tests: Newly created elements should not create a "style" attribute unless necessary.

CHANGE_TESTS = {
  'id':            'C',
  'caption':       'Change Existing Format to Different Format Tests',
  'checkAttrs':    True,
  'checkStyle':    True,
  'styleWithCSS':  False,

  'Proposed': [
    # --- HTML5 spec ---

    # italic
    { 'id':         'I:I-1_SL',
      'desc':       'Italicize partially italicized text',
      'command':    'italic',
      'pad':        'foo[bar<i>baz]</i>qoz',
      'expected':   'foo<i>[barbaz]</i>qoz' },

    { 'id':         'I:B-I-1_SO',
      'desc':       'Italicize partially italicized text in bold context',
      'command':    'italic',
      'pad':        '<b>foo[bar<i>baz</i>}</b>',
      'expected':   '<b>foo<i>[barbaz]</i></b>' },

    # underline
    { 'id':         'U:U-1_SO',
      'desc':       'Underline partially underlined text',
      'command':    'underline',
      'pad':        'foo[bar<u>baz</u>qoz]quz', 
      'expected':   'foo<u>[barbazqoz]</u>quz' },

    { 'id':         'U:U-1_SL',
      'desc':       'Underline partially underlined text',
      'command':    'underline',
      'pad':        'foo[bar<u>baz]qoz</u>quz', 
      'expected':   'foo<u>[barbaz]qoz</u>quz' },

    { 'id':         'U:S-U-1_SO',
      'desc':       'Underline partially underlined text in striked context',
      'command':    'underline',
      'pad':        '<s>foo[bar<u>baz</u>}</s>', 
      'expected':   '<s>foo<u>[barbaz]</u></s>' },

    # --- MIDAS spec ---

    # font name
    { 'id':         'FN-c:FONTf:a-1_SW',
      'desc':       'Change existing font name to new font name, not using CSS styling',
      'command':    'fontname',
      'value':      'courier',
      'pad':        '<font face="arial">[foobarbaz]</font>',
      'expected':   '<font face="courier">[foobarbaz]</font>' },

    { 'id':          'FN-c:FONTf:a-1_SI',
      'desc':        'Change existing font name to new font name, using CSS styling',
      'command':     'fontname',
      'value':       'courier',
      'pad':         '<font face="arial">foo[bar]baz</font>',
      'expected':    '<font face="arial">foo</font><font face="courier">[bar]</font><font face="arial">baz</font>' },

    { 'id':          'FN-c:FONTf:a-2_SL',
      'desc':        'Change existing font name to new font name, using CSS styling',
      'command':     'fontname',
      'value':       'courier',
      'pad':         'foo[bar<font face="arial">baz]qoz</font>',
      'expected':    'foo<font face="courier">[barbaz]</font><font face="arial">qoz</font>' },

    # font size
    { 'id':         'FS-1:FONTsz:4-1_SW',
      'desc':       'Change existing font size to new size, not using CSS styling',
      'command':    'fontsize',
      'value':      '1',
      'pad':        '<font size="4">[foobarbaz]</font>',
      'expected':   '<font size="1">[foobarbaz]</font>' },
                    
    { 'id':         'FS-2:FONTc:b.sz:6-1_SI',
      'desc':       'Change the font size in content with a different font size and font color',
      'command':    'fontsize',
      'value':      '2',
      'pad':        '<font color="blue" size="6">foo[bar]baz</font>',
      'expected':   [ '<font color="blue" size="6">foo<font size="2">[bar]</font>baz</font>',
                      '<font color="blue"><font size="6">foo</font><font size="2">[bar]</font><font size="6">baz</font></font>' ] },

    # forecolor
    { 'id':         'FC-g:FONTc:b.sz:6-1_SI',
      'desc':       'Change the font color in content with a different font size and font color',
      'command':    'forecolor',
      'value':      'green',
      'pad':        '<font color="blue" size="6">foo[bar]baz</font>',
      'expected':   [ '<font color="blue" size="6">foo<font color="green">[bar]</font>baz</font>',
                      '<font size="6"><font color="blue">foo<font color="green">[bar]</font><font color="blue">baz</font></font>' ] }
  ]
}
