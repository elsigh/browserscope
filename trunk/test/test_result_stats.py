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

"""Test Result Stats."""

__author__ = 'slamm@google.com (Stephen Lamm)'

import logging
import random
import unittest

from google.appengine.api import memcache
from google.appengine.ext import db
from categories import all_test_sets
from models import result_stats
from models.result import ResultParent
from third_party import mox
import mock_data


class CategoryBrowserManagerTest(unittest.TestCase):

  def setUp(self):
    self.cls = result_stats.CategoryBrowserManager

  def testEmpty(self):
    category = 'network'
    version_level = 1
    browsers = self.cls.GetBrowsers(category, version_level)
    self.assertEqual([], browsers)

  def testAddUserAgentBasic(self):
    category = 'network'
    self.cls.AddUserAgent(category, mock_data.GetUserAgent('Firefox 3.5'))
    self.cls.AddUserAgent(category, mock_data.GetUserAgent('Firefox 3.0.7'))
    for version_level, expected_browsers in enumerate((
        ['Firefox'],
        ['Firefox 3'],
        ['Firefox 3.0', 'Firefox 3.5'],
        ['Firefox 3.0.7', 'Firefox 3.5'])):
      browsers = self.cls.GetBrowsers(category, version_level)
      self.assertEqual(expected_browsers, browsers)

  def testAddUserAgentSummary(self):
    self.cls.AddUserAgent('network', mock_data.GetUserAgent('Firefox 3.5'))
    self.cls.AddUserAgent('security', mock_data.GetUserAgent('Firefox 3.0.7'))
    for version_level, expected_browsers in enumerate((
        ['Firefox'],
        ['Firefox 3'],
        ['Firefox 3.0', 'Firefox 3.5'],
        ['Firefox 3.0.7', 'Firefox 3.5'])):
      browsers = self.cls.GetBrowsers('summary', version_level)
      self.assertEqual(expected_browsers, browsers)

  def testGetBrowsersTop(self):
    expected_browsers = list(result_stats.TOP_BROWSERS)
    browsers = self.cls.GetBrowsers(category='foo', version_level='top')
    self.assertEqual(expected_browsers, browsers)

  def testGetBrowsersDbAndMemcacheUse(self):
    category = 'network'
    version_level = 3
    cls = result_stats.CategoryBrowserManager
    cls.AddUserAgent(category, mock_data.GetUserAgent('Firefox 3.5'))
    self.assertEqual(['Firefox 3.5'], cls.GetBrowsers(category, version_level))

    # Load browsers from db into memcache and return.
    memcache.flush_all()
    self.assertEqual(['Firefox 3.5'], cls.GetBrowsers(category, version_level))

    # Load browsers memcache (db is not changed).
    cls.get_by_key_name(cls.KeyName(category, version_level)).delete()
    self.assertEqual(['Firefox 3.5'], cls.GetBrowsers(category, version_level))

    # db and memcache are cleared.
    memcache.flush_all()
    self.assertEqual([], cls.GetBrowsers(category, version_level))

  def testSetBrowsers(self):
    category = 'basil'
    version_level = 1
    expected_browsers = ['IE 8', 'Safari 5.8.2', 'Firefox 3.0']
    self.cls.SetBrowsers(category, version_level, expected_browsers)
    browsers = self.cls.GetBrowsers(category, version_level)
    self.assertEqual(sorted(expected_browsers), browsers)

  def testSetBrowsersDbAndMemcacheUse(self):
    category = 'basil'
    version_level = 1
    expected_browsers = ['Firefox 3.0', 'IE 8', 'Safari 5.8.2']
    self.cls.SetBrowsers(category, version_level, expected_browsers)
    browsers = self.cls.GetBrowsers(category, version_level)
    self.assertEqual(expected_browsers, browsers)

  def testUpdateSummaryBrowsers(self):
    self.cls.SetBrowsers(
        'anise', 0, ['Firefox', 'IE'])
    self.cls.SetBrowsers(
        'basil', 0, ['IE', 'Safari'])
    self.cls.SetBrowsers(
        'anise', 3, ['Firefox 3.5.6', 'Firefox 3.6', 'IE 7', 'IE 8'])
    self.cls.SetBrowsers(
        'basil', 3, ['IE 8', 'IE 9', 'Safari 4.3', 'Safari 4.4'])
    self.cls.UpdateSummaryBrowsers(['anise', 'basil'])
    self.assertEqual(['Firefox', 'IE', 'Safari'],
                     self.cls.GetBrowsers('summary', 0))
    self.assertEqual(['Firefox 3.5.6', 'Firefox 3.6', 'IE 7', 'IE 8', 'IE 9',
                      'Safari 4.3', 'Safari 4.4'],
                     self.cls.GetBrowsers('summary', 3))

  def testSortBrowsers(self):
    expected_browsers = [
        'Firefox',
        'Firefox (Minefield)',
        'Firefox (Shiretoko)',
        'Firefox 3',
        'Firefox 3.0a3pre',
        'Firefox 3.0b5',
        'Firefox 3.0pre',
        'Firefox 3.0',
        'Firefox 3.0.1',
        'Firefox 3.4',
        'Firefox 3.4.1',
        'Firefox (Shiretoko) 3.5a1pre',
        'Firefox (Minefield) 3.5a4',
        'Firefox 3.5',
        'Firefox (Namoroka) 3.5.1a3',
        'Firefox 3.5.1',
        'Firefox 3.5.2',
        'iPhone 1.1',
        'Safari 5.0',
        ]
    browsers = expected_browsers[:]
    random.seed(5)
    random.shuffle(browsers)
    self.cls.SortBrowsers(browsers)
    self.assertEqual(expected_browsers, browsers)

  def testInsortBrowser(self):
    browsers = ['Firefox 3.0', 'Firefox 3.5', 'Safari 5.0']
    self.cls.InsortBrowser(browsers, 'iPhone 1.1')
    self.assertEqual(['Firefox 3.0', 'Firefox 3.5', 'iPhone 1.1', 'Safari 5.0'],
                     browsers)

  def testInsortBrowserWithTupleRaises(self):
    browsers = ('Firefox 3.0', 'Firefox 3.5', 'Safari 5.0')
    self.assertRaises(AttributeError,
                      self.cls.InsortBrowser, browsers, 'iPhone 1.1')

  def testInsortWithTopBrowsers(self):
    expected_browsers = list(result_stats.TOP_BROWSERS)
    expected_browsers.append('ZZZzzzz 999.99.9')
    browsers = self.cls.GetBrowsers(category='foo', version_level='top')
    self.cls.InsortBrowser(browsers, 'ZZZzzzz 999.99.9')
    self.assertEqual(expected_browsers, browsers)

  def testSortBrowsersOldStyleAlphaVersion(self):
    """Test that sort handles bad version string sensibly."""
    expected_browsers = ['Firefox 3.0.a4', 'Firefox 3.5']
    browsers = expected_browsers[:]
    random.seed(5)
    random.shuffle(browsers)
    self.cls.SortBrowsers(browsers)
    self.assertEqual(expected_browsers, browsers)


