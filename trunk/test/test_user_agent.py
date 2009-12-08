#!/usr/bin/python2.4
#
# Copyright 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the 'License')
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""User Agent Unit Tests."""

__author__ = 'elsigh@google.com (Lindsey Simon)'

import logging
import re
import unittest

from google.appengine.ext import db
from models.user_agent import *

class UserAgentTest(unittest.TestCase):

  def test_factory(self):
    """Creates two instances of a UserAgent with our factory function
    and test that they're in fact the same entity, ensuring uniqueness."""
    ua_string = ('Mozilla/5.0 (X11 U Linux armv6l de-DE rv:1.9a6pre) '
                 'Gecko/20080606 '
                 'Firefox/3.0a1 Tablet browser 0.3.7 '
                 'RX-34+RX-44+RX-48_DIABLO_4.2008.23-14')
    ua1 = UserAgent.factory(ua_string)
    self.assertNotEqual(ua1, None)

    ua2 = UserAgent.factory(ua_string)
    self.assertEqual(ua1.key(), ua2.key())

    query = db.Query(UserAgent)
    query.filter('string =', ua_string)
    results = query.fetch(2)
    self.assertEqual(1, len(results))


  def test_parse(self):

    ua_string = ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.1pre) '
                 'Gecko/20090717 Ubuntu/9.04 (jaunty) Shiretoko/3.5.1pre')
    self.assertEqual(('Firefox (Shiretoko)', '3', '5', '1pre'),
                     UserAgent.parse(ua_string))

    ua_string = ('Mozilla/5.0 (X11; U; Linux; de-DE) AppleWebKit/527  '
                 '(KHTML, like Gecko, Safari/419.3) '
                 'konqueror/4.3.1,gzip(gfe),gzip(gfe)')
    self.assertEqual(('Konqueror', '4', '3', '1'), UserAgent.parse(ua_string))


    ua_string = 'SomethingWeNeverKnewExisted'
    self.assertEqual(('Other', None, None, None), UserAgent.parse(ua_string))


  def test_get_string_list(self):
    ua_string = ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) '
                 'Gecko/2009011912 Firefox/3.0.6')
    ua = UserAgent.factory(ua_string)
    self.assertEqual(['Firefox', 'Firefox 3', 'Firefox 3.0', 'Firefox 3.0.6'],
                     ua.get_string_list())

    ua_string = ('Mozilla/4.0 '
                 '(compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; '
                 '.NET CLR 2.0.50727; .NET CLR 1.1.4322; '
                 '.NET CLR 3.0.04506.648; .NET CLR 3.5.21022)')
    ua = UserAgent.factory(ua_string)
    self.assertEqual(['IE', 'IE 8', 'IE 8.0'],
                     ua.get_string_list())

    ua_string = ('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) '
                 'AppleWebKit/530.1 (KHTML, like Gecko) '
                 'Chrome/2.0.169.1 Safari/530.1')
    ua = UserAgent.factory(ua_string)
    self.assertEqual(['Chrome', 'Chrome 2', 'Chrome 2.0', 'Chrome 2.0.169'],
                     ua.get_string_list())


  def test_pretty_print(self):
    self.assertEqual('MicroB 3',
                     UserAgent.pretty_print('MicroB', '3', None, None))

    self.assertEqual('Firefox 3.0.6',
                     UserAgent.pretty_print('Firefox', '3', '0', '6'))

    self.assertEqual('Other',
                     UserAgent.pretty_print('Other', None, None, None))


  def test_parse_to_string_list(self):
    self.assertEqual([], UserAgent.parse_to_string_list(''))

    self.assertEqual(['Opera'],
                     UserAgent.parse_to_string_list('Opera'))

    self.assertEqual(['IE', 'IE 8'],
                     UserAgent.parse_to_string_list('IE 8'))

    self.assertEqual(['Firefox', 'Firefox 3', 'Firefox 3.1'],
                     UserAgent.parse_to_string_list('Firefox 3.1'))

    self.assertEqual(['Chrome', 'Chrome 5', 'Chrome 5.4', 'Chrome 5.4.3'],
                     UserAgent.parse_to_string_list('Chrome 5.4.3'))

    self.assertEqual(
        ['Safari', 'Safari 100', 'Safari 100.33', 'Safari 100.33preA4'],
        UserAgent.parse_to_string_list('Safari 100.33preA4'))



