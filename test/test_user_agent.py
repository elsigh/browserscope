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

  def test_parse_pretty(self):
    browsers = (
        ('Chrome Frame (IE 6) 4.0.223', ('Chrome Frame (IE 6)', '4', '0', '223')),
        ('Firefox 3.0', ('Firefox', '3', '0', None)),
        ('Firefox 3.0pre', ('Firefox', '3', '0pre', None)),
        ('Firefox 3.0b5', ('Firefox', '3', '0b5', None)),
        ('Firefox (Shiretoko) 3.5.6pre', ('Firefox (Shiretoko)', '3', '5', '6pre')),
        ('Firefox 3.5.4', ('Firefox', '3', '5', '4')),
        ('Opera Mini 5.0.16875', ('Opera Mini', '5', '0', '16875')),
        ('OLPC 0', ('OLPC', '0', None, None)),
        ('Sony Ericsson K800i', ('Sony Ericsson K800i', None, None, None)),
        ('Space Bison 0.02', ('Space Bison', '0', '02', None)),
        ('Teleca Q7', ('Teleca Q7', None, None, None)),
        )
    for browser, parts in browsers:
      self.assertEqual(parts, UserAgent.parse_pretty(browser))

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
        ['Safari', 'Safari 100', 'Safari 100.33preA4'],
        UserAgent.parse_to_string_list('Safari 100.33preA4'))


class ChromeFrameFactoryTest(unittest.TestCase):

  CHROME_UA_STRING = (
      'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/530.1 '
      '(KHTML, like Gecko) Chrome/2.0.169.1 Safari/530.1')

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

  def testChromeFrameGivenEvenWhenRegularIEComesFirst(self):
    ua_string = (
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 6.0; Trident/4.0; '
        'chromeframe; SLCC1; .NET CLR 2.0.5077; 3.0.30729),gzip(gfe),gzip(gfe)')
    ua = UserAgent.factory(
        ua_string, js_user_agent_string=None)
    ua2 = UserAgent.factory(
        ua_string, js_user_agent_string=self.CHROME_UA_STRING)
    ua3 = UserAgent.factory(
        ua_string, js_user_agent_string=None)
    self.assertEqual('IE', ua.family)
    self.assertEqual('Chrome Frame (IE 6)', ua2.family)
    self.assertEqual('IE', ua3.family)


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
