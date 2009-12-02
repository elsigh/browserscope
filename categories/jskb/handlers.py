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

"""JavaScript Knowledge-Base.

A set of JavaScript expressions that provide useful information to code optimizers.
"""

__author__ = 'msamuel@google.com (Mike Samuel)'

import re
#from categories import all_test_sets
from categories.jskb import ecmascript_snippets
#from base import decorators
from base import util

from django import http
#from django.template import Context, loader


CATEGORY = 'jskb'

def About(request):
  """About page."""
  overview = re.sub(
      r'\r\n +', ' ',
      """
      This page contains side-effect free JavaScript expressions
      that expose information about a browser that can be useful to
      JavaScript code optimizers.""")
  return util.About(request, CATEGORY, overview=overview)


def EnvironmentChecks(request):
  """The main test page."""
  return util.Render(request, 'templates/environment-checks.html',
                     params={ 'snippets': repr(ecmascript_snippets._SNIPPETS) },
                     category=CATEGORY)


def Json(request):
  return http.HttpResponse('yo')  # TODO