class UserAgentGroupTest(unittest.TestCase):

  def setUp(self):
    for version_level, _ in BROWSER_NAV:
      UserAgentGroup.ClearMemcache(version_level)

    user_agent_strings = [
        ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) '
        'Gecko/2009011912 Firefox/2.5.1'),
        ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) '
        'Gecko/2009011912 Firefox/3.0.7'),
        ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) '
         'Gecko/2009011912 Firefox/3.1.8'),
        ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) '
         'Gecko/2009011912 Firefox/3.1.8'),
        ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) '
         'Gecko/2009011912 Firefox/3.1.7'),
        ('Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; '
         '.NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.0.04506.648;'
         '.NET CLR 3.5.21022)'),
        ]
    for user_agent_string in user_agent_strings:
      user_agent = UserAgent.factory(user_agent_string)
      user_agent.update_groups()

  def test_update_groups_version_level_zero(self):
    self.assertEqual(
        ['Firefox', 'IE'],
        UserAgentGroup.GetStrings(version_level=0))

  def test_update_groups_version_level_one(self):
    self.assertEqual(
        ['Firefox 2', 'Firefox 3', 'IE 7'],
        UserAgentGroup.GetStrings(version_level=1))

  def test_update_groups_version_level_two(self):
    self.assertEqual(
        ['Firefox 2.5', 'Firefox 3.0', 'Firefox 3.1', 'IE 7.0'],
        UserAgentGroup.GetStrings(version_level=2))

  def test_update_groups_version_level_three(self):
    # This also tests that the order comes out the way we'd want even though
    # they didn't go in in that order.
    self.assertEqual(
        ['Firefox 2.5.1', 'Firefox 3.0.7', 'Firefox 3.1.7', 'Firefox 3.1.8',
         'IE 7.0'],
        UserAgentGroup.GetStrings(version_level=3))


class UserAgentGroupWithFilterText(unittest.TestCase):
  def setUp(self):
    for version_level, _ in BROWSER_NAV:
      UserAgentGroup.ClearMemcache(version_level)

    user_agent_strings = [
        ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) '
        'Gecko/2009011912 Firefox/2.5.1'),
        ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) '
        'Gecko/2009011912 Firefox/3.0.7'),
        ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) '
         'Gecko/2009011912 Firefox/3.1.8'),
        ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) '
         'Gecko/2009011912 Firefox/3.1.8'),
        ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) '
         'Gecko/2009011912 Firefox/3.1.7'),
        ('Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; '
         '.NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.0.04506.648;'
         '.NET CLR 3.5.21022)'),
        ('Opera/9.70 (Linux ppc64 ; U; en) Presto/2.2.1'),
        ('Opera/9.50 (J2ME/MIDP; Opera Mini/4.0.10031/298; U; en)'),

        ]
    for user_agent_string in user_agent_strings:
      user_agent = UserAgent.factory(user_agent_string)
      user_agent.update_groups()

  def test_get_strings_with_user_agent_filter_family(self):
    self.assertEqual(
        ['Firefox 2.5.1', 'Firefox 3.0.7', 'Firefox 3.1.7', 'Firefox 3.1.8'],
        UserAgentGroup.GetStrings(version_level='top',
                                  user_agent_filter='Firefox'))
    self.assertEqual(
        ['Firefox 2.5.1', 'Firefox 3.0.7', 'Firefox 3.1.7', 'Firefox 3.1.8'],
        UserAgentGroup.GetStrings(version_level=0, user_agent_filter='Firefox'))
    self.assertEqual(
        ['Firefox 2.5.1', 'Firefox 3.0.7', 'Firefox 3.1.7', 'Firefox 3.1.8'],
        UserAgentGroup.GetStrings(version_level=1, user_agent_filter='Firefox'))
    self.assertEqual(
        ['Firefox 2.5.1', 'Firefox 3.0.7', 'Firefox 3.1.7', 'Firefox 3.1.8'],
        UserAgentGroup.GetStrings(version_level=2, user_agent_filter='Firefox'))
    self.assertEqual(
        ['Opera 9.70'],
        UserAgentGroup.GetStrings(version_level=2, user_agent_filter='Opera'))
    self.assertEqual(
        ['Opera Mini 4.0.10031'],
        UserAgentGroup.GetStrings(version_level=2,
                                  user_agent_filter='Opera Mini'))
    self.assertEqual(
        ['IE 7.0'],
        UserAgentGroup.GetStrings(version_level=2, user_agent_filter='IE'))

  def test_get_strings_with_user_agent_filter_one(self):
    self.assertEqual(
        ['Firefox 3.0.7', 'Firefox 3.1.7', 'Firefox 3.1.8'],
        UserAgentGroup.GetStrings(version_level=2,
                                  user_agent_filter='Firefox 3'))

  def test_get_strings_with_user_agent_filter_two(self):
    self.assertEqual(
        ['Firefox 3.1.7', 'Firefox 3.1.8'],
        UserAgentGroup.GetStrings(version_level=1,
                                  user_agent_filter='Firefox 3.1'))
    self.assertEqual(
        ['Firefox 3.0.7'],
        UserAgentGroup.GetStrings(version_level=1,
                                  user_agent_filter='Firefox 3.0'))


