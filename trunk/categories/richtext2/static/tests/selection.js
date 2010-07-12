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

var SELECTION_TESTS = {
  id:            'S',
  caption:       'Selection Tests',
  comment:       'Selection tests',
  checkAttrs:    true,
  checkStyle:    true,
  styleWithCSS:  false,
  testsRFC: {
    // selectall
    'SELALL-TEXT-1': {
      desc:          'select all, text only',
      command:       'selectall',
      pad:           'foo[bar]baz',
      expected:      ['[foobarbaz]',
                      '{foobarbaz}'] },

    'SELALL-I-1': {
      desc:          'select all, with outer tags',
      command:       'selectall',
      pad:           '<i>foo[bar]baz</i>',
      expected:      '{<i>foobarbaz</i>}' },

    // unselect
    'UNSEL-TEXT-1': {
      desc:          'unselect',
      command:       'unselect',
      pad:           'foo[bar]baz',
      checkSel:      true,
      expected:      'foobarbaz' }
  }
};