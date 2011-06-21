#!/usr/bin/python2.5
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

import re

from categories import all_test_sets
from base import decorators
from base import util

from django import http

CATEGORY = 'network'

TEST_PAGE = '/%s/frameset' % CATEGORY

#RESOURCE_CGI_BASE = 'cuzillion.com/bin/resource.cgi'
RESOURCE_CGI_BASE = 'cgi.browserscope.net/cgi-bin/resource.cgi'
#RESOURCE_CGI_BASE = 'resource-cgi-hirep.appspot.com'

RESOURCE_CGI = '1.%s' % RESOURCE_CGI_BASE
RESOURCE_CGI2 = '2.%s' % RESOURCE_CGI_BASE

TRAILER_RESOURCE_CGI = 'cgi.browserscope.org/cgi-bin/nph-trailer.cgi'

def About(request):
  """About page."""
  return util.About(request, CATEGORY)


def Faq(request):
  """Network Performance FAQ"""

  params = {
    'page_title': 'Performance FAQ',
    'resource_cgi_base': RESOURCE_CGI_BASE,
    'resource_cgi': RESOURCE_CGI,
    'resource_cgi2': RESOURCE_CGI2,
  }
  return util.Render(request, 'templates/faq.html', params, CATEGORY)


def CacheExpires(request):
  """Network Performance Cache Expires Test"""

  params = {
    'page_title': 'Performance Cache Expires Test',
    'resource_cgi_base': RESOURCE_CGI_BASE,
    'resource_cgi': RESOURCE_CGI,
    'resource_cgi2': RESOURCE_CGI2,
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
    'resource_cgi_base': RESOURCE_CGI_BASE,
    'resource_cgi': RESOURCE_CGI,
    'resource_cgi2': RESOURCE_CGI2,
  }
  return util.Render(request, 'templates/tests/cache-expires2.html', params,
                     CATEGORY)


def CacheRedirects(request):
  """Network Performance Cache Redirects Test"""

  params = {
    'page_title': 'Performance Cache Redirects Test',
    'resource_cgi_base': RESOURCE_CGI_BASE,
    'resource_cgi': RESOURCE_CGI,
    'resource_cgi2': RESOURCE_CGI2,
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
    'resource_cgi_base': RESOURCE_CGI_BASE,
    'resource_cgi': RESOURCE_CGI,
    'resource_cgi2': RESOURCE_CGI2,
    'prevt': prevt,
  }
  return util.Render(request, 'templates/tests/cache-redirects2.html', params,
                     CATEGORY)


def CacheResourceRedirects(request):
  """Network Performance Cache Resource Redirects Test"""

  params = {
    'page_title': 'Performance Cache Resource Redirects Test',
    'resource_cgi_base': RESOURCE_CGI_BASE,
    'resource_cgi': RESOURCE_CGI,
    'resource_cgi2': RESOURCE_CGI2,
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
    'resource_cgi_base': RESOURCE_CGI_BASE,
    'resource_cgi': RESOURCE_CGI,
    'resource_cgi2': RESOURCE_CGI2,
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
    'resource_cgi_base': RESOURCE_CGI_BASE,
    'resource_cgi': RESOURCE_CGI,
    'resource_cgi2': RESOURCE_CGI2,
    'sleep': sleep,
    'latency': latency,
  }
  return util.Render(request, 'templates/tests/connections-per-hostname.html',
                     params, CATEGORY)


def DataUrls(request):
  """Network Performance Data URLs Test"""

  params = {
    'page_title': 'Performance Data URLs Test',
    'resource_cgi_base': RESOURCE_CGI_BASE,
    'resource_cgi': RESOURCE_CGI,
    'resource_cgi2': RESOURCE_CGI2,
  }
  return util.Render(request, 'templates/tests/data-urls.html', params,
                     CATEGORY)


def Gzip(request):
  """Network Performance, CATEGORY Gzip Test"""

  # HTTP_ACCEPT_ENCODING is filtered out by App Engine because it
  # handles compression for applications.

  params = {
    'page_title': 'Performance Gzip Test',
    'resource_cgi_base': RESOURCE_CGI_BASE,
    'resource_cgi': RESOURCE_CGI,
    'resource_cgi2': RESOURCE_CGI2,
  }
  return util.Render(request, 'templates/tests/gzip.html', params, CATEGORY)


def InlineScriptAfterStylesheet(request):
  """Network Performance Inline Script After Stylesheet Test"""

  params = {
    'page_title': 'Performance Inline Script After Stylesheet Test',
    'resource_cgi_base': RESOURCE_CGI_BASE,
    'resource_cgi': RESOURCE_CGI,
    'resource_cgi2': RESOURCE_CGI2,
  }
  return util.Render(request,
                     'templates/tests/inline-script-after-stylesheet.html',
                     params, CATEGORY)


