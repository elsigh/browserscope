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
from categories import all_test_sets
from base import decorators
from base import util


CATEGORY = 'richtext'


def About(request):
  """About page."""
  params = {
    'page_title': 'Rich Text Tests - About',
    'tests': all_test_sets.GetTestSet(CATEGORY).tests,
  }
  return util.Render(request, 'templates/about.html', params, CATEGORY)

@decorators.provide_csrf
def Test(request):
  params = {
    'page_title': 'Rich Text - Tests',
    'continue': request.GET.get('continue'),
    'autorun': request.GET.get('autorun'),
    'csrf_token': request.session.get('csrf_token'),
    'test_page': '/richtext/static/richtext.html'
  }
  return util.Render(request, util.TEST_DRIVER_TPL, params, CATEGORY)


def EditableIframe(request):

  params = {}
  return shortcuts.render_to_response('richtext/templates/editable.html', params)
