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

var CHANGE_TESTS = {
  id:            'C',
  caption:       'Change Existing Format to Different Format Tests',
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
    // font name
    'FN-TEXT-1': {
      desc:          'Change existing font name to new font name, not using CSS styling',
      command:       'fontname',
      value:         'courier',
      styleWithCSS:  false,
      pad:           '<font face="arial">[foo bar baz]</font>',
      expected:      '<font face="courier">[foo bar baz]</font>' },

    // font size
    'FS-TEXT-1': {
      desc:          'Change existing font size to new size, not using CSS styling',
      command:       'fontsize',
      value:         '1',
      styleWithCSS:  false,
      pad:           '<font size="4">[foo bar baz]</font>',
      expected:      '<font size="1">[foo bar baz]</font>' }
  }
};
