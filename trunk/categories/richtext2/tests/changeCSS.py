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
    # font name
    { 'id':          'FN-c:SPANs:ff:a-1_SW',
      'desc':        'Change existing font name to new font name, using CSS styling',
      'command':     'fontname',
      'value':       'courier',
      'pad':         '<span style="font-family: arial">[foo bar baz]</span>',
      'expected':    '<span style="font-family: courier">[foo bar baz]</span>' },

    # font size
    { 'id':          'FS-1:SPANs:fs:l-1_SW',
      'desc':        'Change existing font size to new size, using CSS styling',
      'command':     'fontsize',
      'value':       '1',
      'pad':         '<span style="font-size: large">[foo bar baz]</span>',
      'expected':    '<span style="font-size: x-small">[foo bar baz]</span>' }
  ]
}
