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

"""Handlers for Network Tests.

Example beacon request:
  http://localhost:8080/beacon?category=network&results=latency=123,hostconn=6,
     maxconn=29,parscript=0,parsheet=1,parcssjs=0,cacheexp=1,cacheredir=0,
     cacheresredir=0,prefetch=1,gzip=1,du=1
"""

__author__ = 'steve@souders.com (Steve Souders)'


from categories import all_test_sets
from base import decorators
from base import util

from django import http

CATEGORY = 'network'


def About(request):
  """About page."""
  params = {
    'page_title': 'Network Tests - About',
    'tests': all_test_sets.GetTestSet(CATEGORY).tests,
  }
  return util.Render(request, 'templates/about.html', params, CATEGORY)


@decorators.provide_csrf
def Test(request):
  """Network Performance Tests"""

  test_page = ('frameset?autorun=%s&testurl=%s' %
               (request.GET.get('autorun', '1'),
                request.GET.get('testurl', '')))
  params = {
    'autorun': request.GET.get('autorun', ''),
    'continue': request.GET.get('continue', ''),
    'test_page': test_page,
    'csrf_token': request.session.get('csrf_token'),
  }
  return util.Render(request, util.TEST_DRIVER_TPL, params, CATEGORY)


def Frameset(request):
  params = {
    'page_title': 'Network Performance - Tests',
    'autorun': request.GET.get('autorun', 1),
    'testurl': request.GET.get('testurl', ''),
  }
  return util.Render(request, 'templates/test.html', params, CATEGORY)


def TestDriver(request):
  """Network Performance Test Driver"""
  tests = all_test_sets.GetTestSet(CATEGORY).tests
  # tests = [tests[0]]
  params = {
    'page_title': 'Performance Test Driver',
    'tests': tests,
    'autorun': request.GET.get('autorun'),
    'testurl': request.GET.get('testurl'),
  }
  return util.Render(request, 'templates/testdriver.html', params, CATEGORY)


def StatsTable(request):
  params = {
    'stats_table': util.GetStats(request, CATEGORY)
  }
  return util.Render(request, 'templates/stats_table.html', params, CATEGORY)


def Faq(request):
  """Network Performance FAQ"""

  params = {
    'page_title': 'Performance FAQ',
  }
  return util.Render(request, 'templates/faq.html', params, CATEGORY)


def CacheExpires(request):
  """Network Performance Cache Expires Test"""

  params = {
    'page_title': 'Performance Cache Expires Test',
  }
  return util.Render(request, 'templates/tests/cache-expires.html', params,
                     CATEGORY)


def CacheExpires2(request):
  """Network Performance Cache Expires Test"""

  if 't' in request.GET:
    prevt = int(request.GET.get('t'))
  else:
    prevt = 128
  # CVSNO - If prevt wasn't found, there's an error

  params = {
    'page_title': 'Performance Cache Expires Test',
    'prevt': prevt,
  }
  return util.Render(request, 'templates/tests/cache-expires2.html', params,
                     CATEGORY)


def CacheRedirects(request):
  """Network Performance Cache Redirects Test"""

  params = {
    'page_title': 'Performance Cache Redirects Test',
  }
  return util.Render(request, 'templates/tests/cache-redirects.html', params,
                     CATEGORY)


def CacheRedirects2(request):
  """Network Performance Cache Redirects Test"""

  if 't' in request.GET:
    prevt = int(request.GET.get('t'))
  else:
    prevt = 128
  # CVSNO - If prevt wasn't found, there's an error

  params = {
    'page_title': 'Performance Cache Redirects Test',
    'prevt': prevt,
  }
  return util.Render(request, 'templates/tests/cache-redirects2.html', params,
                     CATEGORY)


def CacheResourceRedirects(request):
  """Network Performance Cache Resource Redirects Test"""

  params = {
    'page_title': 'Performance Cache Resource Redirects Test',
  }
  return util.Render(request, 'templates/tests/cache-resource-redirects.html',
                     params, CATEGORY)


