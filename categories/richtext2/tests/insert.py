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

"""Insert tests"""

__author__ = 'rolandsteiner@google.com (Roland Steiner)'

# Result selection should be placed after the newly created element, collapsed, in order to allow successive insert operations.
# An non-wrapping insert operation on a non-collapsed selection should be equivalent to a delete operation followed by the insert operation.
# Elements that are not or only partially selected should remain, and retain their name and attributes.
# A selection that started as a text selection should remain a text selection.

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

INSERT_TESTS = {
  'id':         'I',
  'caption':    'Insert Tests',
  'checkAttrs': False,
  'checkStyle': False,
  
  'Proposed': [
    # inserthorizontalrule
    { 'id':         'IHR_TEXT-1_SC',
      'rte1-id':    'a-inserthorizontalrule-0',
      'desc':       'Insert <hr> into text',
      'command':    'inserthorizontalrule',
      'pad':        'foo^bar',
      'expected':   'foo<hr>^bar',
      'accept':     'foo<hr>|bar' },

    { 'id':         'IHR_TEXT-1_SI',
      'desc':       'Insert <hr>, replacing selected text',
      'command':    'inserthorizontalrule',
      'pad':        'foo[bar]baz',
      'expected':   'foo<hr>^baz',
      'accept':     'foo<hr>|bar' },

    { 'id':         'IHR_DIV-B-1_SX',
      'desc':       'Insert <hr> between elements',
      'command':    'inserthorizontalrule',
      'pad':        '<div><b>foo</b>|<b>bar</b></div>',
      'expected':   '<div><b>foo</b><hr>|<b>bar</b></div>' },

    { 'id':         'IHR_DIV-B-2_SO',
      'desc':       'Insert <hr>, replacing a fully wrapped element',
      'command':    'inserthorizontalrule',
      'pad':        '<div><b>foo</b>{<b>bar</b>}<b>baz</b></div>',
      'expected':   '<div><b>foo</b><hr>|<b>baz</b></div>' },

    { 'id':         'IHR_B-1_SC',
      'desc':       'Insert <hr> into a span, splitting it',
      'command':    'inserthorizontalrule',
      'pad':        '<b>foo^bar</b>',
      'expected':   '<b>foo</b><hr><b>^bar</b>' },

    { 'id':         'IHR_B-1_SS',
      'desc':       'Insert <hr> into a span at the start (should not create an empty span)',
      'command':    'inserthorizontalrule',
      'pad':        '<b>^foobar</b>',
      'expected':   '<hr><b>^foobar</b>' },

    { 'id':         'IHR_B-1_SE',
      'desc':       'Insert <hr> into a span at the end',
      'command':    'inserthorizontalrule',
      'pad':        '<b>foobar^</b>',
      'expected':   [ '<b>foobar</b><hr>|',
                      '<b>foobar</b><hr><b>^</b>' ] },

    { 'id':         'IHR_B-2_SL',
      'desc':       'Insert <hr> with oblique selection starting outside of span',
      'command':    'inserthorizontalrule',
      'pad':        'foo[bar<b>baz]qoz</b>',
      'expected':   'foo<hr>|<b>qoz</b>' },

    { 'id':         'IHR_B-2_SLR',
      'desc':       'Insert <hr> with oblique reversed selection starting outside of span',
      'command':    'inserthorizontalrule',
      'pad':        'foo]bar<b>baz[qoz</b>',
      'expected':   [ 'foo<hr>|<b>qoz</b>',
                      'foo<hr><b>^qoz</b>' ] },

    { 'id':         'IHR_B-3_SR',
      'desc':       'Insert <hr> with oblique selection ending outside of span',
      'command':    'inserthorizontalrule',
      'pad':        '<b>foo[bar</b>baz]quoz',
      'expected':   [ '<b>foo</b><hr>|quoz',
                      '<b>foo</b><hr><b>^</b>quoz' ] },

    { 'id':         'IHR_B-3_SRR',
      'desc':       'Insert <hr> with oblique reversed selection starting outside of span',
      'command':    'inserthorizontalrule',
      'pad':        '<b>foo]bar</b>baz[quoz',
      'expected':   '<b>foo</b><hr>|quoz' },

    { 'id':         'IHR_B-I-1_SM',
      'desc':       'Insert <hr> with oblique selection between different spans',
      'command':    'inserthorizontalrule',
      'pad':        '<b>foo[bar</b><i>baz]quoz</i>',
      'expected':   [ '<b>foo</b><hr>|<i>quoz</i>',
                      '<b>foo</b><hr><b>^</b><i>quoz</i>' ] },

    { 'id':         'IHR_B-I-1_SMR',
      'desc':       'Insert <hr> with reversed oblique selection between different spans',
      'command':    'inserthorizontalrule',
      'pad':        '<b>foo]bar</b><i>baz[quoz</i>',
      'expected':   '<b>foo</b><hr><i>^quoz</i>' },

    { 'id':         'IHR_P-1_SC',
      'desc':       'Insert <hr> into a paragraph, splitting it',
      'command':    'inserthorizontalrule',
      'pad':        '<p>foo^bar</p>',
      'expected':   [ '<p>bar</p><hr>|<p>bar</p>',
                      '<p>foo</p><hr><p>^bar</p>' ] },

    { 'id':         'IHR_P-1_SS',
      'desc':       'Insert <hr> into a paragraph at the start (should not create an empty span)',
      'command':    'inserthorizontalrule',
      'pad':        '<p>^foobar</p>',
      'expected':   [ '<hr>|<p>foobar</p>',
                      '<hr><p>^foobar</p>' ] },

    { 'id':         'IHR_P-1_SE',
      'desc':       'Insert <hr> into a paragraph at the end (should not create an empty span)',
      'command':    'inserthorizontalrule',
      'pad':        '<p>foobar^</p>',
      'expected':   '<p>foobar</p><hr>|' },

    # insertparagrap
    { 'id':         'IP_P-1_SC',
      'desc':       'Split paragraph',
      'command':    'insertparagraph',
      'pad':        '<p>foo^bar</p>',
      'expected':   '<p>foo</p><p>^bar</p>' },

    { 'id':         'IP_UL-LI-1_SC',
      'desc':       'Split list item',
      'command':    'insertparagraph',
      'pad':        '<ul><li>foo^bar</li></ul>',
      'expected':   '<ul><li>foo</li><li>^bar</li></ul>' },

    # inserttext
    { 'id':         'ITEXT:text_TEXT-1_SC',
      'desc':       'Insert text',
      'command':    'inserttext',
      'value':      'text',
      'pad':        'foo^bar',
      'expected':   'footext^bar' },

    { 'id':         'ITEXT:text_TEXT-1_SI',
      'desc':       'Insert text, replacing selected text',
      'command':    'inserttext',
      'value':      'text',
      'pad':        'foo[bar]baz',
      'expected':   'footext^baz' },

    # insertlinebreak
    { 'id':         'IBR_TEXT-1_SC',
      'desc':       'Insert <br> into text',
      'command':    'insertlinebreak',
      'pad':        'foo^bar',
      'expected':   [ 'foo<br>|bar',
                      'foo<br>^bar' ] },

    { 'id':         'IBR_TEXT-1_SI',
      'desc':       'Insert <br>, replacing selected text',
      'command':    'insertlinebreak',
      'pad':        'foo[bar]baz',
      'expected':   [ 'foo<br>|baz',
                      'foo<br>^baz' ] },

    { 'id':         'IBR_LI-1_SC',
      'desc':       'Insert <br> within list item',
      'command':    'insertlinebreak',
      'pad':        '<ul><li>foo^bar</li></ul>',
      'expected':   '<ul><li>foo<br>^bar</li></ul>' },

    # insertimage
    { 'id':         'IIMG:url_TEXT-1_SC',
      'rte1-id':    'a-insertimage-0',
      'desc':       'Insert image with URL "http://foo.com/bar.png"',
      'command':    'insertimage',
      'value':      'http://foo.com/bar.png',
      'checkAttrs':  True,
      'pad':        'foo^bar',
      'expected':   [ 'foo<img src="http://foo.com/bar.png">|bar',
                      'foo<img src="http://foo.com/bar.png">^bar' ] },

    { 'id':         'IIMG:url_IMG-1_SO',
      'desc':       'Change existing image to new URL, selection on <img>',
      'command':    'insertimage',
      'value':      'http://baz.com/quz.png',
      'checkAttrs':  True,
      'pad':        '<span>foo{<img src="http://foo.com/bar.png">}bar</span>',
      'expected':   [ '<span>foo<img src="http://baz.com/quz.png"/>|bar</span>',
                      '<span>foo<img src="http://baz.com/quz.png"/>^bar</span>' ] },

    { 'id':         'IIMG:url_SPAN-IMG-1_SO',
      'desc':       'Change existing image to new URL, selection in text surrounding <img>',
      'command':    'insertimage',
      'value':      'http://baz.com/quz.png',
      'checkAttrs':  True,
      'pad':        'foo[<img src="http://foo.com/bar.png">]bar',
      'expected':   [ 'foo<img src="http://baz.com/quz.png"/>|bar',
                      'foo<img src="http://baz.com/quz.png"/>^bar' ] },

    { 'id':         'IIMG:._SPAN-IMG-1_SO',
      'desc':       'Remove existing image or URL, selection on <img>',
      'command':    'insertimage',
      'value':      '',
      'checkAttrs':  True,
      'pad':        '<span>foo{<img src="http://foo.com/bar.png">}bar</span>',
      'expected':   [ '<span>foo^bar</span>',
                      '<span>foo<img>|bar</span>',
                      '<span>foo<img>^bar</span>',
                      '<span>foo<img src="">|bar</span>',
                      '<span>foo<img src="">^bar</span>' ] },

    { 'id':         'IIMG:._IMG-1_SO',
      'desc':       'Remove existing image or URL, selection in text surrounding <img>',
      'command':    'insertimage',
      'value':      '',
      'checkAttrs':  True,
      'pad':        'foo[<img src="http://foo.com/bar.png">]bar',
      'expected':   [ 'foo^bar',
                      'foo<img>|bar',
                      'foo<img>^bar',
                      'foo<img src="">|bar',
                      'foo<img src="">^bar' ] },

    # insertorderedlist
    { 'id':         'IOL_TEXT-1_SC',
      'rte1-id':    'a-insertorderedlist-0',
      'desc':       'Insert ordered list on collapsed selection',
      'command':    'insertorderedlist',
      'pad':        'foo^bar',
      'expected':   '<ol><li>foo^bar</li></ol>' },

    { 'id':         'IOL_TEXT-1_SI',
      'desc':       'Insert ordered list on selected text',
      'command':    'insertorderedlist',
      'pad':        'foo[bar]baz',
      'expected':   '<ol><li>foo[bar]baz</li></ol>' },

    # insertunorderedlist
    { 'id':         'IUL_TEXT-1_SC',
      'desc':       'Insert unordered list on collapsed selection',
      'command':    'insertunorderedlist',
      'pad':        'foo^bar',
      'expected':   '<ul><li>foo^bar</li></ul>' },

    { 'id':         'IUL_TEXT-1_SI',
      'rte1-id':    'a-insertunorderedlist-0',
      'desc':       'Insert unordered list on selected text',
      'command':    'insertunorderedlist',
      'pad':        'foo[bar]baz',
      'expected':   '<ul><li>foo[bar]baz</li></ul>' },

    # inserthtml
    { 'id':         'IHTML:BR_TEXT-1_SC',
      'rte1-id':    'a-inserthtml-0',
      'desc':       'InsertHTML: <br>',
      'command':    'inserthtml',
      'value':      '<br>',
      'pad':        'foo^barbaz',
      'expected':   'foo<br>^barbaz' },

    { 'id':         'IHTML:text_TEXT-1_SI',
      'desc':       'InsertHTML: "NEW"',
      'command':    'inserthtml',
      'value':      'NEW',
      'pad':        'foo[bar]baz',
      'expected':   'fooNEW^baz' },

    { 'id':         'IHTML:S_TEXT-1_SI',
      'desc':       'InsertHTML: "<span>NEW<span>"',
      'command':    'inserthtml',
      'value':      '<span>NEW</span>',
      'pad':        'foo[bar]baz',
      'expected':   'foo<span>NEW</span>^baz' },

    { 'id':         'IHTML:H1.H2_TEXT-1_SI',
      'desc':       'InsertHTML: "<h1>NEW</h1><h2>HTML</h2>"',
      'command':    'inserthtml',
      'value':      '<h1>NEW</h1><h2>HTML</h2>',
      'pad':        'foo[bar]baz',
      'expected':   'foo<h1>NEW</h1><h2>HTML</h2>^baz' },

    { 'id':         'IHTML:P-B_TEXT-1_SI',
      'desc':       'InsertHTML: "<p>NEW</b>HTML</b>!</p>"',
      'command':    'inserthtml',
      'value':      '<p>NEW</b>HTML</b>!</p>',
      'pad':        'foo[bar]baz',
      'expected':   'foo<p>NEW</b>HTML</b>!</p>^baz' }
  ]
}


