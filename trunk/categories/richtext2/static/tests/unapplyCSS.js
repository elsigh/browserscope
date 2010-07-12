/**
 * @fileoverview 
 * Tests
 *
 * Copyright 2010 Google Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the 'License')
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an 'AS IS' BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * @version 0.1
 * @author rolandsteiner@google.com
 */

var UNAPPLY_TESTS_CSS = {
  id:            'UC',
  caption:       'Unapply Existing Formatting Tests, using styleWithCSS',
  comment:       'Assumptions:' +
                 '<ul>' +
                   '<li>Result selection should continue to wrap the originally selected HTML (if any).</li>' +
                   '<li>Result selection should be inside any newly created element.</li>' +
                   '<li>A selection that started as a text selection should remain a text selection.</li>' +
                   '<li>Elements that are not or only partially selected should retain their name and attributes.</li>' +
                 '</ul>' +
                 '"styleWithCSS" tests:' +
                 '<ul>' +
                   '<li>"styleWithCSS" should have no bearing on the unapply operation.</li>' +
                 '</ul>',
  checkAttrs:    true,
  checkStyle:    true,
  styleWithCSS:  true,
  expected:      'foo[bar]baz',
  testsProposed: {
    // bold
    'B-B-SI-1': {
      desc:      'Selection within tags; remove <b> tags',
      command:   'bold',
      pad:       'foo<b>[bar]</b>baz' },

    'B-B-SO-1': {
      desc:      'Selection outside of tags; remove <b> tags',
      command:   'bold',
      pad:       'foo[<b>bar</b>]baz' },

    'B-B-SM-1': {
      desc:      'Selection mixed; remove <b> tags',
      command:   'bold',
      pad:       'foo[<b>bar]</b>baz' },

    'B-B-SM-2': {
      desc:      'Selection mixed; remove <b> tags',
      command:   'bold',
      pad:       'foo<b>[bar</b>]baz' },

    'B-STRONG-SI-1': {
      desc:      'Selection within tags; remove <strong> tags',
      command:   'bold',
      pad:       'foo<strong>[bar]</strong>baz' },

    'B-STRONG-SO-1': {
      desc:      'Selection outside of tags; remove <strong> tags',
      command:   'bold',
      pad:       'foo[<strong>bar</strong>]baz' },

    'B-STRONG-SM-1': {
      desc:      'Selection mixed; remove <strong> tags',
      command:   'bold',
      pad:       'foo[<strong>bar]</strong>baz' },

    'B-STRONG-SM-2': {
      desc:      'Selection mixed; remove <strong> tags',
      command:   'bold',
      pad:       'foo<strong>[bar</strong>]baz' },

    'B-STYLE-FW-SI-1': {
      desc:      'Selection within tags; remove "font-weight: bold"',
      command:   'bold',
      pad:       'foo<span style="font-weight: bold">[bar]</span>baz' },

    'B-STYLE-FW-SO-1': {
      desc:      'Selection outside of tags; remove "font-weight: bold"',
      command:   'bold',
      pad:       'foo[<span style="font-weight: bold">bar</span>]baz' },

    'B-STYLE-FW-SM-1': {
      desc:      'Selection mixed; remove "font-weight: bold"',
      command:   'bold',
      pad:       'foo[<span style="font-weight: bold">bar]</span>baz' },

    'B-STYLE-FW-SM-2': {
      desc:      'Selection mixed; remove "font-weight: bold"',
      command:   'bold',
      pad:       'foo<span style="font-weight: bold">[bar</span>]baz' },

    // italic
    'I-I-SI-1': {
      desc:      'Selection within tags; remove <i> tags',
      command:   'italic',
      pad:       'foo<i>[bar]</i>baz' },

    'I-I-SO-1': {
      desc:      'Selection outside of tags; remove <i> tags',
      command:   'italic',
      pad:       'foo[<i>bar</i>]baz' },

    'I-I-SM-1': {
      desc:      'Selection mixed; remove <i> tags',
      command:   'italic',
      pad:       'foo[<i>bar]</i>baz' },

    'I-I-SM-2': {
      desc:      'Selection mixed; remove <i> tags',
      command:   'italic',
      pad:       'foo<i>[bar</i>]baz' },

    'I-EM-SI-1': {
      desc:      'Selection within tags; remove <em> tags',
      command:   'italic',
      pad:       'foo<em>[bar]</em>baz' },

    'I-EM-SO-1': {
      desc:      'Selection outside of tags; remove <em> tags',
      command:   'italic',
      pad:       'foo[<em>bar</em>]baz' },

    'I-EM-SM-1': {
      desc:      'Selection mixed; remove <em> tags',
      command:   'italic',
      pad:       'foo[<em>bar]</em>baz' },

    'I-EM-SM-2': {
      desc:      'Selection mixed; remove <em> tags',
      command:   'italic',
      pad:       'foo<em>[bar</em>]baz' },

    'I-STYLE-FS-SI-1': {
      desc:      'Selection within tags; remove "font-style: italic"',
      command:   'italic',
      pad:       'foo<span style="font-style: italic">[bar]</span>baz' },

    'I-STYLE-FS-SO-1': {
      desc:      'Selection outside of tags; Italicize "font-style: italic"',
      command:   'italic',
      pad:       'foo[<span style="font-style: italic">bar</span>]baz' },

    'I-STYLE-FS-SM-1': {
      desc:      'Selection mixed; Italicize "font-style: italic"',
      command:   'italic',
      pad:       'foo[<span style="font-style: italic">bar]</span>baz' },

    'I-STYLE-FS-SM-2': {
      desc:      'Selection mixed; Italicize "font-style: italic"',
      command:   'italic',
      pad:       'foo<span style="font-style: italic">[bar</span>]baz' },

    // underline
    'U-U-SI-1': {
      desc:      'Selection within tags; remove <u> tags',
      command:   'underline',
      pad:       'foo<u>[bar]</u>baz' },

    'U-U-SO-1': {
      desc:      'Selection outside of tags; remove <u> tags',
      command:   'underline',
      pad:       'foo[<u>bar</u>]baz' },

    'U-U-SM-1': {
      desc:      'Selection mixed; remove <u> tags',
      command:   'underline',
      pad:       'foo[<u>bar]</u>baz' },

    'U-U-SM-2': {
      desc:      'Selection mixed; remove <u> tags',
      command:   'underline',
      pad:       'foo<u>[bar</u>]baz' },

    'U-STYLE-TD-SI-1': {
      desc:      'Selection within tags; remove "text-decoration: underline"',
      command:   'underline',
      pad:       'foo<span style="text-decoration: underline">[bar]</span>baz' },

    'U-STYLE-TD-SO-1': {
      desc:      'Selection outside of tags; remove "text-decoration: underline"',
      command:   'underline',
      pad:       'foo[<span style="text-decoration: underline">bar</span>]baz' },

    'U-STYLE-TD-SM-1': {
      desc:      'Selection mixed; remove "text-decoration: underline"',
      command:   'underline',
      pad:       'foo[<span style="text-decoration: underline">bar]</span>baz' },

    'U-STYLE-TD-SM-2': {
      desc:      'Selection mixed; remove "text-decoration: underline"',
      command:   'underline',
      pad:       'foo<span style="text-decoration: underline">[bar</span>]baz' },
      
    // strikethrough
    'S-S-SI-1': {
      desc:      'Selection within tags; remove <s> tags',
      command:   'strikethrough',
      pad:       'foo<s>[bar]</s>baz' },

    'S-S-SO-1': {
      desc:      'Selection outside of tags; remove <s> tags',
      command:   'strikethrough',
      pad:       'foo[<s>bar</s>]baz' },

    'S-S-SM-1': {
      desc:      'Selection mixed; remove <s> tags',
      command:   'strikethrough',
      pad:       'foo[<s>bar]</s>baz' },

    'S-S-SM-2': {
      desc:      'Selection mixed; remove <s> tags',
      command:   'strikethrough',
      pad:       'foo<s>[bar</s>]baz' },

    'S-STRIKE-SI-1': {
      desc:      'Selection within tags; remove <strike> tags',
      command:   'strikethrough',
      pad:       'foo<strike>[bar]</strike>baz' },

    'S-STRIKE-SO-1': {
      desc:      'Selection outside of tags; remove <strike> tags',
      command:   'strikethrough',
      pad:       'foo[<strike>bar</strike>]baz' },

    'S-STRIKE-SM-1': {
      desc:      'Selection mixed; remove <strike> tags',
      command:   'strikethrough',
      pad:       'foo[<strike>bar]</strike>baz' },

    'S-STRIKE-SM-2': {
      desc:      'Selection mixed; remove <strike> tags',
      command:   'strikethrough',
      pad:       'foo<strike>[bar</strike>]baz' },

    'S-STYLE-TD-LT-1': {
      desc:      'Selection within tags; remove "text-decoration:line-through"',
      command:   'strikethrough',
      pad:       'foo<span style="text-decoration:line-through">[bar]</span>baz' },

    'S-STYLE-TD-LT-1': {
      desc:      'Selection outside of tags; Italicize "text-decoration:line-through"',
      command:   'strikethrough',
      pad:       'foo[<span style="text-decoration:line-through">bar</span>]baz' },

    'S-STYLE-TD-LT-1': {
      desc:      'Selection mixed; Italicize "text-decoration:line-through"',
      command:   'strikethrough',
      pad:       'foo[<span style="text-decoration:line-through">bar]</span>baz' },

    'S-STYLE-TD-LT-2': {
      desc:      'Selection mixed; Italicize "text-decoration:line-through"',
      command:   'strikethrough',
      pad:       'foo<span style="text-decoration:line-through">[bar</span>]baz' }
  }
};

