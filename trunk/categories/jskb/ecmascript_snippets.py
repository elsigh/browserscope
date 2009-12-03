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
__all__ = ['_SNIPPETS']

def alt(mayThrow, altValue):
  """Combines an expression with a fallback to use if the first expression
  failes with an exception."""

  return '(function(){try{return(%s);}catch(e){return(%s);}})()' % (
      mayThrow, altValue)

BOOL_VALUES = ('false', 'true')
TYPEOF_VALUES = ('"boolean"', '"function"', '"number"', '"object"', '"string"',
                 '"undefined"',
                 #'"array"', '"null"', '"other"', '"unknown"'
                 )

# Side-effect free JS expressions that give information about the environment
# in which JS runs.
# This is an object whose repr() form is properly formatted JSON.
# For this to work, it must not contain any non-ASCII codepoints.
_SNIPPETS = (
  # Get information about the browser that we can use when trying to
  # map a User-Agent request header to an environment file.
  # Some ES global definitions
  { 'code': 'typeof undefined', 'name': 'Undefined', 'values': TYPEOF_VALUES },
  { 'code': 'Infinity === 1/0', 'name': 'Infinity', 'values': BOOL_VALUES },
  { 'code': 'NaN !== NaN', 'name': 'NaN', 'values': BOOL_VALUES },
  { 'code': '!!this.window && this === window', 'name': 'WindowIsGlobal',
    'values': BOOL_VALUES },
  { 'code': '!(function () { return this; }.call(null))',
    'name': 'SupportsStrictMode', 'values': BOOL_VALUES },
  ## Check whether native implementations are available
  { 'code': 'typeof JSON', 'name': 'NativeJSON', 'values': TYPEOF_VALUES },
  { 'code': 'typeof addEventListener', 'name': 'AddEventListener',
    'values': TYPEOF_VALUES },
  # IE makes a lot of its functions, objects.
  # Fun fact: but not ActiveXObject.
  { 'code': 'typeof attachEvent', 'name': 'TypeofAttachEvent',
    'values': TYPEOF_VALUES },
  { 'code': '!!window.attachEvent', 'name': 'AttachEvent',
    'values': BOOL_VALUES },
  { 'code': 'typeof document.getElementsByClassName',
    'name': 'DocGetElementsByClassName', 'values': TYPEOF_VALUES },
  { 'code': 'typeof document.documentElement.getElementsByClassName',
    'name': 'GetElementsByClassName', 'values': TYPEOF_VALUES },
  { 'code': '!!document.all', 'name': 'DocumentAll', 'values': BOOL_VALUES },
  { 'code': 'typeof Date.now', 'name': 'DateNow', 'values': TYPEOF_VALUES },
  # Is the extended createElement syntax available?
  { 'code': alt(
        "document.createElement('<input type=\"radio\">').type === 'radio'",
        'false'),
    'name': 'ExtendedCreateElementSyntax', 'values': BOOL_VALUES },
  # Is the styleSheet member available.
  # http//yuiblog.com/blog/2007/06/07/style/
  { 'code': "typeof document.createElement('style').styleSheet",
    'name': 'StyleDotStyleSheet', 'values': TYPEOF_VALUES },
  { 'code': 'typeof document.body.style.cssText',
    'name': 'StyleDotCssText', 'values': TYPEOF_VALUES },
  { 'code': 'typeof XMLHttpRequest', 'name': 'TypeofXMLHttpRequest',
    'values': TYPEOF_VALUES },
  { 'code': 'typeof ActiveXObject', 'name': 'TypeofActiveXObject',
    'values': TYPEOF_VALUES },
  { 'code': 'typeof getComputedStyle', 'name': 'TypeofGetComputedStyle',
    'values': TYPEOF_VALUES },
  { 'code': 'typeof document.body.currentStyle', 'name': 'TypeofCurrentStyle',
    'values': TYPEOF_VALUES },
  { 'code': '!!document.body.currentStyle', 'name': 'CurrentStyle',
    'values': BOOL_VALUES },
  { 'code': 'typeof document.documentElement.compareDocumentPosition',
    'name': 'TypeofCompareDocumentPosition', 'values': TYPEOF_VALUES },
  { 'code': 'typeof document.documentElement.contains',
    'name': 'TypeofElementContains', 'values': TYPEOF_VALUES },
  { 'code': '!!document.documentElement.contains',
    'name': 'ElementContains', 'values': BOOL_VALUES },
  { 'code': 'typeof document.createEvent', 'name': 'TypeofDocumentCreateEvent',
    'values': TYPEOF_VALUES },
  { 'code': 'typeof document.createRange', 'name': 'TypeofDocumentCreateRange',
    'values': TYPEOF_VALUES },
  { 'code': 'typeof document.documentElement.doScroll',
    'name': 'TypeofDocumentElementDoScroll', 'values': TYPEOF_VALUES },
  { 'code': '!!typeof document.documentElement.doScroll',
    'name': 'DocumentElementDoScroll', 'values': BOOL_VALUES },
  { 'code': 'typeof document.documentElement.getBoundingClientRect',
    'name': 'TypeofDocumentElementGetBoundingClientRect',
    'values': TYPEOF_VALUES },
  { 'code': '!!document.documentElement.getBoundingClientRect',
    'name': 'DocumentElementGetBoundingClientRect', 'values': BOOL_VALUES },
  { 'code': '"sourceIndex" in document.documentElement',
    'name': 'SourceIndexInDocumentElement', 'values': BOOL_VALUES },
  { 'code': 'typeof document.createEventObject',
    'name': 'TypeofDocumentCreateEventObject', 'values': TYPEOF_VALUES },
  { 'code': '!!document.createEventObject',
    'name': 'DocumentCreateEventObject', 'values': BOOL_VALUES },
  { 'code': 'typeof Date.prototype.toISOString',
    'name': 'TypeofDateToISOString', 'values': TYPEOF_VALUES },
  { 'code': 'typeof Date.prototype.toJSON',
    'name': 'TypeofDateToJSON', 'values': TYPEOF_VALUES },
  { 'code': 'typeof Array.slice', 'name': 'TypeofArraySlice',
    'values': TYPEOF_VALUES },
  { 'code': 'typeof Function.prototype.bind', 'name': 'TypeofFunctionBind',
    'values': TYPEOF_VALUES },
  { 'code': 'typeof Object.prototype.toSource', 'name': 'TypeofObjectToSource',
    'values': TYPEOF_VALUES },
  { 'code': 'typeof uneval', 'name': 'TypeofUneval', 'values': TYPEOF_VALUES },
  ## Check for known bugs and inconsistencies
  # Do functions not leak dangerous info in negative indices?
  { 'code': 'void 0 === ((function(){})[-2])', 'name': 'LeakyFunctions',
    'values': BOOL_VALUES },
  # Do function expressions not muck with the local scope?
  { 'code': 'void 0 === ((function(){var b,a=function b(){};return b;})())',
    'name': 'BadFunctionExprs', 'values': BOOL_VALUES },
  # Do function scope frames inherit from Object.prototype?
  # http://yura.thinkweb2.com/named-function-expressions/#spidermonkey-peculiarity
  { 'code': ('0 === (function () {'
             ' var toString = 0; return (function () { return toString; })();'
             ' })()'),
    'name': 'LexicalScopesAreNotObjects', 'values': BOOL_VALUES },
  # Do exceptions scope properly?
  { 'code': '(function(){var e=true;try{throw false;}catch(e){}return e;})()',
    'name': 'CaughtExceptionsScoped', 'values': BOOL_VALUES },
  # Are regex functions or objects?
  { 'code': "typeof new RegExp('x')", 'name': 'TypeofRegExpInstance',
    'values': TYPEOF_VALUES },
  # Are strings indexable
  { 'code': "'a'===('a'[0])", 'name': 'IndexableStrings',
    'values': BOOL_VALUES },
  # Are functions declared only if reachable?
  { 'code': '(function(){var a;if(0)function a(){}return void 0===a;})()',
    'name': 'UnreachableFnDeclsUndefined', 'values': BOOL_VALUES },
  # Is __proto__ defined for objects?
  { 'code': 'typeof ({}).__proto__', 'name': 'ProtoExposed',
    'values': TYPEOF_VALUES },
  # Does setAttribute need only the two parameters?
  { 'code': 'document.body.setAttribute.length === 2',
    'name': 'TwoParamSetAttribute', 'values': BOOL_VALUES },
  # Are format control characters lexically significant?
  { 'code': 'eval("\'\u200d\'").length === 1', 'name': 'CfSignificant',
    'values': BOOL_VALUES },
  # Does string.split work properly?
  { 'code': "'a,,a'.split(',').length === 3",
    'name': 'StringSplitPreservesBlanks', 'values': BOOL_VALUES },
)

def sanity_checks():
  for snippet in _SNIPPETS:
    values = snippet.get('values')
    assert (tuple is type(values)
            and reduce(lambda a, b: a and type(b) is str, values, True)
            and len(set(values)) == len(values)), (
      repr(snippet))
    assert str is type(snippet.get('name')), repr(snippet)
    assert str is type(snippet.get('code')), repr(snippet)
    assert str is type(snippet.get('doc', '')), repr(snippet)
  names = set([snippet['name'] for snippet in _SNIPPETS])
  assert len(names) == len(_SNIPPETS), repr(names)

sanity_checks()
