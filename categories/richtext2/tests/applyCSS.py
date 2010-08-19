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

"""Apply with CSS tests"""

__author__ = 'rolandsteiner@google.com (Roland Steiner)'

# Result selection should continue to wrap the originally selected HTML (if any).
# Result selection should be inside any newly created element.
# A selection that started as a text selection should remain a text selection.
# Elements that are not or only partially selected should retain their name and attributes.

# "styleWithCSS" tests: Newly created elements should always create a "style" attribute.

APPLY_TESTS_CSS = {
  'id':            'AC',
  'caption':       'Apply Formatting Tests, using styleWithCSS',
  'checkAttrs':    True,
  'checkStyle':    True,
  'styleWithCSS':  True,

  'Proposed': [
    # bold
    { 'id':          'B-TEXT-1',
      'desc':        'Bold selection',
      'command':     'bold',
      'pad':         'foo[bar]baz',
      'expected':    'foo<span style="font-weight: bold">[bar]</span>baz' },

    # italic
    { 'id':          'I-TEXT-1',
      'desc':        'Italicize selection',
      'command':     'italic',
      'pad':         'foo[bar]baz',
      'expected':    'foo<span style="font-style: italic">[bar]</span>baz' },

    # underline
    { 'id':          'U-TEXT-1',
      'desc':        'Underline selection',
      'command':     'underline',
      'pad':         'foo[bar]baz',
      'expected':    'foo<span style="text-decoration: underline">[bar]</span>baz' },

    # strikethrough
    { 'id':          'S-TEXT-1',
      'desc':        'Strike-through selection',
      'command':     'strikethrough',
      'pad':         'foo[bar]baz',
      'expected':    'foo<span style="text-decoration: line-through">[bar]</span>baz' },
      
    # backcolor
    { 'id':          'BC-TEXT-1',
      'desc':        'Change background color',
      'command':     'backcolor',
      'value':       'blue',
      'pad':         'foo[bar]baz',
      'expected':    [ 'foo<span style="background-color: blue">[bar]</span>baz',
                       'foo<font style="background-color: blue">[bar]</font>baz' ] },

    # fontcolor
    { 'id':          'FC-TEXT-1',
      'desc':        'Change the text color',
      'command':     'fontcolor',
      'value':       'blue',
      'pad':         'foo[bar]baz',
      'expected':    [ 'foo<span style="color: blue">[bar]</span>baz',
                       'foo<font style="color: blue">[bar]</font>baz' ] },

    # fontname
    { 'id':          'FN-TEXT-1',
      'desc':        'Change the font name',
      'command':     'fontname',
      'value':       'arial',
      'pad':         'foo[bar]baz',
      'expected':    [ 'foo<span style="font-family: arial">[bar]</span>baz',
                       'foo<font style="font-family: blue">[bar]</font>baz' ] },

    # fontsize
    { 'id':          'FS-TEXT-2',
      'desc':        'Change the font size to "2"',
      'command':     'fontsize',
      'value':       '2',
      'pad':         'foo[bar]baz',
      'expected':    [ 'foo<span style="font-size: small">[bar]</span>baz',
                       'foo<font style="font-size: small">[bar]</font>baz' ] },

    { 'id':          'FS-TEXT-18px',
      'desc':        'Change the font size to "18px"',
      'command':     'fontsize',
      'value':       '18px',
      'pad':         'foo[bar]baz',
      'expected':    [ 'foo<span style="font-size: 18px">[bar]</span>baz',
                       'foo<font style="font-size: 18px">[bar]</font>baz' ] },

    { 'id':          'FS-TEXT-large',
      'desc':        'Change the font size to "large"',
      'command':     'fontsize',
      'value':       'large',
      'pad':         'foo[bar]baz',
      'expected':    [ 'foo<span style="font-size: large">[bar]</span>baz',
                       'foo<font style="font-size: large">[bar]</font>baz' ] },

    # justifycenter
    { 'id':          'JC-TEXT-1',
      'desc':        'justify the text centrally',
      'command':     'justifycenter',
      'pad':         'foo^bar',
      'expected':    [ '<p style="text-align: center">foo^bar</p>',
                       '<div style="text-align: center">foo^bar</div>' ] },

    # justifyfull
    { 'id':          'JF-TEXT-1',
      'desc':        'justify the text fully',
      'command':     'justifyfull',
      'pad':         'foo^bar',
      'expected':    [ '<p style="text-align: justify">foo^bar</p>',
                       '<div style="text-align: justify">foo^bar</div>' ] },

    # justifyleft
    { 'id':          'JL-TEXT-1',
      'desc':        'justify the text left',
      'command':     'justifyleft',
      'pad':         'foo^bar',
      'expected':    [ '<p style="text-align: left">foo^bar</p>',
                       '<div style="text-align: left">foo^bar</div>' ] },

    # justifyright
    { 'id':          'JR-TEXT-1',
      'desc':        'justify the text right',
      'command':     'justifyright',
      'pad':         'foo^bar',
      'expected':    [ '<p style="text-align: right">foo^bar</p>',
                       '<div style="text-align: right">foo^bar</div>' ] }
  ]
};



