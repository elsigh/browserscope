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

"""Handlers for the Selectors API Tests."""

__author__ = 'elsigh@google.com (Lindsey Simon)'


from categories import all_test_sets
from base import decorators
from base import util

from django import http
from django.template import Context, loader


CATEGORY = 'selectors'

def About(request):
  """About page."""
  params = {
    'page_title': 'Selectors API Test - About',
    'tests': all_test_sets.GetTestSet(CATEGORY).tests,
  }
  return util.Render(request, 'templates/about.html', params, CATEGORY)

@decorators.provide_csrf
def Test(request):
  """Selectors API Tests"""

  params = {
    'page_title': 'Selectors API - Test',
    'continue': request.GET.get('continue'),
    'autorun': request.GET.get('autorun'),
    'csrf_token': request.session.get('csrf_token'),
  }
  return util.Render(request, 'templates/test.html', params, CATEGORY)