def CacheResourceRedirects2(request):
  """Network Performance Cache Resource Redirects Test"""

  if 't' in request.GET:
    prevt = int(request.GET.get('t'))
  else:
    prevt = 128
  # CVSNO - If prevt wasn't found, there's an error

  params = {
    'page_title': 'Performance Cache Resource Redirects Test',
    'prevt': prevt,
  }
  return util.Render(request, 'templates/tests/cache-resource-redirects2.html',
                     params, CATEGORY)


def ConnectionsPerHostname(request):
  """Network Performance Connections per Hostname Test"""

  latency = request.COOKIES.get('latency', 6)
  sleep = min(9, int(2 * round((int(latency) + 500.0) / 1000.0)))

  params = {
    'page_title': 'Performance Connections per Hostname Test',
    'sleep': sleep,
    'latency': latency,
  }
  return util.Render(request, 'templates/tests/connections-per-hostname.html',
                     params, CATEGORY)


def DataUrls(request):
  """Network Performance Data URLs Test"""

  params = {
    'page_title': 'Performance Data URLs Test',
  }
  return util.Render(request, 'templates/tests/data-urls.html', params,
                     CATEGORY)


def Gzip(request):
  """Network Performance, CATEGORY Gzip Test"""

  # HTTP_ACCEPT_ENCODING is filtered out by App Engine because it
  # handles compression for applications.

  params = {
    'page_title': 'Performance Gzip Test',
  }
  return util.Render(request, 'templates/tests/gzip.html', params, CATEGORY)


def InlineScriptAfterStylesheet(request):
  """Network Performance Inline Script After Stylesheet Test"""

  params = {
    'page_title': 'Performance Inline Script After Stylesheet Test',
  }
  return util.Render(request,
                     'templates/tests/inline-script-after-stylesheet.html',
                     params, CATEGORY)


def Latency(request):
  """Network Performance Latency Measurement"""

  params = {
    'page_title': 'Performance Latency Measurement',
  }
  return util.Render(request, 'templates/tests/latency.html', params, CATEGORY)


def LinkPrefetch(request):
  """Network Performance Link Prefetch Test"""

  params = {
    'page_title': 'Performance Link Prefetch Test',
  }
  return util.Render(request, 'templates/tests/link-prefetch.html', params,
                     CATEGORY)


def LinkPrefetch2(request):
  """Network Performance Link Prefetch Test"""

  if 't' in request.GET:
    prevt = int(request.GET.get('t'))
  else:
    prevt = 128
  # CVSNO - If prevt wasn't found, there's an error

  params = {
    'page_title': 'Performance Link Prefetch Test',
    'prevt': prevt,
  }
  return util.Render(request, 'templates/tests/link-prefetch2.html', params,
                     CATEGORY)


def MaxConnections(request):
  """Network Performance Max Connections Test"""

  latency = request.COOKIES.get('latency', 9)
  sleep = max(6, min(9, int(4 * round((int(latency) + 500.0) / 1000.0))))

  params = {
    'page_title': 'Performance Max Connections Test',
    'sleep': sleep
  }
  return util.Render(request, 'templates/tests/max-connections.html', params,
                     CATEGORY)


def ScriptsBlock(request):
  """Network Performance Scripts Block Test"""

  params = {
    'page_title': 'Performance Scripts Block Test',
  }
  return util.Render(request, 'templates/tests/scripts-block.html', params,
                     CATEGORY)


def StylesheetsBlock(request):
  """Network Performance Stylesheets Block Test"""

  params = {
    'page_title': 'Performance Stylesheets Block Test',
  }
  return util.Render(request, 'templates/tests/stylesheets-block.html', params,
                     CATEGORY)


def Admin(request):
  """Network Performance Admin Tools"""

  params = {
    'page_title': 'Performance Admin Tools',
  }
  return util.Render(request, 'templates/admin/admin.html', params, CATEGORY)


def ConfirmUa(request):
  """Network Performance Confirm User-Agents"""

  params = {
    'page_title': 'Performance Confirm User-Agents',
  }
  return util.Render(request, 'templates/admin/confirm-ua.html')


def Stats(request):
  """Network Performance Stats"""

  params = {
    'page_title': 'Performance Stats',
    'epoch': epochTime(),
  }
  return util.Render(request, 'templates/admin/stats.html', params, CATEGORY)