def Latency(request):
  """Network Performance Latency Measurement"""

  params = {
    'page_title': 'Performance Latency Measurement',
    'resource_cgi_base': RESOURCE_CGI_BASE,
    'resource_cgi': RESOURCE_CGI,
    'resource_cgi2': RESOURCE_CGI2,
  }
  return util.Render(request, 'templates/tests/latency.html', params, CATEGORY)


def LinkPrefetch(request):
  """Network Performance Link Prefetch Test"""

  params = {
    'page_title': 'Performance Link Prefetch Test',
    'resource_cgi_base': RESOURCE_CGI_BASE,
    'resource_cgi': RESOURCE_CGI,
    'resource_cgi2': RESOURCE_CGI2,
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
    'resource_cgi_base': RESOURCE_CGI_BASE,
    'resource_cgi': RESOURCE_CGI,
    'resource_cgi2': RESOURCE_CGI2,
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
    'resource_cgi_base': RESOURCE_CGI_BASE,
    'resource_cgi': RESOURCE_CGI,
    'resource_cgi2': RESOURCE_CGI2,
    'sleep': sleep
  }
  return util.Render(request, 'templates/tests/max-connections.html', params,
                     CATEGORY)


def ScriptsBlock(request):
  """Network Performance Scripts Block Test"""

  params = {
    'page_title': 'Performance Scripts Block Test',
    'resource_cgi_base': RESOURCE_CGI_BASE,
    'resource_cgi': RESOURCE_CGI,
    'resource_cgi2': RESOURCE_CGI2,
  }
  return util.Render(request, 'templates/tests/scripts-block.html', params,
                     CATEGORY)


def ScriptsBlockScripts(request):
  """Network Performance Scripts Block Scripts Test"""

  params = {
    'page_title': 'Performance Scripts Block Scripts Test',
    'resource_cgi_base': RESOURCE_CGI_BASE,
    'resource_cgi': RESOURCE_CGI,
    'resource_cgi2': RESOURCE_CGI2,
  }
  return util.Render(request, 'templates/tests/scripts-block-scripts.html', params,
                     CATEGORY)


def ScriptsBlockStylesheets(request):
  """Network Performance Scripts Block Stylesheets Test"""

  params = {
    'page_title': 'Performance Scripts Block Stylesheets Test',
    'resource_cgi_base': RESOURCE_CGI_BASE,
    'resource_cgi': RESOURCE_CGI,
    'resource_cgi2': RESOURCE_CGI2,
  }
  return util.Render(request, 'templates/tests/scripts-block-stylesheets.html', params,
                     CATEGORY)


def ScriptsBlockImages(request):
  """Network Performance Scripts Block Images Test"""

  params = {
    'page_title': 'Performance Scripts Block Images Test',
    'resource_cgi_base': RESOURCE_CGI_BASE,
    'resource_cgi': RESOURCE_CGI,
    'resource_cgi2': RESOURCE_CGI2,
  }
  return util.Render(request, 'templates/tests/scripts-block-images.html', params,
                     CATEGORY)


def ScriptsBlockIframes(request):
  """Network Performance Scripts Block Iframes Test"""

  params = {
    'page_title': 'Performance Scripts Block Iframes Test',
    'resource_cgi_base': RESOURCE_CGI_BASE,
    'resource_cgi': RESOURCE_CGI,
    'resource_cgi2': RESOURCE_CGI2,
  }
  return util.Render(request, 'templates/tests/scripts-block-iframes.html', params,
                     CATEGORY)


def ScriptsAsync(request):
  """Network Performance Scripts Support Async"""

  params = {
    'page_title': 'Performance Scripts Support Async Test',
    'resource_cgi_base': RESOURCE_CGI_BASE,
    'resource_cgi': RESOURCE_CGI,
    'resource_cgi2': RESOURCE_CGI2,
  }
  return util.Render(request, 'templates/tests/scripts-async.html', params,
                     CATEGORY)


def StylesheetsBlock(request):
  """Network Performance Stylesheets Block Test"""

  params = {
    'page_title': 'Performance Stylesheets Block Test',
    'resource_cgi_base': RESOURCE_CGI_BASE,
    'resource_cgi': RESOURCE_CGI,
    'resource_cgi2': RESOURCE_CGI2,
  }
  return util.Render(request, 'templates/tests/stylesheets-block.html', params,
                     CATEGORY)


def Trailer(request):
  """Network Performance Headers in Trailer Test"""

  params = {
    'page_title': 'Performance Headers in Trailer Test',
    'resource_cgi': TRAILER_RESOURCE_CGI,
  }
  return util.Render(request, 'templates/tests/trailer.html', params,
                     CATEGORY)

