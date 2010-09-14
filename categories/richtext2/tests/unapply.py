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
    { 'id':         'UNLINK_A-1_SO',
      'desc':       'unlink wrapped <a> element',
      'command':    'unlink',
      'pad':        'foo[<a>bar</a>]baz' },

    { 'id':         'UNLINK_A-1_SW',
      'desc':       'unlink <a> element where the selection wraps the full content',
      'command':    'unlink',
      'pad':        'foo<a>[bar]</a>baz' },

    { 'id':         'UNLINK_An:a.h:id-1_SO',
      'desc':       'unlink wrapped <a> element that has a name and href attribute',
      'command':    'unlink',
      'pad':        'foo[<a name="A" href="#UNLINK:An:a.h:id-1_SO">bar</a>]baz' },

    { 'id':         'UNLINK_A-2_SO',
      'desc':       'unlink contained <a> element',
      'command':    'unlink',
      'pad':        'foo[b<a>a</a>r]baz' },

    { 'id':         'UNLINK_A2-1_SO',
      'desc':       'unlink 2 contained <a> elements',
      'command':    'unlink',
      'pad':        'foo[<a>b</a>a<a>r</a>]baz' }
  ],
    
  'Proposed': [
    # bold
    { 'id':         'B_B-1_SW',
      'rte1-id':    'u-bold-0',
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
      'rte1-id':    'u-bold-1',
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
      'rte1-id':    'u-bold-2',
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

    { 'id':         'B_B-P3-1_SO12',
      'desc':       'Unbolding multiple paragraphs in inside bolded content with content-model violation',
      'command':    'bold',
      'pad':        '<b>{<p>foo</p><p>bar</p>}<p>baz</p></b>',
      'expected':   [ '<p>[foo</p><p>bar]</p><p><b>baz</b></p>',
                      '<p>[foo</p><p>bar]</p><b><p>baz</p></b>' ] },

    { 'id':         'B_B-P-I..P-1_SO-I',
      'desc':       'Unbolding italicized content inside bolded content with content-model violation',
      'command':    'bold',
      'pad':        '<b><p>foo[<i>bar</i>]</p><p>baz</p></b>',
      'expected':   [ '<p><b>foo</b><i>[bar]</i></p><p><b>baz</b></p>',
                      '<b><p>foo</p></b><p><i>[bar]</i></p><b><p>baz</p></b>' ] },

    # italic
    { 'id':         'I_I-1_SW',
      'rte1-id':    'u-italic-0',
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
      'rte1-id':    'u-italic-1',
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
      'rte1-id':    'u-italic-2',
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

    { 'id':         'I_I-P3-1_SO2',
      'desc':       'Unitalicize content with content-model violation',
      'command':    'italic',
      'pad':        '<i><p>foo</p>{<p>bar</p>}<p>baz</p></i>',
      'expected':   [ '<p><i>foo</i></p><p>[bar]</p><p><i>baz</i></p>',
                      '<i><p>foo</p></i><p>[bar]</p><i><p>baz</p></i>' ] },

    # underline
    { 'id':         'U_U-1_SW',
      'rte1-id':    'u-underline-0',
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
      'rte1-id':    'u-underline-1',
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

    { 'id':         'U_U-S-1_SO',
      'desc':       'Removing underline from underlined content with striked content',
      'command':    'underline',
      'pad':        '<u>foo[bar<s>baz</s>quoz]</u>',
      'expected':   '<u>foo</u>[bar<s>baz</s>quoz]' },

    { 'id':         'U_U-S-2_SI',
      'desc':       'Removing underline from striked content inside underlined content',
      'command':    'underline',
      'pad':        '<u><s>foo[bar]baz</s>quoz</u>',
      'expected':   '<s><u>foo</u>[bar]<u>baz</u>quoz</s>' },

    { 'id':         'U_U-P3-1_SO',
      'desc':       'Removing underline from underlined content with content-model violation',
      'command':    'underline',
      'pad':        '<u><p>foo</p>{<p>bar</p>}<p>baz</p></u>',
      'expected':   [ '<p><u>foo</u></p><p>[bar]</p><p><u>baz</u></p>',
                      '<u><p>foo</p></u><p>[bar]</p><u><p>baz</p></u>' ] },

    # strikethrough
    { 'id':         'S_S-1_SW',
      'rte1-id':    'u-strikethrough-1',
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
      'rte1-id':    'u-strikethrough-0',
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

    { 'id':         'S_STRIKE-2_SR',
      'desc':       'Selection oblique right; remove <strike> tags',
      'command':    'strikethrough',
      'pad':        'foo<strike>[bar</strike>]baz' },

    { 'id':         'S_DEL-1_SW',
      'rte1-id':    'u-strikethrough-2',
      'desc':       'Selection within tags; remove <del> tags',
      'command':    'strikethrough',
      'pad':        'foo<del>[bar]</del>baz' },

    { 'id':         'S_SPANs:td:lt-1_SW',
      'rte1-id':    'u-strikethrough-3',
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

    { 'id':         'S_S-U-1_SI',
      'desc':       'Removing underline from underlined content inside striked content',
      'command':    'strikethrough',
      'pad':        '<s><u>foo[bar]baz</u>quoz</s>',
      'expected':   '<s><u>foo</u></s><u>[bar]</u><s><u>baz</u>quoz</s>' },

    { 'id':         'S_U-S-1_SI',
      'desc':       'Removing underline from striked content inside underlined content',
      'command':    'strikethrough',
      'pad':        '<u><s>foo[bar]baz</s>quoz</u>',
      'expected':   '<u><s>foo</s>[bar]<s>baz</s>quoz</u>' },

    # subscript
    { 'id':         'SUB_SUB-1_SW',
      'rte1-id':    'u-subscript-0',
      'desc':       'remove subscript',
      'command':    'subscript',
      'pad':        'foo<sub>[bar]</sub>baz' },

    { 'id':         'SUB_SPANs:va:sub-1_SW',
      'rte1-id':    'u-subscript-1',
      'desc':       'remove subscript',
      'command':    'subscript',
      'pad':        'foo<span style="vertical-align: sub">[bar]</span>baz' },

    # superscript
    { 'id':         'SUP_SUP-1_SW',
      'rte1-id':    'u-superscript-0',
      'desc':       'remove superscript',
      'command':    'superscript',
      'pad':        'foo<sup>[bar]</sup>baz' },

    { 'id':         'SUP_SPANs:va:super-1_SW',
      'rte1-id':    'u-superscript-1',
      'desc':       'remove superscript',
      'command':    'superscript',
      'pad':        'foo<span style="vertical-align: super">[bar]</span>baz' },

    # unlink
    { 'id':         'UNLINK_Ahref:url-1_SW',
      'rte1-id':    'u-unlink-0',
      'desc':       'unlink an <a> element with href attribute where all children are selected',
      'command':    'unlink',
      'pad':        'foo<a href="http://www.foo.com">[bar]</a>baz' },

    { 'id':         'UNLINK_A-1_SC',
      'desc':       'unlink an <a> element that contains the collapsed selection',
      'command':    'unlink',
      'pad':        'foo<a>ba^r</a>baz',
      'expected':   'fooba^rbaz' },

    { 'id':         'UNLINK_A-1_SI',
      'desc':       'unlink an <a> element that contains the whole selection',
      'command':    'unlink',
      'pad':        'foo<a>b[a]r</a>baz',
      'expected':   'foob[a]rbaz' },

    { 'id':         'UNLINK_A-2_SL',
      'desc':       'unlink a partially contained <a> element',
      'command':    'unlink',
      'pad':        'foo[ba<a>r]ba</a>z' },

    { 'id':         'UNLINK_A-3_SR',
      'desc':       'unlink a partially contained <a> element',
      'command':    'unlink',
      'pad':        'fo<a>o[ba</a>r]baz' },
    # outdent
    { 'id':         'OUTDENT_BQ-1_SW',
      'rte1-id':    'u-outdent-0',
      'desc':       'outdent (remove) a <blockquote>',
      'command':    'outdent',
      'pad':        'foo<blockquote>[bar]</blockquote>baz',
      'expected':   [ 'foo<p>[bar]</p>baz',
                      'foo<div>[bar]</div>baz' ],
      'accept':     'foo<br>[bar]<br>baz' },

    { 'id':         'OUTDENT_BQ.wibq.s:m:00040.b:n.p:0-1_SW',
      'rte1-id':    'u-outdent-1',
      'desc':       'outdent (remove) a styled <blockquote>',
      'command':    'outdent',
      'pad':        'foo<blockquote class="webkit-indent-blockquote" style="margin: 0 0 0 40px; border: none; padding: 0px">[bar]</blockquote>baz',
      'expected':   [ 'foo<p>[bar]</p>baz',
                      'foo<div>[bar]</div>baz' ],
      'accept':     'foo<br>[bar]<br>baz' },

    { 'id':         'OUTDENT_OL-LI-1_SW',
      'rte1-id':    'u-outdent-3',
      'desc':       'outdent (remove) an ordered list',
      'command':    'outdent',
      'pad':        'foo<ol><li>[bar]</li></ol>baz',
      'expected':   [ 'foo<p>[bar]</p>baz',
                      'foo<div>[bar]</div>baz' ],
      'accept':     'foo<br>[bar]<br>baz' },

    { 'id':         'OUTDENT_UL-LI-1_SW',
      'rte1-id':    'u-outdent-2',
      'desc':       'outdent (remove) an unordered list',
      'command':    'outdent',
      'pad':        'foo<ul><li>[bar]</li></ul>baz',
      'expected':   [ 'foo<p>[bar]</p>baz',
                      'foo<div>[bar]</div>baz' ],
      'accept':     'foo<br>[bar]<br>baz' },

    { 'id':         'OUTDENT_DIV-1_SW',
      'rte1-id':    'u-outdent-4',
      'desc':       'outdent (remove) a styled <div> with margin',
      'command':    'outdent',
      'pad':        'foo<div style="margin-left: 40px;">[bar]</div>baz',
      'expected':   [ 'foo<p>[bar]</p>baz',
                      'foo<div>[bar]</div>baz' ],
      'accept':     'foo<br>[bar]<br>baz' },

    # removeformat
    { 'id':         'REMOVEFORMAT_B-1_SW',
      'rte1-id':    'u-removeformat-0',
      'desc':       'remove a <b> tag using "removeformat"',
      'command':    'removeformat',
      'pad':        'foo<b>[bar]</b>baz' },

    { 'id':         'REMOVEFORMAT_Ahref:url-1_SW',
      'rte1-id':    'u-removeformat-0',
      'desc':       'remove a link using "removeformat"',
      'command':    'removeformat',
      'pad':        'foo<a href="http://www.foo.com">[bar]</a>baz' },

    { 'id':         'REMOVEFORMAT_TABLE-TBODY-TR-TD-1_SW',
      'rte1-id':    'u-removeformat-2',
      'desc':       'remove a table using "removeformat"',
      'command':    'removeformat',
      'pad':        'foo<table><tbody><tr><td>[bar]</td></tr></tbody></table>baz',
      'expected':   [ 'foo<p>[bar]</p>baz',
                      'foo<div>[bar]</div>baz' ],
      'accept':     'foo<br>[bar]<br>baz' },

    # --- Other tests ---

    # unbookmark
    { 'id':         'UNBOOKMARK_An:name-1_SW',
      'rte1-id':    'u-unbookmark-0',
      'desc':       'unlink a bookmark (a named <a> element) where all children are selected',
      'command':    'unbookmark',
      'pad':        'foo<a name="bookmark">[bar]</a>baz' }
  ]
}
