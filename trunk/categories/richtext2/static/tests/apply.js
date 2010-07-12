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

var APPLY_TESTS = {
  id:            'A',
  caption:       'Apply Formatting Tests',
  comment:       'Assumptions:' +
                 '<ul>' +
                   '<li>Result selection should continue to wrap the originally selected HTML (if any).</li>' +
                   '<li>Result selection should be inside any newly created element.</li>' +
                   '<li>A selection that started as a text selection should remain a text selection.</li>' +
                   '<li>Elements that are not or only partially selected should retain their name and attributes.</li>' +
                 '</ul>' +
                 'Non-"styleWithCSS" tests:' +
                 '<ul>' +
                   '<li>Newly created elements should not create a "style" attribute unless necessary.</li>' +
                 '</ul>',
  checkAttrs:    true,
  checkStyle:    true,
  styleWithCSS:  false,
  testsProposed: {
    // bold
    'B-TEXT-1': {
      desc:          'Bold selection',
      command:       'bold',
      pad:           'foo[bar]baz',
      expected:      ['foo<b>[bar]</b>baz',
                      'foo<strong>[bar]</strong>baz'] },

    'B-TEXT-1-SR': {
      desc:          'Bold reversed selection',
      command:       'bold',
      pad:           'foo]bar[baz',
      expected:      ['foo<b>[bar]</b>baz',
                      'foo<strong>[bar]</strong>baz'] },

    'B-MIXED-1': {
      desc:          'Bold selection, partially including italic',
      command:       'bold',
      pad:           'foo[bar<i>baz]qoz</i>quz',
      expected:      ['foo<b>[bar</b><i><b>baz]</b>qoz</i>quz',
                      'foo<b>[bar<i>baz]</i></b><i>qoz</i>quz',
                      'foo<strong>[bar</strong><i><strong>baz]</strong>qoz</i>quz',
                      'foo<strong>[bar<i>baz]</i></strong><i>qoz</i>quz'] },

    // italic
    'I-TEXT-1': {
      desc:          'Italicize selection',
      command:       'italic',
      pad:           'foo[bar]baz',
      expected:      ['foo<i>[bar]</i>baz',
                      'foo<em>[bar]</em>baz'] },

    // underline
    'U-TEXT-1': {
      desc:          'Underline selection',
      command:       'underline',
      pad:           'foo[bar]baz',
      expected:      'foo<u>[bar]</u>baz' },
      
    // strikethrough
    'S-TEXT-1': {
      desc:          'Strike-through selection',
      command:       'strikethrough',
      pad:           'foo[bar]baz',
      expected:      ['foo<s>[bar]</s>baz',
                      'foo<strike>[bar]</strike>baz'] },
      
    // subscript
    'SUB-TEXT-1': {
      desc:          'Change selection to subscript',
      command:       'subscript',
      pad:           'foo[bar]baz',
      expected:      'foo<sub>[bar]</sub>baz' },

    // superscript
    'SUP-TEXT-1': {
      desc:          'Change selection to superscript',
      command:       'superscript',
      pad:           'foo[bar]baz',
      expected:      'foo<sup>[bar]</sup>baz' },

    // backcolor (note, no non-CSS variant available)
    'BC-TEXT-1': {
      desc:          'Change background color (no non-CSS variant available)',
      command:       'backcolor',
      value:         'blue',
      pad:           'foo[bar]baz',
      expected:      ['foo<span style="background-color: blue">[bar]</span>baz',
                      'foo<font style="background-color: blue">[bar]</font>baz'] },

    // fontcolor
    'FC-TEXT-1': {
      desc:          'Change the text color',
      command:       'fontcolor',
      value:         'blue',
      pad:           'foo[bar]baz',
      expected:      'foo<font color="blue">[bar]</font>baz' },

    // fontname
    'FN-TEXT-1': {
      desc:          'Change the font name',
      command:       'fontname',
      value:         'arial',
      pad:           'foo[bar]baz',
      expected:      'foo<font face="arial">[bar]</font>baz' },

    // fontsize
    'FS-TEXT-2': {
      desc:          'Change the font size to "2"',
      command:       'fontsize',
      value:         '2',
      pad:           'foo[bar]baz',
      expected:      'foo<font size="2">[bar]</font>baz' },

    'FS-TEXT-18px': {
      desc:          'Change the font size to "18px"',
      command:       'fontsize',
      value:         '18px',
      pad:           'foo[bar]baz',
      expected:      'foo<font size="18px">[bar]</font>baz' },

    'FS-TEXT-large': {
      desc:          'Change the font size to "large"',
      command:       'fontsize',
      value:         'large',
      pad:           'foo[bar]baz',
      expected:      'foo<font size="large">[bar]</font>baz' },

    // indent
    'IND-TEXT-1': {
      desc:          'Indent the text',
      command:       'indent',
      pad:           'foo^bar',
      checkAttrs:    false,  // FIXME: determine generic way to check indent.
      expected:      '<blockquote>foo^bar</blockquote>' },

    // outdent
    'OUTD-TEXT-1': {
      desc:          'Outdent the text',
      command:       'outdent',
      pad:           '<blockquote>foo^bar</blockquote>',
      expected:      ['foo^bar',
                      '<p>foo^bar</p>',
                      '<div>foo^bar</div>'] },

    // justifycenter
    'JC-TEXT-1': {
      desc:          'justify the text centrally',
      command:       'justifycenter',
      pad:           'foo^bar',
      expected:      ['<center>foo^bar</center>',
                      '<p align="center">foo^bar</p>',
                      '<p align="middle">foo^bar</p>',
                      '<div align="center">foo^bar</div>',
                      '<div align="middle">foo^bar</div>'] },

    // justifyfull
    'JF-TEXT-1': {
      desc:          'justify the text fully',
      command:       'justifyfull',
      pad:           'foo^bar',
      expected:      ['<p align="justify">foo^bar</p>',
                      '<div align="justify">foo^bar</div>'] },

    // justifyleft
    'JL-TEXT-1': {
      desc:          'justify the text left',
      command:       'justifyleft',
      pad:           'foo^bar',
      expected:      ['<p align="left">foo^bar</p>',
                      '<div align="left">foo^bar</div>'] },

    // justifyright
    'JR-TEXT-1': {
      desc:          'justify the text right',
      command:       'justifyright',
      pad:           'foo^bar',
      expected:      ['<p align="right">foo^bar</p>',
                      '<div align="right">foo^bar</div>'] },

    // createlink
    'CL-1': {
      desc:          'create a link around the selection',
      command:       'createlink',
      value:         '#C-CL-1',
      pad:           'foo[bar]baz',
      expected:      'foo<a href="#C-CL-1">bar</a>baz' }
  }
};