class CategoryBrowserManagerFilterTest(unittest.TestCase):

  def setUp(self):
    self.cls = result_stats.CategoryBrowserManager
    self.category = 'network'
    result_stats.CategoryBrowserManager.AddUserAgent(
        self.category, mock_data.GetUserAgent('Firefox 2.5.1'))
    result_stats.CategoryBrowserManager.AddUserAgent(
        self.category, mock_data.GetUserAgent('Firefox 3.1.8'))
    result_stats.CategoryBrowserManager.AddUserAgent(
        self.category, mock_data.GetUserAgent('Firefox 3.0.7'))
    result_stats.CategoryBrowserManager.AddUserAgent(
        self.category, mock_data.GetUserAgent('Firefox 3.1.7'))
    result_stats.CategoryBrowserManager.AddUserAgent(
        self.category, mock_data.GetUserAgent('IE 7.0'))
    result_stats.CategoryBrowserManager.AddUserAgent(
        self.category, mock_data.GetUserAgent('Opera 9.70'))
    result_stats.CategoryBrowserManager.AddUserAgent(
        self.category, mock_data.GetUserAgent('Opera Mini 4.0.10031'))

  def testGetFilteredBrowsersFamily(self):
    expected_browsers = [
        'Firefox 2.5.1', 'Firefox 3.0.7', 'Firefox 3.1.7', 'Firefox 3.1.8']
    browsers = self.cls.GetFilteredBrowsers(self.category, ['Firefox*'])
    self.assertEqual(expected_browsers, browsers)

  def testGetFilteredBrowsersMajorVersion(self):
    expected_browsers = ['Firefox 3.0.7', 'Firefox 3.1.7', 'Firefox 3.1.8']
    browsers = self.cls.GetFilteredBrowsers(self.category, ['Firefox 3*'])
    self.assertEqual(expected_browsers, browsers)

  def testGetFilteredBrowsersMinorVersion(self):
    expected_browsers = ['Firefox 3.1.7', 'Firefox 3.1.8']
    browsers = self.cls.GetFilteredBrowsers(self.category, ['Firefox 3.1*'])
    self.assertEqual(expected_browsers, browsers)

  def testGetFilteredBrowsersOperaSkipsOperaMini(self):
    expected_browsers = ['Opera 9.70']  # Opera Mini 4.0.10031 is excluded
    browsers = self.cls.GetFilteredBrowsers(self.category, ['Opera*'])
    self.assertEqual(expected_browsers, browsers)

  def testGetFilteredBrowsersMinorVersion(self):
    expected_browsers = [
        'Firefox 2.5.1', 'Firefox 3.1.7', 'Firefox 3.1.8', 'Opera 9.70']
    browsers = self.cls.GetFilteredBrowsers(
        self.category, ['Firefox 2.5.1', 'Firefox 3.1*', 'Opera*'])
    self.assertEqual(expected_browsers, browsers)


