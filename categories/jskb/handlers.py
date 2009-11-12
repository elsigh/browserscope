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


CATEGORY = 'jskb'

def About(request):
  """About page."""
  overview = """This page contains a suite of security tests that measure
    whether the browser supports JavaScript APIs that allow safe
    interactions between sites, and whether it follows industry
    best practices for blocking harmful interactions between sites.
    The initial set of tests were contributed by
    <a href="http://www.adambarth.com/">Adam Barth</a>,
    <a href="http://www.collinjackson.com/">Collin Jackson</a>,
    and <a href="http://www.google.com/profiles/meacer">Mustafa Acer</a>."""
  return util.About(request, CATEGORY, overview=overview)


def EnvironmentChecks(request):
  """The main test page."""
  return util.Render(request, 'templates/environment-checks.html', params={},
                     category=CATEGORY)


def Json(request):
  return http.HttpResponse('yo')
