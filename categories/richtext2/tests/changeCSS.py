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

"""Change with CSS tests"""

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

# "styleWithCSS" tests: Newly created elements should ALWAYS create a "style" attribute.

CHANGE_TESTS_CSS = {
  'id':            'CC',
  'caption':       'Change Existing Format to Different Format Tests, using styleWithCSS',
  'checkAttrs':    True,
  'checkStyle':    True,
  'styleWithCSS':  True,

  'Proposed': [
    # --- MIDAS spec ---

    # backcolor
    { 'id':         'BC-gray:SPANs:bc:g-1_SW',
      'desc':       'Change background color from blue to gray',
      'command':    'backcolor',
      'value':      'gray',
      'pad':        '<span style="background-color: blue">[foobarbaz]</span>',
      'expected':   '<span style="background-color: gray">[foobarbaz]</span>' },

    { 'id':         'BC-gray:SPANs:bc:g-1_SO',
      'desc':       'Change background color from blue to gray',
      'command':    'backcolor',
      'value':      'gray',
      'pad':        '{<span style="background-color: blue">foobarbaz</span>}',
      'expected':   [ '{<span style="background-color: gray">foobarbaz</span>}',
                      '<span style="background-color: gray">[foobarbaz]</span>' ] },

    { 'id':         'BC-gray:SPANs:bc:g-1_SI',
      'desc':       'Change background color from blue to gray',
      'command':    'backcolor',
      'value':      'gray',
      'pad':        '<span style="background-color: blue">foo[bar]baz</span>',
      'expected':   '<span style="background-color: blue">foo</span><span style="background-color: gray">[bar]</span><span style="background-color: blue">baz</span>',
      'accept':     '<span style="background-color: blue">foo<span style="background-color: gray">[bar]</span>baz</span>' },

    { 'id':         'BC-gray:P-SPANs:bc:g-1_SW',
      'desc':       'Change background color within a paragraph from blue to gray',
      'command':    'backcolor',
      'value':      'gray',
      'pad':        '<p><span style="background-color: blue">[foobarbaz]</span></p>',
      'expected':   [ '<p><span style="background-color: gray">[foobarbaz]</span></p>',
                      '<p style="background-color: gray">[foobarbaz]</p>' ] },

    { 'id':         'BC-gray:P-SPANs:bc:g-2_SW',
      'desc':       'Change background color within a paragraph from blue to gray',
      'command':    'backcolor',
      'value':      'gray',
      'pad':        '<p>foo<span style="background-color: blue">[bar]</span>baz</p>',
      'expected':   '<p>foo<span style="background-color: gray">[bar]</span>baz</p>' },

    { 'id':         'BC-gray:P-SPANs:bc:g-3_SO',
      'desc':       'Change background color within a paragraph from blue to gray (selection encloses more than previous span)',
      'command':    'backcolor',
      'value':      'gray',
      'pad':        '<p>[foo<span style="background-color: blue">barbaz</span>qoz]quz</p>',
      'expected':   '<p><span style="background-color: gray">[foobarbazqoz]</span>quz</p>' },

    { 'id':         'BC-gray:P-SPANs:bc:g-3_SL',
      'desc':       'Change background color within a paragraph from blue to gray (previous span partially selected)',
      'command':    'backcolor',
      'value':      'gray',
      'pad':        '<p>[foo<span style="background-color: blue">bar]baz</span>qozquz</p>',
      'expected':   '<p><span style="background-color: gray">[foobar]</span><span style="background-color: blue">baz</span>qozquz</p>' },

    # font name
    { 'id':         'FN-c:SPANs:ff:a-1_SW',
      'desc':       'Change existing font name to new font name, using CSS styling',
      'command':    'fontname',
      'value':      'courier',
      'pad':        '<span style="font-family: arial">[foobarbaz]</span>',
      'expected':   '<span style="font-family: courier">[foobarbaz]</span>' },

    { 'id':         'FN-c:FONTf:a-1_SW',
      'desc':       'Change existing font name to new font name, using CSS styling',
      'command':    'fontname',
      'value':      'courier',
      'pad':        '<font face="arial">[foobarbaz]</font>',
      'expected':   [ '<font style="font-family: courier">[foobarbaz]</font>',
                      '<span style="font-family: courier">[foobarbaz]</span>' ] },

    { 'id':         'FN-c:FONTf:a-1_SI',
      'desc':       'Change existing font name to new font name, using CSS styling',
      'command':    'fontname',
      'value':      'courier',
      'pad':        '<font face="arial">foo[bar]baz</font>',
      'expected':   '<font face="arial">foo</font><span style="font-family: courier">[bar]</span><font face="arial">baz</font>' },

    { 'id':         'FN-a:FONTf:a-1_SI',
      'desc':       'Change existing font name to same font name, using CSS styling (should be noop)',
      'command':    'fontname',
      'value':      'courier',
      'pad':        '<font face="arial">foo[bar]baz</font>',
      'expected':   '<font face="arial">foo[bar]baz</font>' },

    { 'id':         'FN-a:FONTf:a-1_SW',
      'desc':       'Change existing font name to same font name, using CSS styling (should be noop or perhaps change tag)',
      'command':    'fontname',
      'value':      'courier',
      'pad':        '<font face="arial">[foobarbaz]</font>',
      'expected':   [ '<font face="arial">[foobarbaz]</font>',
                      '<span style="font-family: arial">[foobarbaz]</span>' ] },

    { 'id':         'FN-a:FONTf:a-1_SO',
      'desc':       'Change existing font name to same font name, using CSS styling (should be noop or perhaps change tag)',
      'command':    'fontname',
      'value':      'courier',
      'pad':        '{<font face="arial">foobarbaz</font>}',
      'expected':   [ '{<font face="arial">foobarbaz</font>}',
                      '<font face="arial">[foobarbaz]</font>',
                      '{<span style="font-family: arial">foobarbaz</span>}',
                      '<span style="font-family: arial">[foobarbaz]</span>' ] },

    { 'id':         'FN-a:SPANs:ff:a-1_SI',
      'desc':       'Change existing font name to same font name, using CSS styling (should be noop)',
      'command':    'fontname',
      'value':      'courier',
      'pad':        '<span style="font-family: arial">[foobarbaz]</span>',
      'expected':   '<span style="font-family: arial">[foobarbaz]</span>' },

    { 'id':         'FN-c:FONTf:a-2_SL',
      'desc':       'Change existing font name to new font name, using CSS styling',
      'command':    'fontname',
      'value':      'courier',
      'pad':        'foo[bar<font face="arial">baz]qoz</font>',
      'expected':   'foo<span style="font-family: courier">[barbaz]</span><font face="arial">qoz</font>' },

    # font size
    { 'id':         'FS-1:SPANs:fs:l-1_SW',
      'desc':       'Change existing font size to new size, using CSS styling',
      'command':    'fontsize',
      'value':      '1',
      'pad':        '<span style="font-size: large">[foobarbaz]</span>',
      'expected':   '<span style="font-size: x-small">[foobarbaz]</span>' },

    { 'id':         'FS-large:SPANs:fs:l-1_SW',
      'desc':       'Change existing font size to same size (should be noop)',
      'command':    'fontsize',
      'value':      'large',
      'pad':        '<span style="font-size: large">[foobarbaz]</span>',
      'expected':   '<span style="font-size: large">[foobarbaz]</span>' },

    { 'id':         'FS-18px:SPANs:fs:l-1_SW',
      'desc':       'Change existing font size to equivalent px size (should be noop, or change unit)',
      'command':    'fontsize',
      'value':      '18px',
      'pad':        '<span style="font-size: large">[foobarbaz]</span>',
      # note: both expectations are treated as equivalent anyway - here for documentation purposes only
      'expected':   [ '<span style="font-size: large">[foobarbaz]</span>',
                      '<span style="font-size: large">[foobarbaz]</span>' ] },

    { 'id':         'FS-4:SPANs:fs:l-1_SW',
      'desc':       'Change existing font size to equivalent numeric size (should be noop)',
      'command':    'fontsize',
      'value':      '4',
      'pad':        '<span style="font-size: large">[foobarbaz]</span>',
      'expected':   '<span style="font-size: large">[foobarbaz]</span>' },

    { 'id':         'FS-4:SPANs:fs:18px-1_SW',
      'desc':       'Change existing font size to equivalent numeric size (should be noop)',
      'command':    'fontsize',
      'value':      '4',
      'pad':        '<span style="font-size: 18px">[foobarbaz]</span>',
      'expected':   '<span style="font-size: 18px">[foobarbaz]</span>' },
      
    { 'id':         'FS-larger:SPANs:fs:l-1_SI',
      'desc':       'Change selection to use next larger font',
      'command':    'fontsize',
      'value':      'larger',
      'pad':        '<span style="font-size: large">foo[bar]baz</span>',
      'expected':   [ '<span style="font-size: large">foo<span style="font-size: x-large">[bar]</span>baz</span>',
                      '<span style="font-size: large">foo</span><span style="font-size: x-large">[bar]</span><span style="font-size: large">baz</span>' ],
      'accept':     '<span style="font-size: large">foo<font size="larger">[bar]</font>baz</span>' },
                    
    { 'id':         'FS-smaller:SPANs:fs:l-1_SI',
      'desc':       'Change selection to use next smaller font',
      'command':    'fontsize',
      'value':      'smaller',
      'pad':        '<span style="font-size: large">foo[bar]baz</span>',
      'expected':   [ '<span style="font-size: large">foo<span style="font-size: medium">[bar]</span>baz</span>',
                      '<span style="font-size: large">foo</span><span style="font-size: medium">[bar]</span><span style="font-size: large">baz</span>' ],
      'accept':     '<span style="font-size: large">foo<font size="smaller">[bar]</font>baz</span>' }
  ]
}
