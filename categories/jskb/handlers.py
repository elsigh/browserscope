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

A set of JavaScript expressions that provide useful information to
code optimizers.
"""

__author__ = 'msamuel@google.com (Mike Samuel)'

import logging
import re
from categories import all_test_sets
from categories.jskb import ecmascript_snippets
from categories.jskb import json
from models import result_stats
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
      JavaScript code optimizers.

      <p>Optimizers can get output in a JSON format at
      <a href=\"json?ua=Chrome\"><tt>json?ua=&hellip;</tt></a>.</p>

      <p>Scores on the test summary page are not meant to be a measure
      of the quality of a browser, but to indicate how many features
      are available as a predictor of how much redundant code might be
      eliminated on that browser.</p>
      """)
  return util.About(request, CATEGORY, overview=overview)


def EnvironmentChecks(request):
  """The main test page."""
  return util.Render(
      request, 'templates/environment-checks.html',
      params={ 'snippets': json.to_json(ecmascript_snippets.SNIPPET_GROUPS) },
      category=CATEGORY)

  for group in ecmascript_snippets:
    for snippet in group[1:]:  # group header is item 0
      snippet_keys.add(snippet[ecmascript_snippets.NAME])


def Json(request):
  def html(s):
    return re.sub(r'<', '&lt;', re.sub('>', '&gt', re.sub(r'&', '&amp;', s)))

  def help_page(msg):
    return (
      '<title>%(msg)s</title>'
      '<h1>%(msg)s</h1>'
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
      '  <li><code>ua=Firefox+3.5</code>\n'
      '  <li><code>ua=MSIE+6.0</code>\n'
      '  <li><code>ot=application%%2Fjson</code>\n'
      '  <li><code>ot=text%%2Fplain</code>\n'
      '</ul>'
      ) % { 'msg': html(msg) }

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

  if user_agent_string is None:
      return http.HttpResponseBadRequest(
          help_page('Please specify useragent'), mimetype='text/html')

  user_agent_strings = user_agent_string.split(',')
  test_set = all_test_sets.GetTestSet(CATEGORY)
  test_keys = [t.key for t in test_set.tests]
  stats_data = result_stats.CategoryStatsManager.GetStats(
      test_set=test_set, browsers=user_agent_strings, test_keys=test_keys)
  del stats_data['total_runs']

  # Keep only those items that are common across all the user agents requested.
  combined = None
  for browser_stats in stats_data.values():
    stats = browser_stats['results']
    if combined is None:
      combined = dict([(k, v.get('display')) for (k, v) in stats.iteritems()
                       if k in ecmascript_snippets.SNIPPET_NAMES])
    else:
      old_combined = combined
      combined = dict([(k, v.get('display')) for (k, v) in stats.iteritems()
                       if (k in old_combined
                           and old_combined.get(k) == v.get('display'))])
  if combined is None: combined = {}
  result = [(ecmascript_snippets.with_name(k)[ecmascript_snippets.CODE], v)
            for (k, v) in combined.iteritems() if v is not None]
  result.append(('*userAgent*', json.to_json(stats_data.keys())))

  def check_json_value(v):
    if v == 'throw':
      return '{ "throw": true }'
    return v
  response = http.HttpResponse(mimetype=out_type)
  response.write('{%s}' % ',\n'.join(
      [('%s:%s' % (json.to_json(k), check_json_value(v))) for (k, v) in result]))
  return response
