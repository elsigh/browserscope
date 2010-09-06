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

"""Delete tests"""

__author__ = 'rolandsteiner@google.com (Roland Steiner)'

# Result selection should be collapsed after the delete operation.
# A selection that started as a text selection should remain a text selection.
# Elements that are not or only partially selected should remain, and retain their name and attributes.

DELETE_TESTS = {
  'id':          'D',
  'caption':       'Delete Tests',
  'command':       'delete',
  'checkAttrs':    True,
  'checkStyle':    False,

  'Proposed': [
    { 'id':          'CHAR-1',
      'desc':        'Delete 1 character',
      'pad':         'foo^barbaz',
      'expected':    'fo^barbaz' },

    { 'id':          'CHAR-2',
      'desc':        'Delete 1 pre-composed character o with diaeresis',
      'pad':         'fo&#xF6;^barbaz',
      'expected':    'fo^barbaz' },

    { 'id':          'CHAR-3',
      'desc':        'Delete 1 character with combining diaeresis above',
      'pad':         'foo&#x0308;^barbaz',
      'expected':    'fo^barbaz' },

    { 'id':          'CHAR-4',
      'desc':        'Delete 1 character with combining diaeresis below',
      'pad':         'foo&#x0324;^barbaz',
      'expected':    'fo^barbaz' },

    { 'id':          'CHAR-5',
      'desc':        'Delete 1 character with combining diaeresis above and below',
      'pad':         'foo&#x0308;&#x0324;^barbaz',
      'expected':    'fo^barbaz' },

    { 'id':          'CHAR-6',
      'desc':        'Delete 1 character with enclosing square',
      'pad':         'foo&#x20DE;^barbaz',
      'expected':    'fo^barbaz' },

    { 'id':          'CHAR-7',
      'desc':        'Delete 1 character with combining long solidus overlay',
      'pad':         'foo&#x0338;^barbaz',
      'expected':    'fo^barbaz' },

    { 'id':          'CHAR-TBL-1',
      'desc':        'Delete from position immediately after table (should have no effect)',
      'pad':         'foo<table><tbody><tr><td>bar</td></tr></tbody></table>^baz',
      'expected':    'foo<table><tbody><tr><td>bar</td></tr></tbody></table>^baz' },

    { 'id':          'CHAR-TBL-2',
      'desc':        'Delete from start of first cell (should have no effect)',
      'pad':         'foo<table><tbody><tr><td>^bar</td></tr></tbody></table>baz',
      'expected':    'foo<table><tbody><tr><td>^bar</td></tr></tbody></table>baz' },

    { 'id':          'CHAR-TBL-3',
      'desc':        'Delete from start of inner cell (should have no effect)',
      'pad':         'foo<table><tbody><tr><td>bar</td><td>^baz</td></tr></tbody></table>quoz',
      'expected':    'foo<table><tbody><tr><td>bar</td><td>^baz</td></tr></tbody></table>quoz' },

    { 'id':          'TEXT-1',
      'desc':        'Delete text selection',
      'pad':         'foo[bar]baz',
      'expected':    'foo^baz' },

    { 'id':          'SPAN-1',
      'desc':        'Delete at start of span',
      'pad':         'foo<b>^bar</b>baz',
      'expected':    'fo^<b>bar</b>baz' },

    { 'id':          'SPAN-2',
      'desc':        'Delete from position after span',
      'pad':         'foo<b>bar</b>^baz',
      'expected':    'foo<b>ba^</b>baz' },

    { 'id':          'SPAN-3',
      'desc':        'Delete oblique selection that starts before span',
      'pad':         'foo[bar<b>baz]quoz</b>quuz',
      'expected':    'foo^<b>quoz</b>quuz' },

    { 'id':          'SPAN-4',
      'desc':        'Delete oblique selection that ends after span',
      'pad':         'foo<b>bar[baz</b>quoz]quuz',
      'expected':    'foo<b>bar^</b>quuz' },

    { 'id':          'SPAN-5',
      'desc':        'Delete selection that wraps the whole span content',
      'pad':         'foo<b>[bar]</b>baz',
      'expected':    'foo^baz' },  # Note: all browsers tested remove <b> tag as well, so let's go with that.

    { 'id':          'SPAN-6',
      'desc':        'Delete selection that wraps the whole span',
      'pad':         'foo[<b>bar</b>]baz',
      'expected':    'foo^baz' },

    { 'id':          'SPAN-7',
      'desc':        'Delete oblique selection that starts and ends in different spans',
      'pad':         'foo<b>bar[baz</b><i>qoz]quuz</i>quuuz',
      'expected':    'foo<b>bar^</b><i>quuz</i>quuuz' },

    { 'id':          'GEN-1',
      'desc':        'Delete at start of span with generated content',
      'pad':         'foo<gen>^bar</gen>baz',
      'expected':    'fo^<gen>bar</gen>baz' },

    { 'id':          'GEN-2',
      'desc':        'Delete from position after span with generated content',
      'pad':         'foo<gen>bar</gen>^baz',
      'expected':    'foo<gen>ba^</gen>baz' },

    { 'id':          'P-1',
      'desc':        'Delete at start of paragraph - should merge with previous',
      'pad':         '<p>foo</p><p>^bar</p>',
      'expected':    '<p>foo^bar</p>' },

    { 'id':          'LI-1',
      'desc':        'Delete fully wrapped list item',
      'pad':         'foo<ol>{<li>bar</li>}<li>baz</li></ol>qoz', 
      'expected':    ['foo<ol>|<li>baz</li></ol>qoz',
                      'foo<ol><li>^baz</li></ol>qoz'] },

    { 'id':          'LI-2',
      'desc':        'Delete oblique range between list items within same list',
      'pad':         'foo<ol><li>ba[r</li><li>b]az</li></ol>qoz',
      'expected':    'foo<ol><li>ba^az</li></ol>qoz' },

    { 'id':          'LI-3',
      'desc':        'Delete contents of last list item (list should remain)',
      'pad':         'foo<ol><li>[foo]</li></ol>qoz',
      'expected':    ['foo<ol><li>|</li></ol>qoz',
                      'foo<ol><li>^</li></ol>qoz'] },

    { 'id':          'LI-4',
      'desc':        'Delete last list item of list (should remove entire list)',
      'pad':         'foo<ol>{<li>foo</li>}</ol>qoz',
      'expected':    'foo^qoz' },

    { 'id':          'CHILD-0',
      'desc':        'Delete selection that starts and ends within nodes that don\'t have children',
      'pad':         'foo<hr {>bar<br }>baz',
      'expected':    'foo<hr>|<br>baz' },

    { 'id':          'TR-1',
      'desc':        'Delete first table row',
      'pad':         '<table><tbody>{<tr><td>A</td></tr>}<tr><td>B</td></tr><tr><td>C</td></tr></tbody></table>',
      'expected':    ['<table><tbody>|<tr><td>B</td></tr><tr><td>C</td></tr></tbody></table>',
                      '<table><tbody><tr><td>^B</td></tr><tr><td>C</td></tr></tbody></table>'] },

    { 'id':          'TR-2',
      'desc':        'Delete middle table row',
      'pad':         '<table><tbody><tr><td>A</td></tr>{<tr><td>B</td></tr>}<tr><td>C</td></tr></tbody></table>',
      'expected':    ['<table><tbody><tr><td>A</td></tr>|<tr><td>C</td></tr></tbody></table>',
                      '<table><tbody><tr><td>A</td></tr><tr><td>^C</td></tr></tbody></table>'] },

    { 'id':          'TR-3',
      'desc':        'Delete last table row',
      'pad':         '<table><tbody><tr><td>A</td></tr><tr><td>B</td></tr>{<tr><td>C</td></tr>}</tbody></table>',
      'expected':    ['<table><tbody><tr><td>A</td></tr><tr><td>B</td></tr>|</tbody></table>',
                      '<table><tbody><tr><td>A</td></tr><tr><td>B^</td></tr></tbody></table>'] },

    { 'id':          'TR-ROWSPAN2-1',
      'desc':        'Delete first table row where a cell has rowspan 2',
      'pad':         '<table><tbody>{<tr><td>A</td><td rowspan=2>R</td></tr>}<tr><td>B</td></tr></tbody></table>',
      'expected':    ['<table><tbody>|<tr><td>B</td><td>R</td></tr></tbody></table>',
                      '<table><tbody><tr><td>^B</td><td>R</td></tr></tbody></table>'] },

    { 'id':          'TR-ROWSPAN2-2',
      'desc':        'Delete second table row where a cell has rowspan 2',
      'pad':         '<table><tbody><tr><td>A</td><td rowspan=2>R</td></tr>{<tr><td>B</td></tr>}</tbody></table>',
      'expected':    ['<table><tbody><tr><td>A</td><td>R</td></tr>|</tbody></table>',
                      '<table><tbody><tr><td>A</td><td>R^</td></tr></tbody></table>'] },

    { 'id':          'TR-ROWSPAN3-1',
      'desc':        'Delete first table row where a cell has rowspan 3',
      'pad':         '<table><tbody>{<tr><td>A</td><td rowspan=3>R</td></tr>}<tr><td>B</td></tr><tr><td>C</td></tr></tbody></table>',
      'expected':    ['<table><tbody>|<tr><td>A</td><td rowspan="2">R</td></tr><tr><td>C</td></tr></tbody></table>',
                      '<table><tbody><tr><td>^A</td><td rowspan="2">R</td></tr><tr><td>C</td></tr></tbody></table>'] },

    { 'id':          'TR-ROWSPAN3-2',
      'desc':        'Delete middle table row where a cell has rowspan 3',
      'pad':         '<table><tbody><tr><td>A</td><td rowspan=3>R</td></tr>{<tr><td>B</td></tr>}<tr><td>C</td></tr></tbody></table>',
      'expected':    ['<table><tbody><tr><td>B</td><td rowspan="2">R</td></tr>|<tr><td>C</td></tr></tbody></table>',
                      '<table><tbody><tr><td>B</td><td rowspan="2">R</td></tr><tr><td>^C</td></tr></tbody></table>'] },

    { 'id':          'TR-ROWSPAN3-3',
      'desc':        'Delete last table row where a cell has rowspan 3',
      'pad':         '<table><tbody><tr><td>A</td><td rowspan=3>R</td></tr><tr><td>B</td></tr>{<tr><td>C</td></tr>}</tbody></table>',
      'expected':    ['<table><tbody><tr><td>A</td><td rowspan="2">R</td></tr><tr><td>B</td></tr>|</tbody></table>',
                      '<table><tbody><tr><td>A</td><td rowspan="2">R</td></tr><tr><td>B^</td></tr></tbody></table>'] }
  ]
};


