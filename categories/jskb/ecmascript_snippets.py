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

def alt(mayThrow, altValue):
  """Combines an expression with a fallback to use if the first expression
  failes with an exception."""

  return '(function(){try{return(%s);}catch(e){return(%s);}})()' % (
      mayThrow, altValue)

# Side-effect free JS expressions that give information about the environment
# in which JS runs.
# This is an object whose repr() form is properly formatted JSON.
# For this to work, it must not contain any non-ASCII codepoints.
_SNIPPETS = [
  # Get information about the browser that we can use when trying to
  # map a User-Agent request header to an environment file.
  { 'code': 'navigator.userAgent', 'name': 'UserAgent',
    'doc': 'Can be matched against user-agent header' },
  { 'code': 'navigator.appName', 'name': 'AppName' },
  { 'code': 'navigator.appVersion', 'name': 'AppVersion' },
  { 'code': 'navigator.platform', 'name': 'Platform' },
  # Some ES global definitions
  { 'code': 'typeof undefined', 'name': 'Undefined' },
  { 'code': 'Infinity === 1/0', 'name': 'Infinity' },
  { 'code': 'NaN !== NaN', 'name': 'NaN' },
  { 'code': '!!this.window && this === window', 'name': 'WindowIsGlobal' },
  { 'code': '!(function () { return this; }.call(null))',
    'name': 'SupportsStrictMode' },
  ## Check whether native implementations are available
  { 'code': 'typeof JSON', 'name': 'NativeJSON' },
  { 'code': 'typeof addEventListener', 'name': 'AddEventListener' },
  # IE makes a lot of its functions, objects.
  # Fun fact: but not ActiveXObject.
  { 'code': 'typeof attachEvent', 'name': 'TypeofAttachEvent' },
  { 'code': '!!window.attachEvent', 'name': 'AttachEvent' },
  { 'code': 'typeof document.getElementsByClassName',
    'name': 'DocGetElementsByClassName' },
  { 'code': 'typeof document.documentElement.getElementsByClassName',
    'name': 'GetElementsByClassName' },
  { 'code': '!!document.all', 'name': 'DocumentAll' },
  { 'code': 'typeof Date.now', 'name': 'DateNow' },
  # Is the extended createElement syntax available?
  { 'code': alt("document.createElement('<input type=\"radio\">').type === 'radio'",
                'false'),
    'name': 'ExtendedCreateElementSyntax' },
  # Is the styleSheet member available.
  # http//yuiblog.com/blog/2007/06/07/style/
  { 'code': "typeof document.createElement('style').styleSheet",
    'name': 'StyleDotStyleSheet' },
  { 'code': 'typeof document.body.style.cssText',
    'name': 'StyleDotCssText' },
  { 'code': 'typeof XMLHttpRequest', 'name': 'TypeofXMLHttpRequest' },
  { 'code': 'typeof ActiveXObject', 'name': 'TypeofActiveXObject' },
  { 'code': 'typeof getComputedStyle', 'name': 'TypeofGetComputedStyle' },
  { 'code': 'typeof document.body.currentStyle', 'name': 'TypeofCurrentStyle' },
  { 'code': '!!document.body.currentStyle', 'name': 'CurrentStyle' },
  { 'code': 'typeof document.documentElement.compareDocumentPosition',
    'name': 'TypeofCompareDocumentPosition' },
  { 'code': 'typeof document.documentElement.contains',
    'name': 'TypeofElementContains' },
  { 'code': '!!document.documentElement.contains',
    'name': 'ElementContains' },
  { 'code': 'typeof document.createEvent', 'name': 'TypeofDocumentCreateEvent' },
  { 'code': 'typeof document.createRange', 'name': 'TypeofDocumentCreateRange' },
  { 'code': 'typeof document.documentElement.doScroll',
    'name': 'TypeofDocumentElementDoScroll' },
  { 'code': '!!typeof document.documentElement.doScroll',
    'name': 'DocumentElementDoScroll' },
  { 'code': 'typeof document.documentElement.getBoundingClientRect',
    'name': 'TypeofDocumentElementGetBoundingClientRect' },
  { 'code': '!!document.documentElement.getBoundingClientRect',
    'name': 'fDocumentElementGetBoundingClientRect' },
  { 'code': '"sourceIndex" in document.documentElement',
    'name': 'SourceIndexInDocumentElement' },
  { 'code': 'typeof document.createEventObject',
    'name': 'TypeofDocumentCreateEventObject' },
  { 'code': '!!document.createEventObject',
    'name': 'DocumentCreateEventObject' },
  { 'code': 'typeof Date.prototype.toISOString',
    'name': 'TypeofDateToISOString' },
  { 'code': 'typeof Date.prototype.toJSON',
    'name': 'TypeofDateToJSON' },
  { 'code': 'typeof Array.slice', 'name': 'TypeofArraySlice' },
  { 'code': 'typeof Function.prototype.bind', 'name': 'TypeofFunctionBind' },
  { 'code': 'typeof Object.prototype.toSource', 'name': 'TypeofObjectToSource' },
  { 'code': 'typeof uneval', 'name': 'TypeofUneval' },
  ## Check for known bugs and inconsistencies
  # Do functions not leak dangerous info in negative indices?
  { 'code': 'void 0 === ((function(){})[-2])', 'name': 'LeakyFunctions' },
  # Do function expressions not muck with the local scope?
  { 'code': 'void 0 === ((function(){var b,a=function b(){};return b;})())',
    'name': 'BadFunctionExprs' },
  # Do function scope frames inherit from Object.prototype?
  # http://yura.thinkweb2.com/named-function-expressions/#spidermonkey-peculiarity
  { 'code': ('0 === (function () {'
             ' var toString = 0; return (function () { return toString; })();'
             ' })()'),
    'name': 'LexicalScopesAreNotObjects' },
  # Do exceptions scope properly?
  { 'code': '(function(){var e=true;try{throw false;}catch(e){}return e;})()',
    'name': 'CaughtExceptionsScoped' },
  # Are regex functions or objects?
  { 'code': "typeof new RegExp('x')", 'name': 'TypeofRegExpInstance' },
  # Are strings indexable
  { 'code': "'a'==('a'[0])", 'name': 'IndexableStrings' },
  # Are functions declared only if reachable?
  { 'code': '(function(){var a;if(0)function a(){}return void 0===a;})()',
    'name': 'UnreachableFnDeclsUndefined' },
  # Is __proto__ defined for objects?
  { 'code': 'typeof ({}).__proto__', 'name': 'ProtoExposed' },
  # Does setAttribute need only the two parameters?
  { 'code': 'document.body.setAttribute.length === 2',
    'name': 'TwoParamSetAttribute' },
  # Are format control characters lexically significant?
  { 'code': 'eval("\'\u200d\'").length === 1', 'name': 'CfSignificant' },
  # Does string.split work properly?
  { 'code': "'a,,a'.split(',').length === 3",
    'name': 'StringSplitPreservesBlanks' },
]