TEST_STATS = {
    'Aardvark': {
        'Firefox 3': {
            'summary_score': 2,
            'summary_display': '93/100',
            'total_runs': 8
            },
        'Firefox 3.5': {
            'summary_score': 5,
            'summary_display': '83/100',
            'total_runs': 5
            },
        },
    'Badger': {
        'Firefox 3': {
            'summary_score': 7,
            'summary_display': '12/15',
            'total_runs': 3
            },
        'IE 7': {
            'summary_score': 9,
            'summary_display': '14/15',
            'total_runs': 1
            },
        },
    'Coati': {
        'Firefox 3': {
            'summary_score': 2,
            'summary_display': '9/19',
            'total_runs': 99
            },
        'Firefox 3.5': {
            'summary_score': 1,
            'summary_display': '8/19',
            'total_runs': 89
            },
        },
    }


class SummaryStatsManagerTest(unittest.TestCase):

  def setUp(self):
    self.cls = result_stats.SummaryStatsManager

  def testUpdateStatsBasic(self):
    category = 'Aardvark'
    updated_summary_stats = self.cls.UpdateStats(category, TEST_STATS[category])
    memcache_summary_stats = memcache.get_multi(
        ['Firefox 3', 'Firefox 3.5'], namespace=self.cls.MEMCACHE_NAMESPACE)
    expected_summary_stats = {
        'Firefox 3': {
            'results': {
                'Aardvark': {
                    'score': 2,
                    'display': '93/100',
                    'total_runs': 8,
                    },
                },
            },
        'Firefox 3.5': {
            'results': {
                'Aardvark': {
                    'score': 5,
                    'display': '83/100',
                    'total_runs': 5,
                    },
                },
            },
        }
    self.assertEqual(expected_summary_stats, updated_summary_stats)
    self.assertEqual(expected_summary_stats, memcache_summary_stats)

  def testUpdateStatsTwoCategories(self):
    for category in ('Aardvark', 'Badger'):
      updated_summary_stats = self.cls.UpdateStats(
          category, TEST_STATS[category])
    expected_updated_summary_stats = {
        'Firefox 3': {
            'results': {
                'Aardvark': {
                    'score': 2,
                    'display': '93/100',
                    'total_runs': 8,
                    },
                'Badger': {
                    'score': 7,
                    'display': '12/15',
                    'total_runs': 3,
                    },
                },
            },
        'IE 7': {
            'results': {
                'Badger': {
                    'score': 9,
                    'display': '14/15',
                    'total_runs': 1,
                    },
                },
            },
        }
    self.assertEqual(expected_updated_summary_stats, updated_summary_stats)
    expected_summary_stats = expected_updated_summary_stats.copy()
    expected_summary_stats.update({
        'Firefox 3.5': {
            'results': {
                'Aardvark': {
                    'score': 5,
                    'display': '83/100',
                    'total_runs': 5,
                    },
                },
            },
        })
    memcache_summary_stats = memcache.get_multi(
        ['Firefox 3', 'Firefox 3.5', 'IE 7'],
        namespace=self.cls.MEMCACHE_NAMESPACE)
    self.assertEqual(expected_summary_stats, memcache_summary_stats)


