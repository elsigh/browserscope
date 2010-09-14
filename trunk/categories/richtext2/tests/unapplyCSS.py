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

"""UnApply with CSS tests"""

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

# Non-"styleWithCSS" tests: "styleWithCSS" should have no bearing on the unapply operation.

UNAPPLY_TESTS_CSS = {
  'id':            'UC',
  'caption':       'Unapply Existing Formatting Tests, using styleWithCSS',
  'checkAttrs':    True,
  'checkStyle':    True,
  'styleWithCSS':  True,
  'expected':      'foo[bar]baz',

  'Proposed': [
    # bold
    { 'id':         'B_B-1_SW',
      'desc':       'Selection within tags; remove <b> tags',
      'command':    'bold',
      'pad':        'foo<b>[bar]</b>baz' },

    { 'id':         'B_B-1_SO',
      'desc':       'Selection outside of tags; remove <b> tags',
      'command':    'bold',
      'pad':        'foo[<b>bar</b>]baz' },

    { 'id':         'B_B-1_SL',
      'desc':       'Selection oblique left; remove <b> tags',
      'command':    'bold',
      'pad':        'foo[<b>bar]</b>baz' },

    { 'id':         'B_B-1_SR',
      'desc':       'Selection oblique right; remove <b> tags',
      'command':    'bold',
      'pad':        'foo<b>[bar</b>]baz' },

    { 'id':         'B_STRONG-1_SW',
      'desc':       'Selection within tags; remove <strong> tags',
      'command':    'bold',
      'pad':        'foo<strong>[bar]</strong>baz' },

    { 'id':         'B_STRONG-1_SO',
      'desc':       'Selection outside of tags; remove <strong> tags',
      'command':    'bold',
      'pad':        'foo[<strong>bar</strong>]baz' },

    { 'id':         'B_STRONG-1_SL',
      'desc':       'Selection oblique left; remove <strong> tags',
      'command':    'bold',
      'pad':        'foo[<strong>bar]</strong>baz' },

    { 'id':         'B_STRONG-1_SR',
      'desc':       'Selection oblique right; remove <strong> tags',
      'command':    'bold',
      'pad':        'foo<strong>[bar</strong>]baz' },

    { 'id':         'B_SPANs:fw:b-1_SW',
      'desc':       'Selection within tags; remove "font-weight: bold"',
      'command':    'bold',
      'pad':        'foo<span style="font-weight: bold">[bar]</span>baz' },

    { 'id':         'B_SPANs:fw:b-1_SO',
      'desc':       'Selection outside of tags; remove "font-weight: bold"',
      'command':    'bold',
      'pad':        'foo[<span style="font-weight: bold">bar</span>]baz' },

    { 'id':         'B_SPANs:fw:b-1_SL',
      'desc':       'Selection oblique left; remove "font-weight: bold"',
      'command':    'bold',
      'pad':        'foo[<span style="font-weight: bold">bar]</span>baz' },

    { 'id':         'B_SPANs:fw:b-1_SR',
      'desc':       'Selection oblique right; remove "font-weight: bold"',
      'command':    'bold',
      'pad':        'foo<span style="font-weight: bold">[bar</span>]baz' },

    # italic
    { 'id':         'I_I-1_SW',
      'desc':       'Selection within tags; remove <i> tags',
      'command':    'italic',
      'pad':        'foo<i>[bar]</i>baz' },

    { 'id':         'I_I-1_SO',
      'desc':       'Selection outside of tags; remove <i> tags',
      'command':    'italic',
      'pad':        'foo[<i>bar</i>]baz' },

    { 'id':         'I_I-1_SL',
      'desc':       'Selection oblique left; remove <i> tags',
      'command':    'italic',
      'pad':        'foo[<i>bar]</i>baz' },

    { 'id':         'I_I-1_SR',
      'desc':       'Selection oblique right; remove <i> tags',
      'command':    'italic',
      'pad':        'foo<i>[bar</i>]baz' },

    { 'id':         'I_EM-1_SW',
      'desc':       'Selection within tags; remove <em> tags',
      'command':    'italic',
      'pad':        'foo<em>[bar]</em>baz' },

    { 'id':         'I_EM-1_SO',
      'desc':       'Selection outside of tags; remove <em> tags',
      'command':    'italic',
      'pad':        'foo[<em>bar</em>]baz' },

    { 'id':         'I_EM-1_SL',
      'desc':       'Selection oblique left; remove <em> tags',
      'command':    'italic',
      'pad':        'foo[<em>bar]</em>baz' },

    { 'id':         'I_EM-1_SR',
      'desc':       'Selection oblique right; remove <em> tags',
      'command':    'italic',
      'pad':        'foo<em>[bar</em>]baz' },

    { 'id':         'I_SPANs:fs:i-1_SW',
      'desc':       'Selection within tags; remove "font-style: italic"',
      'command':    'italic',
      'pad':        'foo<span style="font-style: italic">[bar]</span>baz' },

    { 'id':         'I_SPANs:fs:i-1_SO',
      'desc':       'Selection outside of tags; Italicize "font-style: italic"',
      'command':    'italic',
      'pad':        'foo[<span style="font-style: italic">bar</span>]baz' },

    { 'id':         'I_SPANs:fs:i-1_SL',
      'desc':       'Selection oblique left; Italicize "font-style: italic"',
      'command':    'italic',
      'pad':        'foo[<span style="font-style: italic">bar]</span>baz' },

    { 'id':         'I_SPANs:fs:i-1_SR',
      'desc':       'Selection oblique right; Italicize "font-style: italic"',
      'command':    'italic',
      'pad':        'foo<span style="font-style: italic">[bar</span>]baz' },

    # underline
    { 'id':         'U_U-1_SW',
      'desc':       'Selection within tags; remove <u> tags',
      'command':    'underline',
      'pad':        'foo<u>[bar]</u>baz' },

    { 'id':         'U_U-1_SO',
      'desc':       'Selection outside of tags; remove <u> tags',
      'command':    'underline',
      'pad':        'foo[<u>bar</u>]baz' },

    { 'id':         'U_U-1_SL',
      'desc':       'Selection oblique left; remove <u> tags',
      'command':    'underline',
      'pad':        'foo[<u>bar]</u>baz' },

    { 'id':         'U_U-1_SR',
      'desc':       'Selection oblique right; remove <u> tags',
      'command':    'underline',
      'pad':        'foo<u>[bar</u>]baz' },

    { 'id':         'U_SPANs:td:u-1_SW',
      'desc':       'Selection within tags; remove "text-decoration: underline"',
      'command':    'underline',
      'pad':        'foo<span style="text-decoration: underline">[bar]</span>baz' },

    { 'id':         'U_SPANs:td:u-1_SO',
      'desc':       'Selection outside of tags; remove "text-decoration: underline"',
      'command':    'underline',
      'pad':        'foo[<span style="text-decoration: underline">bar</span>]baz' },

    { 'id':         'U_SPANs:td:u-1_SL',
      'desc':       'Selection oblique left; remove "text-decoration: underline"',
      'command':    'underline',
      'pad':        'foo[<span style="text-decoration: underline">bar]</span>baz' },

    { 'id':         'U_SPANs:td:u-1_SR',
      'desc':       'Selection oblique right; remove "text-decoration: underline"',
      'command':    'underline',
      'pad':        'foo<span style="text-decoration: underline">[bar</span>]baz' },
      
    # strikethrough
    { 'id':         'S_S-1_SW',
      'desc':       'Selection within tags; remove <s> tags',
      'command':    'strikethrough',
      'pad':        'foo<s>[bar]</s>baz' },

    { 'id':         'S_S-1_SO',
      'desc':       'Selection outside of tags; remove <s> tags',
      'command':    'strikethrough',
      'pad':        'foo[<s>bar</s>]baz' },

    { 'id':         'S_S-1_SL',
      'desc':       'Selection oblique left; remove <s> tags',
      'command':    'strikethrough',
      'pad':        'foo[<s>bar]</s>baz' },

    { 'id':         'S_S-1_SR',
      'desc':       'Selection oblique right; remove <s> tags',
      'command':    'strikethrough',
      'pad':        'foo<s>[bar</s>]baz' },

    { 'id':         'S_STRIKE-1_SW',
      'desc':       'Selection within tags; remove <strike> tags',
      'command':    'strikethrough',
      'pad':        'foo<strike>[bar]</strike>baz' },

    { 'id':         'S_STRIKE-1_SO',
      'desc':       'Selection outside of tags; remove <strike> tags',
      'command':    'strikethrough',
      'pad':        'foo[<strike>bar</strike>]baz' },

    { 'id':         'S_STRIKE-1_SL',
      'desc':       'Selection oblique left; remove <strike> tags',
      'command':    'strikethrough',
      'pad':        'foo[<strike>bar]</strike>baz' },

    { 'id':         'S_STRIKE-1_SR',
      'desc':       'Selection oblique right; remove <strike> tags',
      'command':    'strikethrough',
      'pad':        'foo<strike>[bar</strike>]baz' },

    { 'id':         'S_SPANs:td:lt-1_SW',
      'desc':       'Selection within tags; remove "text-decoration:line-through"',
      'command':    'strikethrough',
      'pad':        'foo<span style="text-decoration:line-through">[bar]</span>baz' },

    { 'id':         'S_SPANs:td:lt-1_SO',
      'desc':       'Selection outside of tags; Italicize "text-decoration:line-through"',
      'command':    'strikethrough',
      'pad':        'foo[<span style="text-decoration:line-through">bar</span>]baz' },

    { 'id':         'S_SPANs:td:lt-1_SL',
      'desc':       'Selection oblique left; Italicize "text-decoration:line-through"',
      'command':    'strikethrough',
      'pad':        'foo[<span style="text-decoration:line-through">bar]</span>baz' },

    { 'id':         'S_SPANs:td:lt-1_SR',
      'desc':       'Selection oblique right; Italicize "text-decoration:line-through"',
      'command':    'strikethrough',
      'pad':        'foo<span style="text-decoration:line-through">[bar</span>]baz' },
            
    { 'id':         'S_SPANc:s-1_SW',
      'desc':       'Unapply "strike-through" on interited CSS style',
      'command':    'strikethrough',
      'checkClass': True,
      'pad':        'foo<span class="s">[bar]</span>baz' },

    { 'id':         'S_SPANc:s-2_SI',
      'desc':       'Unapply "strike-through" on interited CSS style',
      'command':    'strikethrough',
      'pad':        '<span class="s">foo[bar]baz</span>',
      'checkClass': True,
      'expected':   '<span class="s">foo</span>[bar]<span class="s">baz</span>',
      'accept':     '<span class="s">foo<span style="text-decoration: none">[bar]</span>baz</span>' }
  ]
}

