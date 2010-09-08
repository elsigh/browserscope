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

"""UnApply tests"""

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

UNAPPLY_TESTS = {
  'id':           'U',
  'caption':      'Unapply Existing Formatting Tests',
  'checkAttrs':   True,
  'checkStyle':   True,
  'styleWithCSS': False,
  'expected':     'foo[bar]baz',

  'RFC': [
    # unlink
    { 'id':         'UNLINK:A-1_SO',
      'desc':       'unlink wrapped <a> element',
      'command':    'unlink',
      'pad':        'foo[<a>bar</a>]baz' },

    { 'id':         'UNLINK:A-1_SW',
      'desc':       'unlink <a> element where the selection wraps the full content',
      'command':    'unlink',
      'pad':        'foo<a>[bar]</a>baz' },

    { 'id':         'UNLINK:An:a.h:id-1_SO',
      'desc':       'unlink wrapped <a> element that has a name and href attribute',
      'command':    'unlink',
      'pad':        'foo[<a name="A" href="#U-UNLINK-1">bar</a>]baz' },

    { 'id':         'UNLINK:A-2_SO',
      'desc':       'unlink contained <a> element',
      'command':    'unlink',
      'pad':        'foo[b<a>a</a>r]baz' },

    { 'id':         'UNLINK:A2-1_SO',
      'desc':       'unlink 2 contained <a> elements',
      'command':    'unlink',
      'pad':        'foo[<a>b</a>a<a>r</a>]baz' }
  ],
    
  'Proposed': [
    # bold
    { 'id':         'B:B-1_SW',
      'desc':       'Selection within tags; remove <b> tags',
      'command':    'bold',
      'pad':        'foo<b>[bar]</b>baz' },

    { 'id':         'B:B-1_SO',
      'desc':       'Selection outside of tags; remove <b> tags',
      'command':    'bold',
      'pad':        'foo[<b>bar</b>]baz' },

    { 'id':         'B:B-1_SL',
      'desc':       'Selection oblique left; remove <b> tags',
      'command':    'bold',
      'pad':        'foo[<b>bar]</b>baz' },

    { 'id':         'B:B-1_SR',
      'desc':       'Selection oblique right; remove <b> tags',
      'command':    'bold',
      'pad':        'foo<b>[bar</b>]baz' },

    { 'id':         'B:STRONG-1_SW',
      'desc':       'Selection within tags; remove <strong> tags',
      'command':    'bold',
      'pad':        'foo<strong>[bar]</strong>baz' },

    { 'id':         'B:STRONG-1_SO',
      'desc':       'Selection outside of tags; remove <strong> tags',
      'command':    'bold',
      'pad':        'foo[<strong>bar</strong>]baz' },

    { 'id':         'B:STRONG-1_SL',
      'desc':       'Selection oblique left; remove <strong> tags',
      'command':    'bold',
      'pad':        'foo[<strong>bar]</strong>baz' },

    { 'id':         'B:STRONG-1_SR',
      'desc':       'Selection oblique right; remove <strong> tags',
      'command':    'bold',
      'pad':        'foo<strong>[bar</strong>]baz' },

    { 'id':         'B:SPANs:fw:b-1_SW',
      'desc':       'Selection within tags; remove "font-weight: bold"',
      'command':    'bold',
      'pad':        'foo<span style="font-weight: bold">[bar]</span>baz' },

    { 'id':         'B:SPANs:fw:b-1_SO',
      'desc':       'Selection outside of tags; remove "font-weight: bold"',
      'command':    'bold',
      'pad':        'foo[<span style="font-weight: bold">bar</span>]baz' },

    { 'id':         'B:SPANs:fw:b-1_SL',
      'desc':       'Selection oblique left; remove "font-weight: bold"',
      'command':    'bold',
      'pad':        'foo[<span style="font-weight: bold">bar]</span>baz' },

    { 'id':         'B:SPANs:fw:b-1_SR',
      'desc':       'Selection oblique right; remove "font-weight: bold"',
      'command':    'bold',
      'pad':        'foo<span style="font-weight: bold">[bar</span>]baz' },

    { 'id':         'B:B-P3-1_SO12',
      'desc':       'Unbolding multiple paragraphs in inside bolded content with content-model violation',
      'command':    'bold',
      'pad':        '<b>{<p>foo</p><p>bar</p>}<p>baz</p></b>',
      'expected':   [ '<p>[foo</p><p>bar]</p><p><b>baz</b></p>',
                      '<p>[foo</p><p>bar]</p><b><p>baz</p></b>' ] },

    { 'id':         'B:B-P-I_SO..P-1',
      'desc':       'Unbolding italicized content inside bolded content with content-model violation',
      'command':    'bold',
      'pad':        '<b><p>foo[<i>bar</i>]</p><p>baz</p></b>',
      'expected':   [ '<p><b>foo</b><i>[bar]</i></p><p><b>baz</b></p>',
                      '<b><p>foo</p></b><p><i>[bar]</i></p><b><p>baz</p></b>' ] },

    # italic
    { 'id':         'I:I-1_SW',
      'desc':       'Selection within tags; remove <i> tags',
      'command':    'italic',
      'pad':        'foo<i>[bar]</i>baz' },

    { 'id':         'I:I-1_SO',
      'desc':       'Selection outside of tags; remove <i> tags',
      'command':    'italic',
      'pad':        'foo[<i>bar</i>]baz' },

    { 'id':         'I:I-1_SL',
      'desc':       'Selection oblique left; remove <i> tags',
      'command':    'italic',
      'pad':        'foo[<i>bar]</i>baz' },

    { 'id':         'I:I-1_SR',
      'desc':       'Selection oblique right; remove <i> tags',
      'command':    'italic',
      'pad':        'foo<i>[bar</i>]baz' },

    { 'id':         'I:EM-1_SI',
      'desc':       'Selection within tags; remove <em> tags',
      'command':    'italic',
      'pad':        'foo<em>[bar]</em>baz' },

    { 'id':         'I:EM-1_SO',
      'desc':       'Selection outside of tags; remove <em> tags',
      'command':    'italic',
      'pad':        'foo[<em>bar</em>]baz' },

    { 'id':         'I:EM-1_SL',
      'desc':       'Selection oblique left; remove <em> tags',
      'command':    'italic',
      'pad':        'foo[<em>bar]</em>baz' },

    { 'id':         'I:EM-1_SR',
      'desc':       'Selection oblique right; remove <em> tags',
      'command':    'italic',
      'pad':        'foo<em>[bar</em>]baz' },

    { 'id':         'I:SPANs:fs:i-1_SW',
      'desc':       'Selection within tags; remove "font-style: italic"',
      'command':    'italic',
      'pad':        'foo<span style="font-style: italic">[bar]</span>baz' },

    { 'id':         'I:SPANs:fs:i-1_SO',
      'desc':       'Selection outside of tags; Italicize "font-style: italic"',
      'command':    'italic',
      'pad':        'foo[<span style="font-style: italic">bar</span>]baz' },

    { 'id':         'I:SPANs:fs:i-1_SL',
      'desc':       'Selection oblique left; Italicize "font-style: italic"',
      'command':    'italic',
      'pad':        'foo[<span style="font-style: italic">bar]</span>baz' },

    { 'id':         'I:SPANs:fs:i-1_SR',
      'desc':       'Selection oblique right; Italicize "font-style: italic"',
      'command':    'italic',
      'pad':        'foo<span style="font-style: italic">[bar</span>]baz' },

    { 'id':         'I:I-P3-1_SO2',
      'desc':       'Unitalicize content with content-model violation',
      'command':    'italic',
      'pad':        '<i><p>foo</p>{<p>bar</p>}<p>baz</p></i>',
      'expected':   [ '<p><i>foo</i></p><p>[bar]</p><p><i>baz</i></p>',
                      '<i><p>foo</p></i><p>[bar]</p><i><p>baz</p></i>' ] },

    # underline
    { 'id':         'U:U-1_SW',
      'desc':       'Selection within tags; remove <u> tags',
      'command':    'underline',
      'pad':        'foo<u>[bar]</u>baz' },

    { 'id':         'U:U-1_SO',
      'desc':       'Selection outside of tags; remove <u> tags',
      'command':    'underline',
      'pad':        'foo[<u>bar</u>]baz' },

    { 'id':         'U:U-1_SL',
      'desc':       'Selection oblique left; remove <u> tags',
      'command':    'underline',
      'pad':        'foo[<u>bar]</u>baz' },

    { 'id':         'U:U-1_SR',
      'desc':       'Selection oblique right; remove <u> tags',
      'command':    'underline',
      'pad':        'foo<u>[bar</u>]baz' },

    { 'id':         'U:SPANs:td:u-1_SW',
      'desc':       'Selection within tags; remove "text-decoration: underline"',
      'command':    'underline',
      'pad':        'foo<span style="text-decoration: underline">[bar]</span>baz' },

    { 'id':         'U:SPANs:td:u-1_SO',
      'desc':       'Selection outside of tags; remove "text-decoration: underline"',
      'command':    'underline',
      'pad':        'foo[<span style="text-decoration: underline">bar</span>]baz' },

    { 'id':         'U:SPANs:td:u-1_SL',
      'desc':       'Selection oblique left; remove "text-decoration: underline"',
      'command':    'underline',
      'pad':        'foo[<span style="text-decoration: underline">bar]</span>baz' },

    { 'id':         'U:SPANs:td:u-1_SR',
      'desc':       'Selection oblique right; remove "text-decoration: underline"',
      'command':    'underline',
      'pad':        'foo<span style="text-decoration: underline">[bar</span>]baz' },

    { 'id':         'U:U-S-1_SO',
      'desc':       'Removing underline from underlined content with striked content',
      'command':    'underline',
      'pad':        '<u>foo[bar<s>baz</s>quoz]</u>',
      'expected':   '<u>foo</u>[bar<s>baz</s>quoz]' },

    { 'id':         'U:U-P3-1_SO',
      'desc':       'Removing underline from underlined content with content-model violation',
      'command':    'underline',
      'pad':        '<u><p>foo</p>{<p>bar</p>}<p>baz</p></u>',
      'expected':   [ '<p><u>foo</u></p><p>[bar]</p><p><u>baz</u></p>',
                      '<u><p>foo</p></u><p>[bar]</p><u><p>baz</p></u>' ] },

    # strikethrough
    { 'id':         'S:S-1_SW',
      'desc':       'Selection within tags; remove <s> tags',
      'command':    'strikethrough',
      'pad':        'foo<s>[bar]</s>baz' },

    { 'id':         'S:S-1_SO',
      'desc':       'Selection outside of tags; remove <s> tags',
      'command':    'strikethrough',
      'pad':        'foo[<s>bar</s>]baz' },

    { 'id':         'S:S-1_SL',
      'desc':       'Selection oblique left; remove <s> tags',
      'command':    'strikethrough',
      'pad':        'foo[<s>bar]</s>baz' },

    { 'id':         'S:S-1_SR',
      'desc':       'Selection oblique right; remove <s> tags',
      'command':    'strikethrough',
      'pad':        'foo<s>[bar</s>]baz' },

    { 'id':         'S:STRIKE-1_SW',
      'desc':       'Selection within tags; remove <strike> tags',
      'command':    'strikethrough',
      'pad':        'foo<strike>[bar]</strike>baz' },

    { 'id':         'S:STRIKE-1_SO',
      'desc':       'Selection outside of tags; remove <strike> tags',
      'command':    'strikethrough',
      'pad':        'foo[<strike>bar</strike>]baz' },

    { 'id':         'S:STRIKE-1_SL',
      'desc':       'Selection oblique left; remove <strike> tags',
      'command':    'strikethrough',
      'pad':        'foo[<strike>bar]</strike>baz' },

    { 'id':         'S:STRIKE-2_SR',
      'desc':       'Selection oblique right; remove <strike> tags',
      'command':    'strikethrough',
      'pad':        'foo<strike>[bar</strike>]baz' },

    { 'id':         'S:SPANs:td:lt-1_SW',
      'desc':       'Selection within tags; remove "text-decoration:line-through"',
      'command':    'strikethrough',
      'pad':        'foo<span style="text-decoration:line-through">[bar]</span>baz' },

    { 'id':         'S:SPANs:td:lt-1_SO',
      'desc':       'Selection outside of tags; Italicize "text-decoration:line-through"',
      'command':    'strikethrough',
      'pad':        'foo[<span style="text-decoration:line-through">bar</span>]baz' },

    { 'id':         'S:SPANs:td:lt-1_SL',
      'desc':       'Selection oblique left; Italicize "text-decoration:line-through"',
      'command':    'strikethrough',
      'pad':        'foo[<span style="text-decoration:line-through">bar]</span>baz' },

    { 'id':         'S:SPANs:td:lt-1_SR',
      'desc':       'Selection oblique right; Italicize "text-decoration:line-through"',
      'command':    'strikethrough',
      'pad':        'foo<span style="text-decoration:line-through">[bar</span>]baz' },

    { 'id':         'S:S-U-1_SI',
      'desc':       'Removing underline from underlined content inside striked content',
      'command':    'strikethrough',
      'pad':        '<s><u>foo[bar]baz</u>quoz</s>',
      'expected':   '<s><u>foo</u></s><u>[bar]</u><s><u>baz</u>quoz</s>' },

    { 'id':         'S:U-S-1_SI',
      'desc':       'Removing underline from striked content inside underlined content',
      'command':    'strikethrough',
      'pad':        '<u><s>foo[bar]baz</s>quoz</u>',
      'expected':   '<u><s>foo</s>[bar]<s>baz</s>quoz</u>' },

    # unlink
    { 'id':         'UNLINK:A-1_SC',
      'desc':       'unlink an <a> element that contains the collapsed selection',
      'command':    'unlink',
      'pad':        'foo<a>ba^r</a>baz',
      'expected':   'fooba^rbaz' },

    { 'id':         'UNLINK:A-1_SI',
      'desc':       'unlink an <a> element that contains the whole selection',
      'command':    'unlink',
      'pad':        'foo<a>b[a]r</a>baz',
      'expected':   'foob[a]rbaz' },

    { 'id':         'UNLINK:A-2_SL',
      'desc':       'unlink a partially contained <a> element',
      'command':    'unlink',
      'pad':        'foo[ba<a>r]ba</a>z' },

    { 'id':         'UNLINK:A-3_SR',
      'desc':       'unlink a partially contained <a> element',
      'command':    'unlink',
      'pad':        'fo<a>o[ba</a>r]baz' }
  ]
}