class SummaryStatsManagerGetStatsTest(unittest.TestCase):

  def setUp(self):
    self.mox = mox.Mox()
    self.cls = result_stats.SummaryStatsManager
    self.test_set_a = mock_data.MockTestSet(category='Aardvark')
    self.test_set_b = mock_data.MockTestSet(category='Badger')
    all_test_sets.AddTestSet(self.test_set_a)
    all_test_sets.AddTestSet(self.test_set_b)

  def tearDown(self):
    self.mox.UnsetStubs()
    all_test_sets.RemoveTestSet(self.test_set_a)
    all_test_sets.RemoveTestSet(self.test_set_b)

  def testGetStatsBasic(self):
    for category in ('Aardvark', 'Coati'):
      updated_summary_stats = self.cls.UpdateStats(
          category, TEST_STATS[category])
    expected_summary_stats = {
        'Firefox 3.5': {
            'summary_score': 3,
            'summary_display': '3/100',
            'total_runs': 94,
            'results': {
                'Aardvark': {
                    'score': 5,
                    'display': '83/100',
                    'total_runs': 5,
                    },
                'Coati': {
                    'score': 1,
                    'display': '8/19',
                    'total_runs': 89,
                    },
                },
            },
        'total_runs': 94,
        }
    summary_stats = self.cls.GetStats(
        ['Firefox 3.5'], categories=['Aardvark', 'Coati'])
    self.assertEqual(expected_summary_stats, summary_stats)

  def testGetStatsTrimUnwanted(self):
    for category in ('Aardvark', 'Coati'):
      updated_summary_stats = self.cls.UpdateStats(
          category, TEST_STATS[category])
    expected_summary_stats = {
        'Firefox 3': {
            'summary_score': 2,
            'summary_display': '2/100',
            'total_runs': 107,
            'results': {
                'Aardvark': {
                    'score': 2,
                    'display': '93/100',
                    'total_runs': 8,
                    },
                'Coati': {
                    'score': 2,
                    'display': '9/19',
                    'total_runs': 99,
                    },
                },
            },
        'Firefox 3.5': {
            'summary_score': 3,
            'summary_display': '3/100',
            'total_runs': 94,
            'results': {
                'Aardvark': {
                    'score': 5,
                    'display': '83/100',
                    'total_runs': 5,
                    },
                'Coati': {
                    'score': 1,
                    'display': '8/19',
                    'total_runs': 89,
                    },
                },
            },
        'total_runs': 201,
        }
    summary_stats = self.cls.GetStats(
        ['Firefox 3', 'Firefox 3.5'], categories=['Aardvark', 'Coati'])
    self.assertEqual(expected_summary_stats, summary_stats)

  def testGetStatsMissingStats(self):
    for category in ('Aardvark', 'Badger'):
      updated_summary_stats = self.cls.UpdateStats(
          category, TEST_STATS[category])
    self.mox.StubOutWithMock(
        result_stats.CategoryStatsManager, 'GetStats')
    result_stats.CategoryStatsManager.GetStats(
        self.test_set_a, ['Safari'], ['apple', 'banana', 'coconut']
        ).InAnyOrder().AndReturn({
            'Safari': {
                'summary_score': 0,
                'summary_display': '',
                'total_runs': 0,
                'results': {
                    'Aardvark': {
                        'score': 0,
                        'display': '',
                        'total_runs': 0,
                        },
                    },
                },
            'total_runs': 0,
            })
    result_stats.CategoryStatsManager.GetStats(
        self.test_set_b, ['Safari'], ['apple', 'banana', 'coconut']
        ).InAnyOrder().AndReturn({
            'Safari': {
                'summary_score': 5,
                'summary_display': '5/15',
                'total_runs': 15,
                'results': {
                    'Badger': {
                        'score': 5,
                        'display': '5/15',
                        'total_runs': 15,
                        },
                     },
                },
            'total_runs': 15,
            })
    self.mox.ReplayAll()
    expected_summary_stats = {
        'Firefox 3': {
            'summary_score': 4,
            'summary_display': '4/100',
            'total_runs': 11,
            'results': {
                'Aardvark': {
                    'score': 2,
                    'display': '93/100',
                    'total_runs': 8,
                    },
                'Badger': {
                    'score': 7,
                    'display': '12/15',
                    'total_runs': 3,
                    },
                },
            },
        'Safari': {
            'summary_score': 2,
            'summary_display': '2/100',
            'total_runs': 15,
            'results': {
                'Aardvark': {
                    'score': 0,
                    'display': '',
                    'total_runs': 0,
                    },
                'Badger': {
                    'score': 5,
                    'display': '5/15',
                    'total_runs': 15,
                    },
                },
            },
        'total_runs': 26,
        }
    summary_stats = self.cls.GetStats(
        ['Firefox 3', 'Safari'], categories=['Aardvark', 'Badger'])
    self.mox.VerifyAll()
    self.assertEqual(expected_summary_stats, summary_stats)


