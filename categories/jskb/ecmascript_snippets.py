#!/usr/bin/python2.4
#
# Copyright 2009 Google Inc.
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

"""
Defines the code snippets that the JavaScript Knowledge Base tracks.
"""

__author__ = 'msamuel@google.com (Mike Samuel)'
__all__ = ['_SNIPPETS', 'with_name',
           'CODE', 'DOC', 'GOOD', 'NAME', 'SUMMARY', 'VALUES']

def alt(mayThrow, altValue):
  """Combines an expression with a fallback to use if the first expression
  failes with an exception."""

  return '(function(){try{return(%s);}catch(e){return(%s);}})()' % (
      mayThrow, altValue)

# Dictionary keys
CODE = 'code'  # The ES source code to execute
DOC = 'doc'  # Detailed description of the reason this snippet is important.
GOOD = 'good'  # Good values
NAME = 'name'  # Identifier used in database
SUMMARY = 'summary'  # Short description.
# Expected results as JSON or the keyword "throw" which indicates abnormal exit.
# Should not be reordered or removed from
VALUES = 'values'

# Common value sets
# Position is important so these should not be reordered or removed from.
BOOL_VALUES = ('false', 'true')
TYPEOF_VALUES = ('"boolean"', '"function"', '"number"', '"object"', '"string"',
                 '"undefined"',
                 #'"array"', '"null"', '"other"', '"unknown"'
                 )
THROWS = ('throw',)

