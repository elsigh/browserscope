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
__all__ = ['_SNIPPET_GROUPS', 'with_name',
           'CODE', 'DOC', 'GOOD', 'NAME', 'SUMMARY', 'VALUES', 'ABBREV']

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
# Maps values to abbreviated names.  For the large display, we create a set of
# abbreviated values and display those as representative of a whole group of
# tests.
ABBREV = 'abbrev'

# Common value sets
# Position is important so these should not be reordered or removed from.
BOOL_VALUES = ('false', 'true')
T_BOO = '"boolean"'
T_FUN = '"function"'
T_NUM = '"number"'
T_OBJ = '"object"'
T_STR = '"string"'
T_UND = '"undefined"'
TYPEOF_VALUES = (T_BOO, T_FUN, T_NUM, T_OBJ, T_STR, T_UND,
                 #'"array"', '"null"', '"other"', '"unknown"'
                 )
THROWS = ('throw',)

# Groups of side-effect free JS expressions that give information
# about the environment in which JS runs.
# This is an object whose repr() form is properly formatted JSON.
# For this to work, it must not contain any non-ASCII codepoints.
_SNIPPET_GROUPS = (
  # Get information about the browser that we can use when trying to
  # map a User-Agent request header to an environment file.
  # Some ES global definitions
  (
    { NAME: 'CoreFeatures',
      DOC: 'Summary of JS features independent of browser APIs' },

    { CODE: 'typeof undefined', NAME: 'Undef', VALUES: TYPEOF_VALUES,
      GOOD: ('"undefined"',), DOC: 'Is the global undefined really undefined',
      SUMMARY: 'undef OK', ABBREV: {} },
    { CODE: 'Infinity === 1/0', NAME: 'Inf', VALUES: BOOL_VALUES,
      GOOD: ('true',), DOC: 'Is the global Infinity set properly',
      SUMMARY: 'Inf OK', ABBREV: {} },
    { CODE: 'NaN !== NaN', NAME: 'NaN', VALUES: BOOL_VALUES,
      GOOD: ('true',), DOC: 'Is the global NaN set properly',
      SUMMARY: 'NaN OK', ABBREV: {} },
    { CODE: '!!this.window && this === window', NAME: 'GlblWin',
      VALUES: BOOL_VALUES, SUMMARY: 'window is global',
      DOC: 'Does "window" alias the global scope?', GOOD: ('true',),
      ABBREV: { 'true': 'global window' } },
    { CODE: '!(function () { return this; }.call(null))',
      NAME: 'Strict', VALUES: BOOL_VALUES,
      SUMMARY: 'Can "use strict"', DOC: 'Is EcmaScript5 strict mode supported?',
      GOOD: ('true',), ABBREV: { 'true': 'strict mode' } },
    { CODE: 'typeof Array.slice', NAME: 'ArrSlice',
      VALUES: TYPEOF_VALUES, SUMMARY: 'Array.slice', GOOD: (T_FUN,),
      ABBREV: { T_FUN: 'Array.slice' } },
    { CODE: 'typeof Function.prototype.bind', NAME: 'FnBind',
      VALUES: TYPEOF_VALUES, GOOD: (T_FUN,), SUMMARY: 'fn.bind',
      ABBREV: { T_FUN: 'fn.bind' } },
    { CODE: alt('!!eval("({get x() { return true; }})").x', 'false'),
      NAME: 'Gtrs', VALUES: BOOL_VALUES,
      DOC: 'Are getters/setters supported?',
      SUMMARY: 'getters', GOOD: ('true',), ABBREV: { 'true' : 'getters' } },
    { CODE: '(function (undefined) { return (0,eval)("undefined") === 1; })(1)',
      NAME: 'ES5 eval', GOOD: ('true',), SUMMARY: 'eval function',
      VALUES: BOOL_VALUES,
      DOC: ('Does eval differ when used as a function vs. as an operator?'
            '  See ES5 sec 15.1.2.1.1.'),
      ABBREV: { 'true': 'ES5 eval' } },
    { CODE: 'typeof Date.now', NAME: 'DateNow', VALUES: TYPEOF_VALUES,
      ABBREV: { T_FUN: 'Date.now' } },
  ),

  (
    { NAME: 'Serialization', DOC: 'JSON and serialization support' },

    ## Check whether native implementations are available
    { CODE: 'typeof JSON', NAME: 'JSON', VALUES: TYPEOF_VALUES,
      DOC: 'Is JSON defined natively?', SUMMARY: 'native JSON',
      GOOD: (T_OBJ, T_FUN), ABBREV: { T_OBJ: 'JSON', T_FUN: 'JSON' } },
    { CODE: 'typeof Object.prototype.toSource', NAME: 'ObjSrc',
      VALUES: TYPEOF_VALUES, ABBREV: { T_FUN: 'toSource' } },
    { CODE: 'typeof Object.prototype.toJSON', NAME: 'Obj2JSON',
      VALUES: TYPEOF_VALUES, ABBREV: { T_FUN: 'toJSON' }  },
    { CODE: 'typeof Date.prototype.toISOString',
      NAME: 'DateISO', VALUES: TYPEOF_VALUES, SUMMARY: 'date.toISOString',
      ABBREV: { T_FUN: 'date.toISOString' } },
    { CODE: 'typeof Date.prototype.toJSON',
      NAME: 'DateJSON', VALUES: TYPEOF_VALUES, SUMMARY: 'date.toJSON',
      ABBREV: { T_FUN: 'date.toJSON' } },
    { CODE: ('typeof JSON !== "undefined"'
             ' && JSON.stringify(false,'
             ' function (x) { return !this[x]; }) === "true"'),
      NAME: 'JSONStringify', VALUES: BOOL_VALUES,
      SUMMARY: 'JSON.stringify with replacer',
      ABBREV: { 'true': 'JSON replacer/reviver' } },
    { CODE: 'typeof uneval', NAME: 'Uneval', VALUES: TYPEOF_VALUES,
      ABBREV: { T_FUN: 'uneval' } },
  ),
  (
    { NAME: 'Events', DOC: 'Event APIs available.' },

    { CODE: 'typeof addEventListener', NAME: 'StdEv',
      VALUES: TYPEOF_VALUES, SUMMARY: 'standard events',
      ABBREV: { T_OBJ: 'addEventListener', T_FUN: 'addEventListener' } },
    # IE makes a lot of its functions, objects.
    # Fun fact: but not ActiveXObject.
    { CODE: 'typeof attachEvent', NAME: 'TOIEEv', VALUES: TYPEOF_VALUES,
      ABBREV: { T_OBJ: 'attachEvent', T_FUN: 'attachEvent' } },
    { CODE: '!!window.attachEvent', NAME: 'IEEv',
      VALUES: BOOL_VALUES, SUMMARY: 'IE events',
      ABBREV: { 'true': 'attachEvent' } },
    { CODE: 'typeof document.createEvent', NAME: 'DocCrtEv',
      VALUES: TYPEOF_VALUES, SUMMARY: 'doc.createEvent',
      ABBREV: { T_FUN: 'createEvent', T_OBJ: 'createEvent' } },
    { CODE: 'typeof document.createEventObject', NAME: 'TODocCrtEvO',
      VALUES: TYPEOF_VALUES, SUMMARY: 'createEventObject',
      ABBREV: { T_FUN: 'createEventObject', T_OBJ: 'createEventObject' } },
    { CODE: '!!document.createEventObject', NAME: 'DocCrtEvO',
      VALUES: BOOL_VALUES, SUMMARY: 'createEventObject',
      ABBREV: { 'true': 'createEventObject' } },
  ),
  (
    { NAME: 'DOM', DOC: 'DOM APIs' },

    { CODE: 'typeof document.getElementsByClassName', NAME: 'DocElByClass',
      VALUES: TYPEOF_VALUES, SUMMARY: 'native getElementsByClassName',
      GOOD: (T_FUN,), ABBREV: { T_FUN: 'getElementsByClassName' } },
    { CODE: 'typeof document.documentElement.getElementsByClassName',
      NAME: 'ElByClass', VALUES: TYPEOF_VALUES,
      SUMMARY: 'native getElementsByClassName', GOOD: (T_FUN,),
      ABBREV: { T_FUN: 'getElementsByClassName' } },
    { CODE: '!!document.all', NAME: 'DocAll', VALUES: BOOL_VALUES,
      SUMMARY: 'document.all', DOC: 'Is document.all present?',
      ABBREV: { 'true': 'document.all' } },
    { CODE: alt(
          "document.createElement('<input type=\"radio\">').type === 'radio'",
          'false'),
      NAME: 'ExtCreateEl', VALUES: BOOL_VALUES,
      SUMMARY: 'extended createElement syntax',
      ABBREV: { 'true': 'createElement+' } },
    { CODE: 'typeof document.documentElement.compareDocumentPosition',
      NAME: 'CmpDocPos', VALUES: TYPEOF_VALUES,
      SUMMARY: 'compareDocumentPosition',
      ABBREV: { T_FUN: 'compareDocumentPosition',
                T_OBJ: 'compareDocumentPosition' } },
    { CODE: 'typeof document.documentElement.contains',
      NAME: 'TOElCont', VALUES: TYPEOF_VALUES,
      SUMMARY: 'Element.contains',
      ABBREV: { T_FUN: 'contains', T_OBJ: 'contains' } },
    { CODE: '!!document.documentElement.contains',
      NAME: 'ElCont', VALUES: BOOL_VALUES,
      SUMMARY: 'Element.contains', ABBREV: { 'true': 'contains' } },
    { CODE: 'typeof document.createRange', NAME: 'DocCrtRng',
      VALUES: TYPEOF_VALUES, SUMMARY: 'doc.createRange',
      ABBREV: { T_FUN: 'createRange', T_OBJ: 'createRange' } },
    { CODE: 'typeof document.documentElement.doScroll',
      NAME: 'TODocElScroll', VALUES: TYPEOF_VALUES,
      SUMMARY: 'doScroll', ABBREV: { T_FUN: 'doScroll', T_OBJ: 'doScroll' } },
    { CODE: '!!document.documentElement.doScroll',
      NAME: 'DocElScroll', VALUES: BOOL_VALUES, SUMMARY: 'doScroll',
      ABBREV: { 'true': 'doScroll' } },
    { CODE: 'typeof document.documentElement.getBoundingClientRect',
      NAME: 'TODocElBoundRect', VALUES: TYPEOF_VALUES,
      SUMMARY: 'getBoundingClientRect',
      ABBREV: { T_FUN: 'getBoundingClientRect',
                T_OBJ: 'getBoundingClientRect' } },
    { CODE: '!!document.documentElement.getBoundingClientRect',
      NAME: 'DocElBoundRect', VALUES: BOOL_VALUES,
      SUMMARY: 'getBoundingClientRect',
      ABBREV: { 'true': 'getBoundingClientRect' } },
    { CODE: '"sourceIndex" in document.documentElement',
      NAME: 'SrcIdxDocEl', VALUES: BOOL_VALUES, SUMMARY: 'html.sourceIndex',
      ABBREV: { 'true': 'sourceIndex' } },
    { CODE: 'document.body.setAttribute.length === 2',
      NAME: 'SetAttr2', VALUES: BOOL_VALUES,
      SUMMARY: '2 param setAttribute',
      DOC: 'Does setAttribute need only the two parameters?',
      ABBREV: { 'true': 'setAttribute 2 params' } },
  ),

  (
    { NAME: 'Css', DOC: 'CSS' },

    # Is the styleSheet member available.
    # http//yuiblog.com/blog/2007/06/07/style/
    { CODE: "typeof document.createElement('style').styleSheet",
      NAME: 'DotSSheet', VALUES: TYPEOF_VALUES,
      SUMMARY: 'style.styleSheet',
      ABBREV: { T_FUN: '<style>.styleSheet', T_OBJ: '<style>.styleSheet' } },
    { CODE: 'typeof document.body.style.cssText',
      NAME: 'DotCssText', VALUES: TYPEOF_VALUES, SUMMARY: 'cssText',
      ABBREV: { T_STR: 'cssText' } },
    { CODE: 'typeof getComputedStyle', NAME: 'CompStyle',
      VALUES: TYPEOF_VALUES, SUMMARY: 'getComputedStyle',
      ABBREV: { T_FUN: 'getComputedStyle', T_OBJ: 'getComputedStyle' } },
    { CODE: 'typeof document.body.currentStyle', NAME: 'TOCurStyle',
      VALUES: TYPEOF_VALUES, SUMMARY: 'currentStyle',
      ABBREV: { T_FUN: 'currentStyle', T_OBJ: 'currentStyle' } },
    { CODE: '!!document.body.currentStyle', NAME: 'CurStyle',
      VALUES: BOOL_VALUES, SUMMARY: 'currentStyle',
      ABBREV: { 'true': 'currentStyle' } },
  ),

  (
    { NAME: 'Network', DOC: 'Network APIs' },

    { CODE: 'typeof XMLHttpRequest', NAME: 'XHR',
      VALUES: TYPEOF_VALUES, SUMMARY: 'XMLHttpRequest',
      GOOD: (T_FUN,), ABBREV: { T_FUN: 'XMLHttpRequest' } },
    { CODE: 'typeof ActiveXObject', NAME: 'ActiveX',
      VALUES: TYPEOF_VALUES, SUMMARY: 'ActiveXObject',
      ABBREV: { T_FUN: 'ActiveXObject', T_OBJ: 'ActiveXObject' } },
  ),

  (
    { NAME: 'Oddities', DOC: 'Bugs & Oddities' },

    ## Known bugs and inconsistencies
    { CODE: 'void 0 === ((function(){})[-2])', NAME: 'LeakyFn',
      VALUES: BOOL_VALUES, GOOD: ('true',),
      DOC: 'Do functions not leak dangerous info in negative indices?',
      SUMMARY: 'Function Junk', ABBREV: { 'false': 'leaky fn' } },
    { CODE: 'void 0 === ((function(){var b,a=function b(){};return b;})())',
      NAME: 'BadFnE', VALUES: BOOL_VALUES,
      DOC: 'Do function expressions not muck with the local scope?',
      SUMMARY: 'function exprs OK', GOOD: ('true',),
      ABBREV: { 'false': 'fn exprs declare' } },
    { CODE: '(function () { try { throw null; } finally { return true; } })()',
      NAME: 'FinallyOK', VALUES: BOOL_VALUES + THROWS,
      DOC: 'Do finally blocks fire even if there\'s no catch on the stack.',
      SUMMARY: 'finally OK', GOOD: ('true',),
      ABBREV: { 'false': 'finally broken' } },
    { CODE: ('0 === (function x() {'
             ' var toString = 0; return (function () { return toString; })();'
             ' })()'),
      NAME: 'NReifScope', VALUES: BOOL_VALUES,
      DOC: ('Do function scope frames for named functions not inherit'
            ' from Object.prototype?'
            '  http://yura.thinkweb2.com/named-function-expressions/'
            '#spidermonkey-peculiarity'),
      SUMMARY: 'function scope OK', GOOD: ('true',),
      ABBREV: { 'false': 'broken scopes' } },
    { CODE: '(function(){var e=true;try{throw false;}catch(e){}return e;})()',
      NAME: 'CatchScope', VALUES: BOOL_VALUES,
      DOC: 'Do exceptions scope properly?', SUMMARY: 'try scope OK',
      GOOD: ('true',), ABBREV: { 'false': 'catch leaks' } },
    { CODE: "typeof new RegExp('x')", NAME: 'TORegx',
      VALUES: TYPEOF_VALUES, DOC: 'Are RegExps functions or objects?',
      ABBREV: {} },
    { CODE: "'a'===('a'[0])", NAME: 'StrIdx', VALUES: BOOL_VALUES,
      SUMMARY: 'strings indexable', GOOD: ('true',),
      ABBREV: { 'false': 'strings not indexable' } },
    { CODE: '(function(){var a;if(0)function a(){}return void 0===a;})()',
      NAME: 'UnreachFn', VALUES: BOOL_VALUES,
      DOC: 'Are functions declared only if reachable?',
      SUMMARY: 'unreachable function', ABBREV: {} },
    { CODE: 'typeof ({}).__proto__', NAME: 'ProtoMem',
      VALUES: TYPEOF_VALUES, DOC: 'Is __proto__ defined for objects?',
      SUMMARY: '__proto__', ABBREV: {} },
    { CODE: 'eval("\'\u200d\'").length === 1', NAME: 'CfSig',
      VALUES: BOOL_VALUES, SUMMARY: '[:Cf:]', GOOD: ('true',),
      DOC: 'Are format control characters lexically significant?',
      ABBREV: { 'false': '[:Cf:]' } },
    { CODE: "'a,,a'.split(',').length === 3",
      NAME: 'SplitOK', VALUES: BOOL_VALUES, GOOD: ('true',),
      DOC: 'Does string.split work properly -- no skipping blanks?',
      SUMMARY: 'String.split OK',
      ABBREV: { 'false': 'string.split broken' } },
    { CODE: "[,].length === 1", NAME: 'ArrComma', VALUES: BOOL_VALUES,
      DOC: 'Is a trailing comma in an array ignored?',
      SUMMARY: 'Trailing comma', GOOD: ('true',),
      ABBREV: { 'false': '[,]' } },
    { CODE: ('(function (a) { a.length = 0; for (var _ in a) { return false; }'
             ' return true; })([0])'),
      NAME: 'LenNoEnum', VALUES: BOOL_VALUES,
      DOC: ('Does the length property of an array become enumerable'
            ' after being set?'),
      SUMMARY: 'Length DontEnum', GOOD: ('true',),
      ABBREV: { 'false': 'enum length' } },
    { CODE: '(function () { return arguments instanceof Array; })()',
      NAME: 'ArgsArr', VALUES: BOOL_VALUES,
      DOC: 'Is the arguments object an instanceof Array?',
      SUMMARY: 'arguments instanceof Array', GOOD: ('false',),
      ABBREV: { 'true': 'arguments array' } },
    { CODE: ('(function () {'
             ' return arguments instanceof Array'
                 ' && [].concat(arguments)[0][0] !== 1;'
             ' })(1, 2)'),
      NAME: 'CatArgsBug', VALUES: BOOL_VALUES, GOOD: ('false',),
      DOC: "Safari makes arguments an Array but breaks concat.",
      SUMMARY: 'Buggy arguments concat', ABBREV: { 'true': 'args concat' } },
    { CODE: '(function () { for (var _ in {}) return false; return true; })()',
      NAME: 'EmptyO', VALUES: BOOL_VALUES, GOOD: ('true',),
      DOC: "Have enumerable keys been added to Object.prototype?",
      SUMMARY: '{} empty', ABBREV: { 'false': '{} not empty' } },
    { CODE: '"name" in function () {}',
      NAME: 'FnName', VALUES: BOOL_VALUES,
      DOC: "Do functions have a <tt>name</tt> property?",
      SUMMARY: 'fn.name', ABBREV: { 'true': 'fn.name' } },
    { CODE: ('(function () {'
             ' function c() {}'
             ' c.prototype = {p:0};'
             ' return (new c).propertyIsEnumerable("p");'
             ' })()'),
      NAME: 'PropEnum', VALUES: BOOL_VALUES,
      DOC: "Are inherited properties inumerable?",
      SUMMARY: 'inherited enumerable', ABBREV: {} },
    { CODE: ('(function (x) {'
                'return eval("x",'
                            'function(x) {'
                              'return function() { return x * 0; }'
                            '}(true))'
              '}(false))'),
      NAME: 'Eval2', VALUES: BOOL_VALUES + THROWS,
      DOC: "Does eval violate integrity of closures?",
      SUMMARY: 'eval(s,f)',
      ABBREV: { 'true': 'eval(s,f) bug', 'throw': 'eval(s,f) global' } },
  ),
)

