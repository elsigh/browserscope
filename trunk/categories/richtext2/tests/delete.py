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

DELETE_TESTS = {
  'id':          'D',
  'caption':       'Delete Tests',
  'command':       'delete',
  'checkAttrs':    True,
  'checkStyle':    False,

  'Proposed': [
    # single characters
    { 'id':          'CHAR-1_SC',
      'desc':        'Delete 1 character',
      'pad':         'foo^barbaz',
      'expected':    'fo^barbaz' },

    { 'id':          'CHAR-2_SC',
      'desc':        'Delete 1 pre-composed character o with diaeresis',
      'pad':         'fo&#xF6;^barbaz',
      'expected':    'fo^barbaz' },

    { 'id':          'CHAR-3_SC',
      'desc':        'Delete 1 character with combining diaeresis above',
      'pad':         'foo&#x0308;^barbaz',
      'expected':    'fo^barbaz' },

    { 'id':          'CHAR-4_SC',
      'desc':        'Delete 1 character with combining diaeresis below',
      'pad':         'foo&#x0324;^barbaz',
      'expected':    'fo^barbaz' },

    { 'id':          'CHAR-5_SC',
      'desc':        'Delete 1 character with combining diaeresis above and below',
      'pad':         'foo&#x0308;&#x0324;^barbaz',
      'expected':    'fo^barbaz' },

    { 'id':          'CHAR-5_SI-1',
      'desc':        'Delete 1 character with combining diaeresis above and below, selection on diaeresis above',
      'pad':         'foo[&#x0308;]&#x0324;barbaz',
      'expected':    'fo^barbaz' },

    { 'id':          'CHAR-5_SI-2',
      'desc':        'Delete 1 character with combining diaeresis above and below, selection on diaeresis below',
      'pad':         'foo&#x0308;[&#x0324;]barbaz',
      'expected':    'fo^barbaz' },

    { 'id':          'CHAR-5_SR',
      'desc':        'Delete 1 character with combining diaeresis above and below, selection oblique on diaeresis and following text',
      'pad':         'foo&#x0308;[&#x0324;bar]baz',
      'expected':    'fo^baz' },

    { 'id':          'CHAR-6_SC',
      'desc':        'Delete 1 character with enclosing square',
      'pad':         'foo&#x20DE;^barbaz',
      'expected':    'fo^barbaz' },

    { 'id':          'CHAR-7_SC',
      'desc':        'Delete 1 character with combining long solidus overlay',
      'pad':         'foo&#x0338;^barbaz',
      'expected':    'fo^barbaz' },

    # text selection
    { 'id':          'TEXT-1_SI',
      'desc':        'Delete text selection',
      'pad':         'foo[bar]baz',
      'expected':    'foo^baz' },

    { 'id':          'B-1_SS',
      'desc':        'Delete at start of span',
      'pad':         'foo<b>^bar</b>baz',
      'expected':    'fo^<b>bar</b>baz' },

    { 'id':          'B-1_SA',
      'desc':        'Delete from position after span',
      'pad':         'foo<b>bar</b>^baz',
      'expected':    'foo<b>ba^</b>baz' },

    { 'id':          'B-1_SW',
      'desc':        'Delete selection that wraps the whole span content',
      'pad':         'foo<b>[bar]</b>baz',
      'expected':    'foo^baz' },  # Note: all browsers tested remove <b> tag as well, so let's go with that.

    { 'id':          'B-1_SO',
      'desc':        'Delete selection that wraps the whole span',
      'pad':         'foo[<b>bar</b>]baz',
      'expected':    'foo^baz' },

    { 'id':          'B-1_SL',
      'desc':        'Delete oblique selection that starts before span',
      'pad':         'foo[bar<b>baz]quoz</b>quuz',
      'expected':    'foo^<b>quoz</b>quuz' },

    { 'id':          'B-1_SR',
      'desc':        'Delete oblique selection that ends after span',
      'pad':         'foo<b>bar[baz</b>quoz]quuz',
      'expected':    'foo<b>bar^</b>quuz' },

    { 'id':          'B.I-1_SM',
      'desc':        'Delete oblique selection that starts and ends in different spans',
      'pad':         'foo<b>bar[baz</b><i>qoz]quuz</i>quuuz',
      'expected':    'foo<b>bar^</b><i>quuz</i>quuuz' },

    { 'id':          'GEN-1_SS',
      'desc':        'Delete at start of span with generated content',
      'pad':         'foo<gen>^bar</gen>baz',
      'expected':    'fo^<gen>bar</gen>baz' },

    { 'id':          'GEN-1_SA',
      'desc':        'Delete from position after span with generated content',
      'pad':         'foo<gen>bar</gen>^baz',
      'expected':    'foo<gen>ba^</gen>baz' },

    # paragraphs
    { 'id':          'P2-1_SS2',
      'desc':        'Delete from collapsed selection at start of paragraph - should merge with previous',
      'pad':         '<p>foobar</p><p>^bazqoz</p>',
      'expected':    '<p>foobar^bazqoz</p>' },

    { 'id':          'P2-1_SI2',
      'desc':        'Delete non-collapsed selection at start of paragraph - should not merge with previous',
      'pad':         '<p>foobar</p><p>[baz]qoz</p>',
      'expected':    '<p>foobar</p><p>^qoz</p>' },

    { 'id':          'P2-1_SM',
      'desc':        'Delete non-collapsed selection spanning 2 paragraphs - should merge them',
      'pad':         '<p>foo[bar</p><p>baz]qoz</p>',
      'expected':    '<p>foo^qoz</p>' },

    # lists
    { 'id':          'OL-LI2-1_SO1',
      'desc':        'Delete fully wrapped list item',
      'pad':         'foo<ol>{<li>bar</li>}<li>baz</li></ol>qoz', 
      'expected':    ['foo<ol>|<li>baz</li></ol>qoz',
                      'foo<ol><li>^baz</li></ol>qoz'] },

    { 'id':          'OL-LI2-1_SM',
      'desc':        'Delete oblique range between list items within same list',
      'pad':         'foo<ol><li>ba[r</li><li>b]az</li></ol>qoz',
      'expected':    'foo<ol><li>ba^az</li></ol>qoz' },

    { 'id':          'OL-LI-1_SW',
      'desc':        'Delete contents of last list item (list should remain)',
      'pad':         'foo<ol><li>[foo]</li></ol>qoz',
      'expected':    ['foo<ol><li>|</li></ol>qoz',
                      'foo<ol><li>^</li></ol>qoz'] },

    { 'id':          'OL-LI-1_SO',
      'desc':        'Delete last list item of list (should remove entire list)',
      'pad':         'foo<ol>{<li>foo</li>}</ol>qoz',
      'expected':    'foo^qoz' },

    # strange selections
    { 'id':          'HR.BR-1_SM',
      'desc':        'Delete selection that starts and ends within nodes that don\'t have children',
      'pad':         'foo<hr {>bar<br }>baz',
      'expected':    'foo<hr>|<br>baz' },

    # tables
    { 'id':          'TABLE-1_SA',
      'desc':        'Delete from position immediately after table (should have no effect)',
      'pad':         'foo<table><tbody><tr><td>bar</td></tr></tbody></table>^baz',
      'expected':    'foo<table><tbody><tr><td>bar</td></tr></tbody></table>^baz' },

    # table cells
    { 'id':          'TD-1_SS',
      'desc':        'Delete from start of first cell (should have no effect)',
      'pad':         'foo<table><tbody><tr><td>^bar</td></tr></tbody></table>baz',
      'expected':    'foo<table><tbody><tr><td>^bar</td></tr></tbody></table>baz' },

    { 'id':          'TD2-1_SS2',
      'desc':        'Delete from start of inner cell (should have no effect)',
      'pad':         'foo<table><tbody><tr><td>bar</td><td>^baz</td></tr></tbody></table>quoz',
      'expected':    'foo<table><tbody><tr><td>bar</td><td>^baz</td></tr></tbody></table>quoz' },

    { 'id':          'TD2-1_SM',
      'desc':        'Delete with selection spanning 2 cells',
      'pad':         'foo<table><tbody><tr><td>ba[r</td><td>b]az</td></tr></tbody></table>quoz',
      'expected':    'foo<table><tbody><tr><td>ba^</td><td>az</td></tr></tbody></table>quoz' },

    # table rows
    { 'id':          'TR3-1_SO1',
      'desc':        'Delete first table row',
      'pad':         '<table><tbody>{<tr><td>A</td></tr>}<tr><td>B</td></tr><tr><td>C</td></tr></tbody></table>',
      'expected':    ['<table><tbody>|<tr><td>B</td></tr><tr><td>C</td></tr></tbody></table>',
                      '<table><tbody><tr><td>^B</td></tr><tr><td>C</td></tr></tbody></table>'] },

    { 'id':          'TR3-1_SO2',
      'desc':        'Delete middle table row',
      'pad':         '<table><tbody><tr><td>A</td></tr>{<tr><td>B</td></tr>}<tr><td>C</td></tr></tbody></table>',
      'expected':    ['<table><tbody><tr><td>A</td></tr>|<tr><td>C</td></tr></tbody></table>',
                      '<table><tbody><tr><td>A</td></tr><tr><td>^C</td></tr></tbody></table>'] },

    { 'id':          'TR3-1_SO3',
      'desc':        'Delete last table row',
      'pad':         '<table><tbody><tr><td>A</td></tr><tr><td>B</td></tr>{<tr><td>C</td></tr>}</tbody></table>',
      'expected':    ['<table><tbody><tr><td>A</td></tr><tr><td>B</td></tr>|</tbody></table>',
                      '<table><tbody><tr><td>A</td></tr><tr><td>B^</td></tr></tbody></table>'] },

    { 'id':          'TR2rs:2-1_SO1',
      'desc':        'Delete first table row where a cell has rowspan 2',
      'pad':         '<table><tbody>{<tr><td>A</td><td rowspan=2>R</td></tr>}<tr><td>B</td></tr></tbody></table>',
      'expected':    ['<table><tbody>|<tr><td>B</td><td>R</td></tr></tbody></table>',
                      '<table><tbody><tr><td>^B</td><td>R</td></tr></tbody></table>'] },

    { 'id':          'TR2rs:2-1_SO2',
      'desc':        'Delete second table row where a cell has rowspan 2',
      'pad':         '<table><tbody><tr><td>A</td><td rowspan=2>R</td></tr>{<tr><td>B</td></tr>}</tbody></table>',
      'expected':    ['<table><tbody><tr><td>A</td><td>R</td></tr>|</tbody></table>',
                      '<table><tbody><tr><td>A</td><td>R^</td></tr></tbody></table>'] },

    { 'id':          'TR3rs:3-1_SO1',
      'desc':        'Delete first table row where a cell has rowspan 3',
      'pad':         '<table><tbody>{<tr><td>A</td><td rowspan=3>R</td></tr>}<tr><td>B</td></tr><tr><td>C</td></tr></tbody></table>',
      'expected':    ['<table><tbody>|<tr><td>A</td><td rowspan="2">R</td></tr><tr><td>C</td></tr></tbody></table>',
                      '<table><tbody><tr><td>^A</td><td rowspan="2">R</td></tr><tr><td>C</td></tr></tbody></table>'] },

    { 'id':          'TR3rs:3-1_SO2',
      'desc':        'Delete middle table row where a cell has rowspan 3',
      'pad':         '<table><tbody><tr><td>A</td><td rowspan=3>R</td></tr>{<tr><td>B</td></tr>}<tr><td>C</td></tr></tbody></table>',
      'expected':    ['<table><tbody><tr><td>B</td><td rowspan="2">R</td></tr>|<tr><td>C</td></tr></tbody></table>',
                      '<table><tbody><tr><td>B</td><td rowspan="2">R</td></tr><tr><td>^C</td></tr></tbody></table>'] },

    { 'id':          'TR3rs:3-1_SO3',
      'desc':        'Delete last table row where a cell has rowspan 3',
      'pad':         '<table><tbody><tr><td>A</td><td rowspan=3>R</td></tr><tr><td>B</td></tr>{<tr><td>C</td></tr>}</tbody></table>',
      'expected':    ['<table><tbody><tr><td>A</td><td rowspan="2">R</td></tr><tr><td>B</td></tr>|</tbody></table>',
                      '<table><tbody><tr><td>A</td><td rowspan="2">R</td></tr><tr><td>B^</td></tr></tbody></table>'] }
  ]
}


