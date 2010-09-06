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

"""Selection tests"""

__author__ = 'rolandsteiner@google.com (Roland Steiner)'

SELECTION_TESTS = {
  'id':            'S',
  'caption':       'Selection Tests',
  'checkAttrs':    True,
  'checkStyle':    True,
  'checkSel':      True,
  'styleWithCSS':  False,

  'RFC': [
    # selectall
    { 'id':          'SELALL-TEXT',
      'desc':        'select all, text only',
      'command':     'selectall',
      'pad':         'foo[bar]baz',
      'expected':    [ '[foobarbaz]',
                       '{foobarbaz}' ] },

    { 'id':          'SELALL-I',
      'desc':        'select all, with outer tags',
      'command':     'selectall',
      'pad':         '<i>foo[bar]baz</i>',
      'expected':    '{<i>foobarbaz</i>}' },

    # unselect
    { 'id':          'UNSEL-TEXT',
      'desc':        'unselect',
      'command':     'unselect',
      'pad':         'foo[bar]baz',
      'expected':    'foobarbaz' },

#    # window.getSelection().selectAllChildren(<element>)
#    { 'id':          'SELALLCHILDREN-DIV',
#      'desc':        'selectAllChildren(<element>) on div',
#      'function':    'window.getSelection().selectAllChildren(document.getElementById("test"));',
#      'pad':         'foo<div id="test">bar <span>baz</span></div>qoz',
#      'expected':    'foo<div id="test">[bar <span>baz</span>]</div>qoz' }
  ]
};

