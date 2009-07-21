#!/usr/bin/python2.4
#
# Copyright 2009 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the 'License')
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Handlers for Rich Text Tests"""

__author__ = 'annie.sullivan@gmail.com (Annie Sullivan)'

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import django
from django import http
from django import shortcuts

from django.template import add_to_builtins
add_to_builtins('base.custom_filters')

# Shared stuff
from shared import decorators

commands = {
  'backcolor' : {
    'opt_arg': '#FF0000',
    'test_unapply': True,
    'collapse': False,
    'unapply_extras': []},
  'bold' : {
    'opt_arg': None,
    'test_unapply': True,
    'collapse': False,
    'unapply_extras': [
      "['<b>', '</b>']",
      "['<STRONG>', '</STRONG>']",
      "['<span style=\"font-weight: bold;\">', '</span>']"]},
  'createbookmark' : {
    'opt_arg': 'bookmark_name',
    'test_unapply': False,
    'collapse': False,
    'unapply_extras': []},
  'createlink' : {
    'opt_arg': 'http://www.openweb.org',
    'test_unapply': False,
    'collapse': False,
    'unapply_extras': []},
  'decreasefontsize' : {
    'opt_arg': None,
    'test_unapply': False,
    'collapse': False,
    'unapply_extras': []},
  'fontname' : {
    'opt_arg': 'Arial',
    'test_unapply': False,
    'collapse': False,
    'unapply_extras': []},
  'fontsize' : {
    'opt_arg': 4,
    'test_unapply': False,
    'collapse': False,
    'unapply_extras': []},
  'forecolor' : {
    'opt_arg': '#FF0000',
    'test_unapply': False,
    'collapse': False,
    'unapply_extras': []},
  'formatblock' : {
    'opt_arg': 'h1',
    'test_unapply': True,
    'collapse': False,
    'unapply_extras': []},
  'indent' : {
    'opt_arg': None,
    'test_unapply': False,
    'collapse': False,
    'unapply_extras': []},
  'inserthorizontalrule' : {
    'opt_arg': None,
    'test_unapply': False,
    'collapse': True,
    'unapply_extras': []},
  'inserthtml': {
    'opt_arg': '<br>',
    'test_unapply': False,
    'collapse': True,
    'unapply_extras': []},
  'insertimage': {
    'opt_arg': 'http://www.google.com/intl/en_ALL/images/logo.gif',
    'test_unapply': False,
    'collapse': True,
    'unapply_extras': []},
  'insertorderedlist' : {
    'opt_arg': None,
    'test_unapply': False,
    'collapse': False,
    'unapply_extras': []},
  'insertunorderedlist' : {
    'opt_arg': None,
    'test_unapply': False,
    'collapse': False,
    'unapply_extras': []},
  'insertparagraph' : {
    'opt_arg': None,
    'test_unapply': True,
    'collapse': False,
    'unapply_extras': []},
  'italic' : {
    'opt_arg': None,
    'test_unapply': True,
    'collapse': False,
    'unapply_extras': [
      "['<i>', '</i>']",
      "['<EM>', '</EM>']",
      "['<span style=\"font-style: italic;\">', '</span>']"]},
  'justifycenter' : {
    'opt_arg': None,
    'test_unapply': False,
    'collapse': False,
    'unapply_extras': []},
  'justifyfull' : {
    'opt_arg': None,
    'test_unapply': False,
    'collapse': False,
    'unapply_extras': []},
  'justifyleft' : {
    'opt_arg': None,
    'test_unapply': False,
    'collapse': False,
    'unapply_extras': []},
  'justifyright' : {
    'opt_arg': None,
    'test_unapply': False,
    'collapse': False,
    'unapply_extras': []},
  'strikethrough' : {
    'opt_arg': None,
    'test_unapply': True,
    'collapse': False,
    'unapply_extras': [
      "['<strike>', '</strike>']",
      "['<s>', '</s>']",
      "['<del>', '</del>']",
      "['<span style=\"text-decoration: line-through;\">', '</span>']"]},
  'subscript' : {
    'opt_arg': None,
    'test_unapply': True,
    'collapse': False,
    'unapply_extras': [
      "['<sub>', '</sub>']",
      "['<span style=\"vertical-align: sub;\">', '</span>']"]},
  'superscript' : {
    'opt_arg': None,
    'test_unapply': True,
    'collapse': False,
    'unapply_extras': [
      "['<sup>', '</sup>']",
      "['<span style=\"vertical-align: super;\">', '</span>']"]},
  'underline' : {
    'opt_arg': None,
    'test_unapply': True,
    'collapse': False,
    'unapply_extras': [
      "['<u>', '</u>']",
      "['<span style=\"text-decoration: underline;\">', '</span>']"]}
};

@decorators.provide_csrf
def RunTests(request):
  """Runs the execCommand tests listed in the query string."""

  tests = request.GET.get('tests', None);
  if tests == None:
    tests = commands.keys()
  else:
    tests = tests.split(',')
  tests.sort()

  code = ''
  for test in tests:
    opt_arg = 'null'
    if commands[test]['opt_arg'] != None:
      opt_arg = "'%s'" % commands[test]['opt_arg']

    unapply = 'false'
    if commands[test]['test_unapply']:
      unapply = 'true'

    collapse = 'false'
    if commands[test]['collapse']:
      collapse = 'true'

    extra_unapply = '[' + ','.join(commands[test]['unapply_extras']) + ']'

    code += '        results.push(\'%s\' + \'=\' + testCommand(\'%s\', %s, %s, %s, %s));\n' % (test, test, unapply, opt_arg, collapse, extra_unapply)

  params = {
    'csrf_token': request.session.get('csrf_token'),
    'code': code,
  }
  return shortcuts.render_to_response('templates/tests.html', params)

def EditableIframe(request):

  params = {}
  return shortcuts.render_to_response('templates/editable.html', params)