class ChromeFrameTest(unittest.TestCase):

  CHROME_UA_STRING = ('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) '
                        'AppleWebKit/530.1 (KHTML, like Gecko) '
                        'Chrome/2.0.169.1 Safari/530.1')

  CHROME_FRAME_STRINGS = (
      # (family, v1, v2, v3, actual_user_agent_string)
      ('Chrome Frame (IE 6)', '2', '0', '169',
       'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Trident/4.0; '
       'chromeframe; 3.5.30729),gzip(gfe),gzip(gfe)'),
      )

  def testChromeFrameParseSleipnir(self):
    parts = UserAgent.parse(
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; '
        'chromeframe; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR '
        '3.5.30729; Sleipnir 2.8.5),gzip(gfe),gzip(gfe)',
        js_user_agent_string=self.CHROME_UA_STRING)
    self.assertEqual(('Chrome Frame (Sleipnir 2)', '2', '0', '169'), parts)

  def testChromeFrameParseIE(self):
    parts = UserAgent.parse(
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; '
        'chromeframe; SLCC1; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR '
        '3.0.30729),gzip(gfe),gzip(gfe)',
        js_user_agent_string=self.CHROME_UA_STRING)
    self.assertEqual(('Chrome Frame (IE 8)', '2', '0', '169'), parts)

    # Make sure regular IE doesn't get parsed incorrectly if Chrome Frame is
    # installed but not enabled.
    ie8_js_ua_string = ('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; '
        'Trident/4.0; GTB6; chromeframe; .NET CLR 2.0.50727; '
        '.NET CLR 1.1.4322; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; '
        '.NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)')
    parts = UserAgent.parse(
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6; '
        'chromeframe; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR ' '3.0.04506.648; .NET CLR 3.5.21022; .NET CLR 3.0.4506.2152; .NET CLR ' '3.5.30729),gzip(gfe),gzip(gfe)',
        js_user_agent_string=ie8_js_ua_string)
    self.assertEqual(('IE', '8', '0', None), parts)

  def testChromeFrameFactoryExpandoProperty(self):
    ua_string = (
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 6.0; Trident/4.0; '
        'chromeframe; SLCC1; .NET CLR 2.0.5077; 3.0.30729),gzip(gfe),gzip(gfe)')
    ua = UserAgent.factory(
        ua_string, js_user_agent_string=self.CHROME_UA_STRING)
    self.assertEqual(self.CHROME_UA_STRING, ua.js_user_agent_string)

  def testChromeFrameFactoryReuseSamesEntity(self):
    ua_string = (
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 6.0; Trident/4.0; '
        'chromeframe; SLCC1; .NET CLR 2.0.5077; 3.0.30729),gzip(gfe),gzip(gfe)')
    ua = UserAgent.factory(
        ua_string, js_user_agent_string=self.CHROME_UA_STRING)
    ua.remember_me = 99
    ua.put()
    ua2 = UserAgent.factory(
        ua_string, js_user_agent_string=self.CHROME_UA_STRING)
    self.assertEqual(99, ua2.remember_me)

  def testJsUserAgentStringIsNoneReusesSameEntity(self):
    ua_string = (
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 6.0; Trident/4.0; '
        'chromeframe; SLCC1; .NET CLR 2.0.5077; 3.0.30729),gzip(gfe),gzip(gfe)')
    ua = UserAgent.factory(ua_string, js_user_agent_string=None)
    ua.remember_me = 99
    ua.put()
    ua2 = UserAgent.factory(ua_string, js_user_agent_string=None)
    self.assertEqual(99, ua2.remember_me)


class CrazyRigorousUserAgentTest_SKIP_ME(object):
#class CrazyRigorousUserAgentTest(unittest.TestCase):
  def setUp(self):
    import csv
    self.data = list(csv.DictReader(open('test/user_agent_data.csv'),
                                    fieldnames=['ua_string', 'pretty']))

  def testAll(self):
    for record in self.data:
      parsed = UserAgent.parse(record['ua_string'])
      pretty = UserAgent.pretty_print(parsed[0], parsed[1], parsed[2],
                                      parsed[3])
      try:
        self.assertEqual(record['pretty'], pretty)
      except AssertionError:
        if record['pretty'] == 'unknown' and pretty == 'Other':
          donothing = 1
        #ignore for now
        elif re.search(r'pre', pretty):
          donothing = 1
        #ignore for now
        elif re.search(r'\da', pretty):
          donothing = 1
        else:
          logging.info('Steve has %s, we got %s for %s' %
                       (record['pretty'], pretty, record['ua_string']))


if __name__ == '__main__':
  unittest.main()
