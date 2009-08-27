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
from base import decorators

@decorators.provide_csrf
def RunTests(request):

  params = {
    'csrf_token': request.session.get('csrf_token'),
  }
  return shortcuts.render_to_response('richtext/templates/tests.html', params)

def EditableIframe(request):

  params = {}
  return shortcuts.render_to_response('richtext/templates/editable.html', params)

@decorators.provide_csrf
def Apply(request):

  params = {
    'csrf_token': request.session.get('csrf_token'),
  }
  return shortcuts.render_to_response('richtext/templates/apply.html', params)

@decorators.provide_csrf
def Unapply(request):

  params = {
    'csrf_token': request.session.get('csrf_token'),
  }
  return shortcuts.render_to_response('richtext/templates/unapply.html', params)
  
@decorators.provide_csrf
def QueryCommand(request):
  params = {
    'csrf_token': request.session.get('csrf_token'),
  }
  return shortcuts.render_to_response('richtext/templates/query.html', params)
  
@decorators.provide_csrf
def Change(request):
  params = {
    'csrf_token': request.session.get('csrf_token'),
  }
  return shortcuts.render_to_response('richtext/templates/change.html', params)