class CategoryStatsManagerTest(unittest.TestCase):

  MANAGER_QUERY = result_stats.CategoryBrowserManager.all(keys_only=True)

  def setUp(self):
    self.test_set = mock_data.MockTestSet()
    all_test_sets.AddTestSet(self.test_set)

  def tearDown(self):
    all_test_sets.RemoveTestSet(self.test_set)

  def testGetStats(self):
    add_result_params = (
        # ((apple, banana, coconut), firefox_version)
        ((0, 0, 500), 'Firefox 3.0.7'),
        ((1, 1, 200), 'Firefox 3.0.7'),
        ((0, 2, 300), 'Firefox 3.0.7'),
        ((1, 3, 100), 'Firefox 3.5'),
        ((0, 4, 400), 'Firefox 3.5')
        )
    for scores, browser in add_result_params:
      parent = ResultParent.AddResult(
          self.test_set, '12.2.2.25', mock_data.GetUserAgentString(browser),
          'apple=%s,banana=%s,coconut=%s' % scores)
    level_1_stats = {
        'Firefox 3': {
            'summary_score': 605,
            'summary_display': '302',
            'total_runs': 5,
            'results': {
                'coconut': {'score': 600, 'raw_score': 300, 'display': 'd:600'},
                'apple': {'score': 1, 'raw_score': 0, 'display': 'no'},
                'banana': {'score': 4, 'raw_score': 2, 'display': 'd:4'}
                }
            },
        'total_runs': 5,
        }
    self.assertEqual(level_1_stats, result_stats.CategoryStatsManager.GetStats(
        self.test_set, browsers=('Firefox 3',),
        test_keys=['apple', 'banana', 'coconut']))

    level_3_stats = {
        'Firefox 3.0.7': {
            'summary_score': 603,
            'summary_display': '301',
            'total_runs': 3,
            'results': {
                'coconut': {'score': 600, 'raw_score': 300, 'display': 'd:600'},
                'apple': {'score': 1, 'raw_score': 0, 'display': 'no'},
                'banana': {'score': 2, 'raw_score': 1, 'display': 'd:2'}
                }
            },
        'Firefox 3.5': {
            'summary_score': 908,
            'summary_display': '405',
            'total_runs': 2,
            'results': {
                'coconut': {'score': 800, 'raw_score': 400, 'display': 'd:800'},
                'apple': {'score': 100, 'raw_score': 1, 'display': 'yes'},
                'banana': {'score': 8, 'raw_score': 4, 'display': 'd:8'}
                }
            },
        'total_runs': 5,
        }
    self.assertEqual(level_3_stats, result_stats.CategoryStatsManager.GetStats(
        self.test_set, browsers=('Firefox 3.0.7', 'Firefox 3.5'),
        test_keys=['apple', 'banana', 'coconut']))


class UpdateStatsCacheTest(unittest.TestCase):

  MANAGER_QUERY = result_stats.CategoryBrowserManager.all(keys_only=True)

  def setUp(self):
    self.mox = mox.Mox()
    self.test_set = mock_data.MockTestSet()
    all_test_sets.AddTestSet(self.test_set)

  def tearDown(self):
    self.mox.UnsetStubs()
    all_test_sets.RemoveTestSet(self.test_set)

  def testBasic(self):
    category = self.test_set.category
    cls = result_stats.CategoryStatsManager
    browsers = ['Earth', 'Wind', 'Fire']
    test_keys = ['apple', 'banana', 'coconut']
    self.mox.StubOutWithMock(self.test_set, 'GetMediansAndNumScores')
    self.mox.StubOutWithMock(self.test_set, 'GetStats')
    self.mox.StubOutWithMock(result_stats.SummaryStatsManager, 'UpdateStats')
    self.test_set.GetMediansAndNumScores('Earth').AndReturn(('m1', 'n1'))
    self.test_set.GetStats(test_keys, 'm1', 'n1').AndReturn('s1')
    self.test_set.GetMediansAndNumScores('Wind').AndReturn(('m2', 'n2'))
    self.test_set.GetStats(test_keys, 'm2', 'n2').AndReturn('s2')
    self.test_set.GetMediansAndNumScores('Fire').AndReturn(('m3', 'n3'))
    self.test_set.GetStats(test_keys, 'm3', 'n3').AndReturn('s3')
    expected_ua_stats = {'Earth': 's1', 'Wind': 's2', 'Fire': 's3'}
    result_stats.SummaryStatsManager.UpdateStats(
        category, expected_ua_stats).AndReturn('notused')
    self.mox.ReplayAll()
    cls.UpdateStatsCache(category, browsers)
    self.mox.VerifyAll()
    ua_stats = memcache.get_multi(browsers, **cls.MemcacheParams(category))
    self.assertEqual(expected_ua_stats, ua_stats)
