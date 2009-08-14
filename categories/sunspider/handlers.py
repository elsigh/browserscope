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

"""Handlers for SunSpider Benchmark Tests.

Example beacon request:
  http://localhost:8080/beacon?category=sunspider&results=3d=612,access=513,
  bitops=183,controlflow=14,crypto=482,date=464,math=558,regexp=71,string=748,
  total=3645
"""

__author__ = 'jacobm@google.com (Jacob Moon)'

import time

from categories import all_test_sets
from base import decorators
from base import util

from django import http

CATEGORY = 'sunspider'


def Render(request, template_file, params):
  """Render SunSpider Benchmark test pages."""

  params['epoch'] = int(time.time())
  return util.Render(request, template_file, params, CATEGORY)

def About(request):
  """About page."""
  params = {
    'page_title': 'SunSpider JavaScript Benchmark - About',
    'tests': all_test_sets.GetTestSet(CATEGORY).tests,
  }
  return Render(request, 'templates/about.html', params)

@decorators.provide_csrf
def Test(request):
  """SunSpider Benchmark Performance Tests"""

  params = {
    'page_title': 'SunSpider JavaScript Benchmark - Test',
    'continue': request.GET.get('continue'),
    'autorun': request.GET.get('autorun'),
    'testurl': request.GET.get('testurl'),
    'csrf_token': request.session.get('csrf_token'),
  }
  return Render(request, 'templates/test.html', params)
