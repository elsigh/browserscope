#!/usr/bin/python
#
# Copyright 2009 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Generates static stats tables HTML files."""

_author__ = 'elsigh@google.com (Lindsey Simon)'

import logging
import os
import sys
import urllib2

sys.path.extend(['..', '../../..'])
import settings

BROWSER_NAV = [
  # version_level, label
  ('top', 'Top Browsers'),
  ('0', 'Browser Families'),
  ('1', 'Major Versions'),
  ('2', 'Minor Versions'),
  ('3', 'All Versions')
]

logging.getLogger().setLevel(logging.INFO)
logging.debug('categories: %s' % settings.CATEGORIES)

HOST = 'elsigh.latest.ua-profiler.appspot.com'

for category in settings.CATEGORIES:
  for family in BROWSER_NAV:
    version_level = family[0]
    url = 'http://%s/?category=%s&v=%s&xhr=1' % (HOST, category, version_level)
    logging.info('Opening URL: %s' % url)
    try:
      response = urllib2.urlopen(url)
    except urllib2.HTTPError, e:
      print 'The server couldn\'t fulfill the request.'
      print 'Error code: ', e.code
    except urllib2.URLError, e:
      print 'We failed to reach a server.'
      print 'Reason: ', e.reason
    else:
      html = response.read()
      print html
    sys.exit(0)
