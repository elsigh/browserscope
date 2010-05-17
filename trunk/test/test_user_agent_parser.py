#!/usr/bin/python2.5
#
# Copyright 2008 Google Inc.
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

"""User Agent Parser Unit Tests."""

__author__ = 'slamm@google.com (Stephen Lamm)'

import unittest

from models import user_agent_parser


CHROME_UA_STRING = (
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/530.1 '
    '(KHTML, like Gecko) Chrome/2.0.169.1 Safari/530.1')

TEST_STRINGS = (
    # ((family, v1, v2, v3), user_agent_string)
    (('Firefox (Shiretoko)', '3', '5', '1pre'),
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.1pre) '
     'Gecko/20090717 Ubuntu/9.04 (jaunty) Shiretoko/3.5.1pre', {}),
    (('Konqueror', '4', '3', '1'),
     'Mozilla/5.0 (X11; U; Linux; de-DE) AppleWebKit/527  '
     '(KHTML, like Gecko, Safari/419.3) konqueror/4.3.1,gzip(gfe)', {}),
    (('Other', None, None, None),
     'SomethingWeNeverKnewExisted', {}),
    (('Chrome Frame (Sleipnir 2)', '2', '0', '169'),
     'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; '
     'chromeframe; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR '
     '3.5.30729; Sleipnir 2.8.5),gzip(gfe),gzip(gfe)',
     {'js_user_agent_string': CHROME_UA_STRING}),
    (('Chrome Frame (IE 8)', '2', '0', '169'),
     'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; '
     'chromeframe; SLCC1; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR '
     '3.0.30729),gzip(gfe),gzip(gfe)',
     {'js_user_agent_string': CHROME_UA_STRING}),
    # Chrome Frame installed but not enabled
    (('IE', '8', '0', None),
     'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6; '
     'chromeframe; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR '
     '3.0.04506.648; .NET CLR 3.5.21022; .NET CLR 3.0.4506.2152; .NET CLR '
     '3.5.30729),gzip(gfe),gzip(gfe)',
     {'js_user_agent_string': 'Mozilla/4.0 (compatible; MSIE 8.0; '
      'Windows NT 5.1; Trident/4.0; chromeframe; .NET CLR 2.0.50727; '
      '.NET CLR 1.1.4322; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; '
      '.NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'}),
    (('IE Platform Preview', '9', '0', None),
     'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6; '
     '.NET CLR 2.0.50727; .NET CLR 1.1.4322),gzip(gfe),gzip(gfe)',
     {'js_user_agent_string': 'Mozilla/4.0 (compatible; MSIE 8.0; '
      'Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 1.1.4322)',
      'js_document_mode': '9'}),
    (('iPad', '4', '0', '4'),
     'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) Apple '
     'WebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B367 '
     'Safari/531.21.10', {}),
    (('Midori', '0', '2', None),
     'Midori/0.2 (X11; Linux; U; en-us) WebKit/531.2 ,gzip(gfe),gzip(gfe)',
     {}),
    (('MozillaDeveloperPreview', '3', '7', 'a1'),
     'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.3a1) '
     'Gecko/20100208 MozillaDeveloperPreview/3.7a1 '
     '(.NET CLR 3.5.30729),gzip(gfe),gzip(gfe)', {}),
    (('Opera', '10', '53', None),
      'Opera/9.80 (Windows NT 5.1; U; ru) Presto/2.5.24 Version/10.53',
      {}),
    (('Opera Mobile', '10', '00', None),
     'Opera/9.80 (S60; SymbOS; Opera Mobi/275; U; es-ES) '
     'Presto/2.4.13 Version/10.00,gzip(gfe),gzip(gfe)', {}),

    )


class ParseTest(unittest.TestCase):

  def testStrings(self):
    for (family, v1, v2, v3), user_agent_string, kwds in TEST_STRINGS:
      self.assertEqual((family, v1, v2, v3),
                       user_agent_parser.Parse(user_agent_string, **kwds))


class GetFiltersTest(unittest.TestCase):
  def testGetFiltersNoMatchesGiveEmptyDict(self):
    user_agent_string = 'foo'
    filters = user_agent_parser.GetFilters(
        user_agent_string, js_user_agent_string=None, js_document_mode=None)
    self.assertEqual({}, filters)

  def testGetFiltersJsUaPassedThrough(self):
    user_agent_string = 'foo'
    filters = user_agent_parser.GetFilters(
        user_agent_string, js_user_agent_string='bar', js_document_mode=None)
    self.assertEqual({'js_user_agent_string': 'bar'}, filters)

  def testGetFiltersDocumentModeForIe8Ignored(self):
    user_agent_string = ('Mozilla/4.0 (compatible; MSIE 8.0; '
      'Windows NT 5.1; Trident/4.0; GTB6; .NET CLR 2.0.50727; '
      '.NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)')
    filters = user_agent_parser.GetFilters(
        user_agent_string, js_user_agent_string='bar', js_document_mode='8')
    self.assertEqual({'js_user_agent_string': 'bar'}, filters)

  def testGetFiltersDocumentModeForIe9PlatformPreviewReturned(self):
    user_agent_string = ('Mozilla/4.0 (compatible; MSIE 8.0; '
      'Windows NT 5.1; Trident/4.0; GTB6; .NET CLR 2.0.50727; '
      '.NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)')
    filters = user_agent_parser.GetFilters(
        user_agent_string, js_user_agent_string='bar', js_document_mode='9')
    self.assertEqual({'js_user_agent_string': 'bar',
                      'js_document_mode': '9'}, filters)
