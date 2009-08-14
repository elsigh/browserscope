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

"""Handlers for JS Benchmark Tests.

Example beacon request:
  http://localhost:8080/beacon?category=v8&results=Richards=1748,DeltaBlue=2046,
  Crypto=1470,RayTrace=2262,EarleyBoyer=2982,RegExp=725,Splay=3330,Overall=1888
"""

__author__ = 'jacobm@google.com (Jacob Moon)'

import time

from categories import all_test_sets
from base import decorators
from base import util

from django import http

CATEGORY = 'v8'


def Render(request, template_file, params):
  """Render V8 Benchmark test pages."""

  params['epoch'] = int(time.time())
  return util.Render(request, template_file, params, CATEGORY)

def About(request):
  """About page."""
  params = {
    'page_title': 'V8 Benchmark Suite Tests - About',
    'tests': all_test_sets.GetTestSet(CATEGORY).tests,
  }
  return Render(request, 'templates/about.html', params)

@decorators.provide_csrf
def Test(request):
  """V8 Benchmark Performance Tests"""

  params = {
    'page_title': 'V8 Benchmark Suite Tests - Test',
    'continue': request.GET.get('continue'),
    'autorun': request.GET.get('autorun'),
    'testurl': request.GET.get('testurl'),
    'csrf_token': request.session.get('csrf_token'),
  }
  return Render(request, 'templates/test.html', params)