# Side-effect free JS expressions that give information about the environment
# in which JS runs.
# This is an object whose repr() form is properly formatted JSON.
# For this to work, it must not contain any non-ASCII codepoints.
_SNIPPETS = (
  # Get information about the browser that we can use when trying to
  # map a User-Agent request header to an environment file.
  # Some ES global definitions
  { CODE: 'typeof undefined', NAME: 'Undefined', VALUES: TYPEOF_VALUES,
    GOOD: ('"undefined"',) },
  { CODE: 'Infinity === 1/0', NAME: 'Infinity', VALUES: BOOL_VALUES,
    GOOD: ('true',) },
  { CODE: 'NaN !== NaN', NAME: 'NaN', VALUES: BOOL_VALUES,
    GOOD: ('true',) },
  { CODE: '!!this.window && this === window', NAME: 'WindowIsGlobal',
    VALUES: BOOL_VALUES, SUMMARY: 'window is global',
    DOC: 'Does "window" alias the global scope?', GOOD: ('true',) },
  { CODE: '!(function () { return this; }.call(null))',
    NAME: 'SupportsStrictMode', VALUES: BOOL_VALUES,
    SUMMARY: 'Can "use strict"', DOC: 'Is EcmaScript5 Strict mode supported?',
    GOOD: ('true',) },
  ## Check whether native implementations are available
  { CODE: 'typeof JSON', NAME: 'NativeJSON', VALUES: TYPEOF_VALUES,
    DOC: 'Is JSON defined natively?', SUMMARY: 'native JSON',
    GOOD: ('"object"', '"function"') },
  { CODE: 'typeof addEventListener', NAME: 'AddEventListener',
    VALUES: TYPEOF_VALUES, SUMMARY: 'standard events' },
  # IE makes a lot of its functions, objects.
  # Fun fact: but not ActiveXObject.
  { CODE: 'typeof attachEvent', NAME: 'TypeofAttachEvent',
    VALUES: TYPEOF_VALUES,  },
  { CODE: '!!window.attachEvent', NAME: 'AttachEvent',
    VALUES: BOOL_VALUES, SUMMARY: 'IE events' },
  { CODE: 'typeof document.getElementsByClassName',
    NAME: 'DocGetElementsByClassName', VALUES: TYPEOF_VALUES,
    SUMMARY: 'native getElementsByClassName',
    GOOD: ('"function"',) },
  { CODE: 'typeof document.documentElement.getElementsByClassName',
    NAME: 'GetElementsByClassName', VALUES: TYPEOF_VALUES,
    SUMMARY: 'native getElementsByClassName',
    GOOD: ('"function"',) },
  { CODE: '!!document.all', NAME: 'DocumentAll', VALUES: BOOL_VALUES },
  { CODE: 'typeof Date.now', NAME: 'DateNow', VALUES: TYPEOF_VALUES },
  { CODE: alt(
        "document.createElement('<input type=\"radio\">').type === 'radio'",
        'false'),
    NAME: 'ExtendedCreateElementSyntax', VALUES: BOOL_VALUES,
    SUMMARY: 'extended createElement syntax' },
  # Is the styleSheet member available.
  # http//yuiblog.com/blog/2007/06/07/style/
  { CODE: "typeof document.createElement('style').styleSheet",
    NAME: 'StyleDotStyleSheet', VALUES: TYPEOF_VALUES,
    SUMMARY: 'StyleElement.styleSheet' },
  { CODE: 'typeof document.body.style.cssText',
    NAME: 'StyleDotCssText', VALUES: TYPEOF_VALUES,
    SUMMARY: 'cssText' },
  { CODE: 'typeof XMLHttpRequest', NAME: 'TypeofXMLHttpRequest',
    VALUES: TYPEOF_VALUES, SUMMARY: 'XMLHttpRequest',
    GOOD: ('"function"',) },
  { CODE: 'typeof ActiveXObject', NAME: 'TypeofActiveXObject',
    VALUES: TYPEOF_VALUES, SUMMARY: 'ActiveXObject' },
  { CODE: 'typeof getComputedStyle', NAME: 'TypeofGetComputedStyle',
    VALUES: TYPEOF_VALUES, SUMMARY: 'getComputedStyle' },
  { CODE: 'typeof document.body.currentStyle', NAME: 'TypeofCurrentStyle',
    VALUES: TYPEOF_VALUES, SUMMARY: 'currentStyle' },
  { CODE: '!!document.body.currentStyle', NAME: 'CurrentStyle',
    VALUES: BOOL_VALUES, SUMMARY: 'currentStyle' },
  { CODE: 'typeof document.documentElement.compareDocumentPosition',
    NAME: 'TypeofCompareDocumentPosition', VALUES: TYPEOF_VALUES,
    SUMMARY: 'compareDocumentPosition' },
  { CODE: 'typeof document.documentElement.contains',
    NAME: 'TypeofElementContains', VALUES: TYPEOF_VALUES,
    SUMMARY: 'Element.contains' },
  { CODE: '!!document.documentElement.contains',
    NAME: 'ElementContains', VALUES: BOOL_VALUES,
    SUMMARY: 'Element.contains'},
  { CODE: 'typeof document.createEvent', NAME: 'TypeofDocumentCreateEvent',
    VALUES: TYPEOF_VALUES },
  { CODE: 'typeof document.createRange', NAME: 'TypeofDocumentCreateRange',
    VALUES: TYPEOF_VALUES },
  { CODE: 'typeof document.documentElement.doScroll',
    NAME: 'TypeofDocumentElementDoScroll', VALUES: TYPEOF_VALUES,
    SUMMARY: 'doScroll' },
  { CODE: '!!typeof document.documentElement.doScroll',
    NAME: 'DocumentElementDoScroll', VALUES: BOOL_VALUES,
    SUMMARY: 'doScroll' },
  { CODE: 'typeof document.documentElement.getBoundingClientRect',
    NAME: 'TypeofDocumentElementGetBoundingClientRect',
    VALUES: TYPEOF_VALUES, SUMMARY: 'getBoundingClientRect' },
  { CODE: '!!document.documentElement.getBoundingClientRect',
    NAME: 'DocumentElementGetBoundingClientRect', VALUES: BOOL_VALUES,
    SUMMARY: 'getBoundingClientRect' },
  { CODE: '"sourceIndex" in document.documentElement',
    NAME: 'SourceIndexInDocumentElement', VALUES: BOOL_VALUES,
    SUMMARY: 'BodyElement.sourceIndex' },
  { CODE: 'typeof document.createEventObject',
    NAME: 'TypeofDocumentCreateEventObject', VALUES: TYPEOF_VALUES,
    SUMMARY: 'document.createEventObject' },
  { CODE: '!!document.createEventObject',
    NAME: 'DocumentCreateEventObject', VALUES: BOOL_VALUES,
    SUMMARY: 'document.createEventObject' },
  { CODE: 'typeof Date.prototype.toISOString',
    NAME: 'TypeofDateToISOString', VALUES: TYPEOF_VALUES },
  { CODE: 'typeof Date.prototype.toJSON',
    NAME: 'TypeofDateToJSON', VALUES: TYPEOF_VALUES },
  { CODE: 'typeof Array.slice', NAME: 'TypeofArraySlice',
    VALUES: TYPEOF_VALUES, SUMMARY: 'Array.slice', GOOD: ('"function"',) },
  { CODE: 'typeof Function.prototype.bind', NAME: 'TypeofFunctionBind',
    VALUES: TYPEOF_VALUES, GOOD: ('"function"',) },
  { CODE: 'typeof Object.prototype.toSource', NAME: 'TypeofObjectToSource',
    VALUES: TYPEOF_VALUES },
  { CODE: 'typeof uneval', NAME: 'TypeofUneval', VALUES: TYPEOF_VALUES },
  ## Known bugs and inconsistencies
  { CODE: 'void 0 === ((function(){})[-2])', NAME: 'LeakyFunctions',
    VALUES: BOOL_VALUES, GOOD: ('true',),
    DOC: 'Do functions not leak dangerous info in negative indices?',
    SUMMARY: 'Function Junk' },
  { CODE: 'void 0 === ((function(){var b,a=function b(){};return b;})())',
    NAME: 'BadFunctionExprs', VALUES: BOOL_VALUES,
    DOC: 'Do function expressions not muck with the local scope?',
    SUMMARY: 'function exprs OK', GOOD: ('true',) },
  { CODE: '(function () { try { throw null; } finally { return true; } })()',
    NAME: 'FinallyWorks', VALUES: BOOL_VALUES + THROWS,
    DOC: 'Do finally blocks fire even if there\'s no catch on the stack.',
    SUMMARY: 'finally OK', GOOD: ('true',) },
  { CODE: ('0 === (function () {'
             ' var toString = 0; return (function () { return toString; })();'
             ' })()'),
    NAME: 'LexicalScopesAreNotObjects', VALUES: BOOL_VALUES,
    DOC: ('Do function scope frames not inherit from Object.prototype?'
          '  http://yura.thinkweb2.com/named-function-expressions/'
          '#spidermonkey-peculiarity'),
    SUMMARY: 'function scope OK', GOOD: ('true',) },
  { CODE: '(function(){var e=true;try{throw false;}catch(e){}return e;})()',
    NAME: 'CaughtExceptionsScoped', VALUES: BOOL_VALUES,
    DOC: 'Do exceptions scope properly?', SUMMARY: 'try scope OK',
    GOOD: ('true',) },
  { CODE: "typeof new RegExp('x')", NAME: 'TypeofRegExpInstance',
    VALUES: TYPEOF_VALUES, DOC: 'Are RegExps functions or objects?' },
  { CODE: "'a'===('a'[0])", NAME: 'IndexableStrings',
    VALUES: BOOL_VALUES, SUMMARY: 'strings indexable',
    GOOD: ('true',) },
  { CODE: '(function(){var a;if(0)function a(){}return void 0===a;})()',
    NAME: 'UnreachableFnDeclsUndefined', VALUES: BOOL_VALUES,
    DOC: 'Are functions declared only if reachable?',
    SUMMARY: 'unreachable function' },
  { CODE: 'typeof ({}).__proto__', NAME: 'ProtoExposed',
    VALUES: TYPEOF_VALUES, DOC: 'Is __proto__ defined for objects?',
    SUMMARY: '__proto__' },
  { CODE: 'document.body.setAttribute.length === 2',
    NAME: 'TwoParamSetAttribute', VALUES: BOOL_VALUES,
    SUMMARY: '2 param setAttribute',
    DOC: 'Does setAttribute need only the two parameters?' },
  { CODE: 'eval("\'\u200d\'").length === 1', NAME: 'CfSignificant',
    VALUES: BOOL_VALUES, SUMMARY: '[:Cf:]',
    DOC: 'Are format control characters lexically significant?',
    GOOD: ('true',) },
  { CODE: "'a,,a'.split(',').length === 3",
    NAME: 'StringSplitPreservesBlanks', VALUES: BOOL_VALUES,
    DOC: 'Does string.split work properly -- no skipping blanks?',
    SUMMARY: 'String.split OK', GOOD: ('true',) },
  { CODE: "[,].length === 1",
    NAME: 'ArrayTrailingComma', VALUES: BOOL_VALUES,
    DOC: 'Is a trailing comma in an array ignored?',
    SUMMARY: 'TrailingComma', GOOD: ('true',) },
)

def init():
  global BY_NAME
  # sanity checks
  for snippet in _SNIPPETS:
    values = snippet.get(VALUES)
    assert (tuple is type(values)
            and reduce(lambda a, b: a and type(b) is str, values, True)
            and len(set(values)) == len(values)), (
      repr(snippet))
    good = snippet.get(GOOD)
    if good is not None:
      assert (tuple is type(good)
              and reduce(lambda a, b: a and b in values, good, True)
              and len(set(good)) == len(good)), (
        repr(snippet))
    assert str is type(snippet.get(NAME)), repr(snippet)
    assert str is type(snippet.get(CODE)), repr(snippet)
    assert str is type(snippet.get(DOC, '')), repr(snippet)
    summary = snippet.get(SUMMARY, '')
    assert (str is type(summary)
            and len(summary) < 40
            and '\n' not in summary), (repr(snippet))
  names = set([snippet[NAME] for snippet in _SNIPPETS])
  assert len(names) == len(_SNIPPETS), repr(names)
  # initialize derived globals
  BY_NAME = dict([(snippet[NAME], snippet) for snippet in _SNIPPETS])

init()

def with_name(name):
  """The snippet with the given name or None"""
  return BY_NAME.get(name)
