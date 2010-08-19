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

"""ForwardDelete tests"""

__author__ = 'rolandsteiner@google.com (Roland Steiner)'

# Result selection should be collapsed after the delete operation.
# A selection that started as a text selection should remain a text selection.
# Elements that are not or only partially selected should remain, and retain their name and attributes.

FORWARDDELETE_TESTS = {
  'id':          'FD',
  'caption':       'Forward-Delete Tests',
  'command':       'forwardDelete',
  'checkAttrs':    False,
  'checkStyle':    False,

  'Proposed': [
    # backward delete
    { 'id':          'CHAR-1',
      'desc':        'Delete 1 character',
      'pad':         'foo^barbaz',
      'expected':    'foo^arbaz' },

    { 'id':          'CHAR-2',
      'desc':        'Delete 1 pre-composed character o with diaeresis',
      'pad':         'fo^&#xF6;barbaz',
      'expected':    'fo^barbaz' },

    { 'id':          'CHAR-3',
      'desc':        'Delete 1 character with combining diaeresis above',
      'pad':         'fo^o&#x0308;barbaz',
      'expected':    'fo^barbaz' },

    { 'id':          'CHAR-4',
      'desc':        'Delete 1 character with combining diaeresis below',
      'pad':         'fo^o&#x0324;barbaz',
      'expected':    'fo^barbaz' },

    { 'id':          'CHAR-5',
      'desc':        'Delete 1 character with combining diaeresis above and below',
      'pad':         'fo^o&#x0308;&#x0324;barbaz',
      'expected':    'fo^barbaz' },

    { 'id':          'CHAR-6',
      'desc':        'Delete 1 character with enclosing square',
      'pad':         'fo^o&#x20DE;barbaz',
      'expected':    'fo^barbaz' },

    { 'id':          'CHAR-7',
      'desc':        'Delete 1 character with combining long solidus overlay',
      'pad':         'fo^o&#x0338;barbaz',
      'expected':    'fo^barbaz' },

    { 'id':          'CHAR-TBL-1',
      'desc':        'Delete from position immediately before table (should have no effect)',
      'pad':         'foo^<table><tbody><tr><td>bar</td></tr></tbody></table>baz',
      'expected':    'foo^<table><tbody><tr><td>bar</td></tr></tbody></table>baz' },

    { 'id':          'CHAR-TBL-2',
      'desc':        'Delete from end of last cell (should have no effect)',
      'pad':         'foo<table><tbody><tr><td>bar^</td></tr></tbody></table>baz',
      'expected':    'foo<table><tbody><tr><td>bar^</td></tr></tbody></table>baz' },

    { 'id':          'CHAR-TBL-3',
      'desc':        'Delete from end of inner cell (should have no effect)',
      'pad':         'foo<table><tbody><tr><td>bar^</td><td>baz</td></tr></tbody></table>quoz',
      'expected':    'foo<table><tbody><tr><td>bar^</td><td>baz</td></tr></tbody></table>quoz' },

    { 'id':          'TEXT-1',
      'desc':        'Delete text selection',
      'pad':         'foo[bar]baz',
      'expected':    'foo^baz' },
      
    { 'id':          'SPAN-1',
      'desc':        'Delete at end of span',
      'pad':         'foo<b>bar^</b>baz',
      'expected':    'foo<b>bar</b>az' },

    { 'id':          'SPAN-2',
      'desc':        'Delete from position before span',
      'pad':         'foo^<b>bar</b>baz',
      'expected':    'foo<b>ar</b>baz' },

    { 'id':          'SPAN-3',
      'desc':        'Delete oblique selection that starts before span',
      'pad':         'foo[bar<b>baz]quoz</b>quuz',
      'expected':    'foo<b>quoz</b>quuz' },

    { 'id':          'SPAN-4',
      'desc':        'Delete oblique selection that ends after span',
      'pad':         'foo<b>bar[baz</b>quoz]quuz',
      'expected':    'foo<b>bar</b>quuz' },

    { 'id':          'SPAN-5',
      'desc':        'Delete selection that wraps the whole span content',
      'pad':         'foo<b>[bar]</b>baz',
      'expected':    'foo^baz' },  # Note: for 'delete', all browsers tested remove <b> tag as well, so let's go with that here as well.

    { 'id':          'SPAN-6',
      'desc':        'Delete selection that wraps the whole span',
      'pad':         'foo[<b>bar</b>]baz',
      'expected':    'foo^baz' },

    { 'id':          'SPAN-7',
      'desc':        'Delete oblique selection that starts and ends in different spans',
      'pad':         'foo<b>bar[baz</b><i>qoz]quuz</i>quuuz',
      'expected':    'foo<b>bar</b><i>quuz</i>quuuz' },

    { 'id':          'GEN-1',
      'desc':        'Delete at end of span with generated content',
      'pad':         'foo<gen>bar^</gen>baz',
      'expected':    'foo<gen>bar</gen>az' },

    { 'id':          'DEL-GEN-2',
      'desc':        'Delete from position before span with generated content',
      'pad':         'foo^<gen>bar</gen>baz',
      'expected':    'foo<gen>ar</gen>baz' },

    { 'id':          'P-1',
      'desc':        'Delete at end of paragraph - should merge with next',
      'pad':         '<p>foo^</p><p>bar</p>',
      'expected':    '<p>foo^bar</p>' },

    { 'id':          'LI-1',
      'desc':        'Delete fully wrapped list item',
      'pad':         'foo<ol>{<li>bar</li>}<li>baz</li></ol>qoz', 
      'expected':    'foo<ol><li>baz</li></ol>qoz' },

    { 'id':          'LI-2',
      'desc':        'Delete oblique range between list items within same list',
      'pad':         'foo<ol><li>ba[r</li><li>b]az</li></ol>qoz',
      'expected':    'foo<ol><li>ba^az</li></ol>qoz' },

    { 'id':           'LI-3',
      'desc':        'Delete contents of last list item (list should remain)',
      'pad':         'foo<ol><li>[foo]</li></ol>qoz',
      'expected':    'foo<ol><li></li></ol>qoz' },

    { 'id':          'LI-4',
      'desc':        'Delete last list item of list (should remove entire list)',
      'pad':         'foo<ol>{<li>foo</li>}</ol>qoz',
      'expected':    'foo^qoz' },

    { 'id':          'CHILD-0',
      'desc':        'Delete selection that starts and ends within nodes that don\'t have children',
      'pad':         'foo<hr {>bar<br }>baz',
      'expected':    'foo<hr>|<br>baz' }
  ]
};