def init():
  global BY_NAME

  def dupes(items):
    seen = set()
    dupes = []
    for item in items:
      if item in seen:
        dupes.append(item)
      else:
        seen.add(item)
    return dupes
  # sanity checks
  all_snippets = []
  for group in _SNIPPET_GROUPS:
    assert tuple is type(group)
    group_info = group[0]
    assert dict is type(group_info)
    assert NAME in group_info and DOC in group_info
    assert str is type(group_info[NAME]), repr(group_info)
    assert str is type(group_info[DOC]), repr(group_info)
    for snippet in group[1:]:
      all_snippets.append(snippet)
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
      abbrev = snippet.get(ABBREV)
      assert (dict is type(abbrev)
              and reduce(lambda a, b: a and b in values and type(b) is str,
                         abbrev.iterkeys(), True)), (
        repr(snippet))
      assert str is type(snippet.get(NAME)), repr(snippet)
      assert str is type(snippet.get(CODE)), repr(snippet)
      assert str is type(snippet.get(DOC, '')), repr(snippet)
      summary = snippet.get(SUMMARY, '')
      assert (str is type(summary)
              and len(summary) < 40
              and '\n' not in summary), (repr(snippet))
    names = [snippet[NAME] for snippet in all_snippets]
    assert len(set(names)) == len(all_snippets), repr(dupes(names))
    group_names = [group[0][NAME] for group in _SNIPPET_GROUPS]
    assert len(set(group_names)) == len(_SNIPPET_GROUPS), (
        repr(dupes(group_names)))

    # initialize derived globals
    BY_NAME = dict([(snippet[NAME], snippet) for snippet in all_snippets])

init()

def with_name(name):
  """The snippet with the given name or None"""
  return BY_NAME.get(name)
