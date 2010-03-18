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

import datetime
import unittest
from models import user_agent_release_dates

class ParseReleaseCsvTest(unittest.TestCase):
  def testParseReleaseCsvOne(self):
    releases = user_agent_release_dates.ParseReleaseCsv('Foo,2010-03-11,1.1')
    expected_releases = {
        ('Foo', '1.1'): datetime.date(2010, 3, 11),
        }
    self.assertEqual(expected_releases, releases)

  def testParseReleaseCsvMultiple(self):
    releases = user_agent_release_dates.ParseReleaseCsv(
        'Product,Date,Version\n'
        'Foo,2010-03-11,1.1\n'
        'Foo,2010-03-12,1.2\n')
    expected_releases = {
        ('Foo', '1.1'): datetime.date(2010, 3, 11),
        ('Foo', '1.2'): datetime.date(2010, 3, 12),
        }
    self.assertEqual(expected_releases, releases)


  def testParseReleaseCsvNoDayGivesFirst(self):
    releases = user_agent_release_dates.ParseReleaseCsv('Foo,2010-03,1.1')
    expected_releases = {
        ('Foo', '1.1'): datetime.date(2010, 3, 1),
        }
    self.assertEqual(expected_releases, releases)

  def testParseReleaseCsvNoMonthGivesJanuary(self):
    releases = user_agent_release_dates.ParseReleaseCsv('Foo,2010,1.1')
    expected_releases = {
        ('Foo', '1.1'): datetime.date(2010, 1, 1),
        }
    self.assertEqual(expected_releases, releases)

class ParseChromeReleaseCsvTest(unittest.TestCase):
  def testParseChromeReleaseCsvOne(self):
    releases = user_agent_release_dates.ParseChromeReleaseCsv(
        'Chrome,2010-03-11,1.0.160.0,Dev')
    expected_releases = {
        ('Chrome', '1.0.160'): datetime.date(2010, 3, 11),
        }
    self.assertEqual(expected_releases, releases)

  def testParseChromeReleaseCsvOverlap(self):
    releases = user_agent_release_dates.ParseChromeReleaseCsv(
        'Product,Date,Version,Channel\n'
        'Chrome,2010-03-11,1.0.160.0,Dev\n'
        'Chrome,2010-03-12,1.0.160.0,Beta\n')
    expected_releases = {
        ('Chrome', '1.0.160'): datetime.date(2010, 3, 11),
        }
    self.assertEqual(expected_releases, releases)


class ParseSafariReleaseCsvTest(unittest.TestCase):
  def testParseSafariReleaseCsvOne(self):
    releases = user_agent_release_dates.ParseSafariReleaseCsv(
        'Safari,2010-03-11,4.3.2,565.43,Windows')
    expected_releases = {
        ('Safari', '4.3.2'): datetime.date(2010, 3, 11),
        }
    self.assertEqual(expected_releases, releases)

  def testParseSafariReleaseCsvMultiple(self):
    releases = user_agent_release_dates.ParseSafariReleaseCsv(
        'Product,Date,Version,Webkit Version,OS\n'
        'Safari,2010-03-11,3.2.1,525.27,Windows\n'
        'Safari,2010-03-12,3.2.2,525.27.1,MacOS X\n')
    expected_releases = {
        ('Safari', '3.2.1'): datetime.date(2010, 3, 11),
        ('Safari', '3.2.2'): datetime.date(2010, 3, 12),
        }
    self.assertEqual(expected_releases, releases)


class ReleaseDateTest(unittest.TestCase):
  def testReleaseDateMissGivesNone(self):
    self.assertEqual(None,
                     user_agent_release_dates.ReleaseDate('M', '123456'))
    self.assertEqual(None,
                     user_agent_release_dates.ReleaseDate('Product', 'Version'))

  def testReleaseDateBasic(self):
    releases = (
        (('IE', '1.0'), datetime.date(1995, 8, 1)),
        (('IE', '7.0'), datetime.date(2006, 10, 18)),
        (('IE', '8.0'), datetime.date(2009, 3, 19)),
        (('Safari', '0.8'), datetime.date(2003, 1, 7)),
        (('Safari', '4.0.4'), datetime.date(2009, 11, 11)),
        (('Opera', '5.0'), datetime.date(2000, 6, 12)),
        (('Opera', '7.0 Beta 1 v. 2'), datetime.date(2002, 11, 22)),
        (('Firefox', '0.1'), datetime.date(2002, 9, 23)),
        (('Firefox', '3.7.a2'), datetime.date(2010, 3, 1)),
        (('Chrome', '0.0.81.0'), datetime.date(2007, 5, 10)),
        (('Chrome', '2.0.154.65'), datetime.date(2009, 5, 8)),
        )
