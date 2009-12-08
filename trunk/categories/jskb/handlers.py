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

import logging
import re
from categories import all_test_sets
from categories.jskb import ecmascript_snippets
from categories.jskb import json
from models import user_agent
from base import util

from django import http

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
  return util.Render(
      request, 'templates/environment-checks.html',
      params={ 'snippets': json.to_json(ecmascript_snippets._SNIPPETS) },
      category=CATEGORY)


def Json(request):
  def html(s):
    return re.sub(r'<', '&lt;', re.sub('>', '&gt', re.sub(r'&', '&amp;', s)))

  def help_page(msg, stats_data):
    return (
      '<title>%(msg)s</title>'
      '<h1>%(msg)s</h1>'
      '<p><code>%(stats_data)s</code></p>'
      'Serve JSON mapping code snippets to results.\n'
      '<p>The JSON is the intersection of the (key, value) pairs accross all'
      ' user agents requested, so if Firefox 3 was requested then only'
      ' key/value pairs that are present in both Firefox 3.0, 3.1, etc.'
      ' will be present.\n'
      '<p>The extra <code>userAgent</code> key maps to the user agents'
      ' requested so that the output is self-describing.\n'
      '\n'
      '<p>CGI params<dl>\n'
      '  <dt><code>ot</code></dt>\n'
      '  <dd>The output mime-type</dd>\n'
      '  <dt><code>ua</code></dt>\n'
      '  <dd>The user agents requested</dd>\n'
      '</dl>\n'
      'E.g.,\n'
      '  <li><code>ua=Firefox%%2F3.0</code>\n'
      '  <li><code>ua=MSIE+6.0</code>\n'
      '  <li><code>ot=application%%2Fjson</code>\n'
      '  <li><code>ot=text%%2Fplain</code>\n'
      '</ul>'
      ) % { 'msg': html(msg), 'stats_data': html('%s' % stats_data) }

  if request.method != 'GET' and request.method != 'HEAD':
    return http.HttpResponseBadRequest(
        help_page('Bad method "%s"' % request.method), mimetype='text/html')
  user_agent_string = None
  out_type = 'text/plain'
  for key, value in request.GET.iteritems():
    if key == u'ua':
      user_agent_string = value
    elif key == u'ot' and value in ('text/plain', 'application/json'):
      out_type = value
    else:
      return http.HttpResponseBadRequest(
        help_page('Unknown CGI param "%s"' % key), mimetype='text/html')
      raise Exception()
  #ua = user_agent.UserAgent.factory(user_agent_string)
  #ua = user_agent.UserAgent.parse_to_string_list(user_agent_string)
  user_agent_strings = user_agent_string.split(',')
  tests = all_test_sets.GetTestSet(CATEGORY).tests
  stats_data = util.GetStatsData(CATEGORY, tests, user_agent_strings,
                                 ua_by_param=None, params_str=None,
                                 version_level='1')

  response = http.HttpResponse(mimetype='text/html')  # TODO: out_type
  response.write(help_page(
    ('TODO(mikesamuel): implement me. '
    'Requested useragent=%r' % (user_agent_strings)),
    stats_data))
  return response
