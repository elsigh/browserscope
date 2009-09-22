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

"""Test admin_rankers."""

__author__ = 'slamm@google.com (Stephen Lamm)'


import logging
import unittest

import mock_data
import settings

from django.test.client import Client
from django.utils import simplejson
from google.appengine.ext import db

from categories import test_set_params
from models import result_ranker
from models.result import ResultParent
from models.result import ResultTime
from models.user_agent import UserAgent
from models.user_agent import UserAgentGroup

from base import admin_rankers

USER_AGENT_STRINGS = {
    'Firefox 3.0.6': ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) '
                      'Gecko/2009011912 Firefox/3.0.6'),
    'Firefox 3.5': ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) '
                    'Gecko/2009011912 Firefox/3.5'),
    'Firefox 3.0.9': ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) '
                      'Gecko/2009011912 Firefox/3.0.9'),
    }

class TestResultParentQuery(unittest.TestCase):
  USER_AGENT_PRETTY = 'test_admin_rankers 1.1.1'

  def setUp(self):
    pass

  def tearDown(self):
    db.delete(ResultParent.all(keys_only=True).fetch(1000))
    db.delete(ResultTime.all(keys_only=True).fetch(1000))

  def testQueryEmpty(self):
    limit = 10
    bookmark = None
    query = admin_rankers.ResultParentQuery('el cato', limit, bookmark)
    self.assertFalse(query.HasNext())
    self.assertEqual(None, query.GetNext())
    self.assertEqual(None, query.GetBookmark())
    self.assertEqual(0, query.GetCountUsed())
    self.assertRaises(AssertionError, query.PushBack)

  def testQueryOne(self):
    test_set = mock_data.MockTestSet('el cato')
    result = ResultParent.AddResult(
        test_set, '12.2.2.25', USER_AGENT_STRINGS['Firefox 3.0.6'],
        'testDisplay=500,testVisibility=200')
    limit = 10
    bookmark = None
    query = admin_rankers.ResultParentQuery(result.category, limit, bookmark)
    self.assert_(query.HasNext())
    self.assertEqual('12.2.2.25', query.GetNext().ip)
    self.assertEqual(None, query.GetBookmark())
    self.assertEqual(1, query.GetCountUsed())
    query.PushBack()
    self.assertEqual(None, query.GetBookmark())
    self.assertEqual(0, query.GetCountUsed())

  def testQueryThree(self):
    test_set = mock_data.MockTestSet('el cato')
    for index in range(3):
      result = ResultParent.AddResult(
          test_set, '12.2.2.%s' % index, USER_AGENT_STRINGS['Firefox 3.0.6'],
          'testDisplay=500,testVisibility=200')
    limit = 10
    bookmark = None
    query = admin_rankers.ResultParentQuery(result.category, limit, bookmark)
    self.assert_(query.HasNext())
    self.assertEqual('12.2.2.0', query.GetNext().ip)
    self.assert_(query.HasNext())
    self.assertNotEqual(None, query.GetBookmark())
    self.assertEqual(1, query.GetCountUsed())
    self.assertEqual('12.2.2.1', query.GetNext().ip)
    self.assertEqual('12.2.2.2', query.GetNext().ip)
    self.assertFalse(query.HasNext())
    self.assertEqual(3, query.GetCountUsed())
    query.PushBack()
    self.assert_(query.HasNext())
    self.assertEqual(2, query.GetCountUsed())

    bookmark = query.GetBookmark()
    self.assertNotEqual(None, bookmark)
    query = admin_rankers.ResultParentQuery(result.category, limit, bookmark)
    self.assert_(query.HasNext())
    self.assertEqual('12.2.2.2', query.GetNext().ip)

class TestResultTimeQuery(unittest.TestCase):

  def testQueryBasic(self):
    query = admin_rankers.ResultTimeQuery()
    test_set = mock_data.MockTestSet('el cato')
    result = ResultParent.AddResult(
        test_set, '12.2.2.25', USER_AGENT_STRINGS['Firefox 3.0.6'],
        'testDisplay=500,testVisibility=200')
    for result_time in ResultTime.all().fetch(1000):
      result_time.dirty = False
      result_time.put()
    result_time = query.get(result, 'testDisplay')
    self.assertEqual(500, result_time.score)


class TestRebuildRankers(unittest.TestCase):


  def setUp(self):
    self.old_settings = settings.CATEGORIES
    settings.CATEGORIES = None  # set this in each test
    self.client = Client()

  def tearDown(self):
    settings.CATEGORIES = self.old_settings

  def testRebuildBasic(self):
    settings.CATEGORIES = ['el cato']
    test_set = mock_data.MockTestSet('el cato')
    result = ResultParent.AddResult(
        test_set, '12.2.2.25', USER_AGENT_STRINGS['Firefox 3.0.6'],
        'testDisplay=500,testVisibility=200')
    result.increment_all_counts()
    params = {}
    response = self.client.get('/admin/rankers/rebuild', params)
    self.assertEqual(200, response.status_code)
    response_data = simplejson.loads(response.content)
    self.assertEqual(None, response_data['bookmark'])
    self.assertFalse(response_data['is_done'])
    self.assertEqual(1, response_data['total_results'])

    ranker = result_ranker.ResultRanker.Get(
        'el cato', test_set.GetTest('testDisplay'), 'Firefox 3',
        params_str=None, ranker_version='next')
    self.assertEqual((500, 1), ranker.GetMedianAndNumScores())

  def testRebuildResultsWithBookmarks(self):
    settings.CATEGORIES = ['catogrey']
    test_set = mock_data.MockTestSet(
        'catogrey', params=test_set_params.Params('foo', 'd=c'))
    params_str = str(test_set.default_params)
    version_scores = (
        ('3.0.6', (500, 0)),
        ('3.0.9', (200, 1)),
        ('3.0.9', (300, 2)),
        ('3.5', (100, 3)),
        ('3.5', (400, 4)),
        )
    for version, scores in version_scores:
      result = ResultParent.AddResult(
          test_set, '12.2.2.25', USER_AGENT_STRINGS['Firefox %s' % version],
          'testDisplay=%s,testVisibility=%s' % scores, params_str=params_str)
      result.increment_all_counts()
    params = {'fetch_limit': 2}
    request_count = 0
    while not params.get('is_done', False):
      response = self.client.get('/admin/rankers/rebuild', params)
      params = simplejson.loads(response.content)
      logging.info('params: %s', params)
      request_count += 1

    # ceiling(num_result_parents * num_tests / fetch_limit)
    self.assertEqual(6, request_count)

    ranker = result_ranker.ResultRanker.Get(
        'catogrey', test_set.GetTest('testDisplay'), 'Firefox 3.0',
        params_str=params_str, ranker_version='next')
    self.assertEqual((300, 3), ranker.GetMedianAndNumScores())

    ranker = result_ranker.ResultRanker.Get(
        'catogrey', test_set.GetTest('testVisibility'), 'Firefox',
        params_str=params_str, ranker_version='next')
    self.assertEqual((2, 5), ranker.GetMedianAndNumScores())


class TestReleaseNextRankers(unittest.TestCase):
  def setUp(self):
    self.client = Client()

  def testReleaseNextNone(self):
    response = self.client.get('/admin/rankers/release_next', {})
    params = simplejson.loads(response.content)
    self.assertEqual(200, response.status_code)
    self.assertEqual(True, params['is_done'])
    self.assertEqual(0, params['total'])

  def testReleaseNextBasic(self):
    test = mock_data.MockTest('foo', 'Boo Hoo', '/poopoo', 'custom')
    user_agent_version = 'Chrome 3'
    params_str = None
    for score, category in ((3, 'cat 1'), (5, 'cat II'), (7, 'cat c')):
      ranker = result_ranker.ResultRanker.GetOrCreate(
          category, test, user_agent_version, params_str, ranker_version='next')
      ranker.Add(score)
    params = {}
    response = self.client.get('/admin/rankers/release_next', {})
    params = simplejson.loads(response.content)
    self.assertEqual(200, response.status_code)
    self.assertEqual(True, params['is_done'])
    self.assertEqual(3, params['total'])

    for score, category in ((3, 'cat 1'), (5, 'cat II'), (7, 'cat c')):
      ranker = result_ranker.ResultRanker.Get(
          category, test, user_agent_version, params_str, 'current')
      self.assertEqual((score, 1), ranker.GetMedianAndNumScores())

  def testReleaseNextTwoRequests(self):
    test = mock_data.MockTest('foo', 'Boo Hoo', '/poopoo', 'custom')
    user_agent_version = 'Chrome 3'
    params_str = None
    for score, category in ((3, 'cat 1'), (5, 'cat II'), (7, 'cat c')):
      ranker = result_ranker.ResultRanker.GetOrCreate(
          category, test, user_agent_version, params_str, ranker_version='next')
      ranker.Add(score)
    params = {'fetch_limit': 2}
    request_count = 0
    while not params.get('is_done', False):
      response = self.client.get('/admin/rankers/release_next', params)
      params = simplejson.loads(response.content)
      logging.info('params: %s', params)
      request_count += 1
    self.assertEqual(2, request_count)

    for score, category in ((3, 'cat 1'), (5, 'cat II'), (7, 'cat c')):
      ranker = result_ranker.ResultRanker.Get(
          category, test, user_agent_version, params_str, 'current')
      self.assertEqual((score, 1), ranker.GetMedianAndNumScores())


class TestRebuildUserAgents(unittest.TestCase):
  def setUp(self):
    self.client = Client()
    self.assertEqual(None, UserAgent.all().get())
    self.assertEqual(None, UserAgentGroup.all().get())

  def tearDown(self):
    db.delete(UserAgent.all(keys_only=True).fetch(1000))
    db.delete(UserAgentGroup.all(keys_only=True).fetch(1000))

  def testPartsFixed(self):
    ua_string = ('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; '
                 'Trident/4.0; .NET CLR 2.0.50727; .NET CLR 1.1.4322')
    ua = UserAgent.factory(ua_string)
    ua.v1 = '9'
    ua.put()
    params = {}
    response = self.client.get('/admin/ua/rebuild', params)
    self.assertEqual(200, response.status_code)
    ua = UserAgent.all().get()
    self.assertEqual(('IE', '8', '0', None), (ua.family, ua.v1, ua.v2, ua.v3))

  def testUserAgentStringListCached(self):
    ua_string = ('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; '
                 'Trident/4.0; .NET CLR 2.0.50727; .NET CLR 1.1.4322')
    ua = UserAgent.factory(ua_string)
    self.is_get_string_list_called = False
    def GetStringListExpected():
      self.is_get_string_list_called = True
    ua.get_string_list = GetStringListExpected
    admin_rankers.RetrieveUserAgentStringList(ua)
    self.assertTrue(self.is_get_string_list_called)

    params = {}
    response = self.client.get('/admin/ua/rebuild', params)
    self.assertEqual(200, response.status_code)
    self.is_get_string_list_called = False
    admin_rankers.RetrieveUserAgentStringList(ua)
    self.assertFalse(self.is_get_string_list_called)

  def testUserAgentGroupUpdatedForRebuild(self):
    chrome_ua_string = (
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/530.1 '
        '(KHTML, like Gecko) Chrome/2.0.169.1 Safari/530.1')
    ie_ua_string = (
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; '
        '.NET CLR 2.0.50727; .NET CLR 1.1.4322')
    ua = UserAgent.factory(chrome_ua_string)
    ua.update_groups()
    user_agent_strings = UserAgentGroup.GetStrings(0)

    UserAgent.factory(ie_ua_string)
    params = {}
    response = self.client.get('/admin/ua/rebuild', params)
    self.assertEqual(200, response.status_code)

    # IE gets added to groups memcache with '_rebuild' key.
    # Therefore, only the earlier add gets returned at this point.
    self.assertEqual(['Chrome'], UserAgentGroup.GetStrings(0))
    self.assertEqual(['Chrome 2'], UserAgentGroup.GetStrings(1))
    self.assertEqual(['Chrome 2.0'], UserAgentGroup.GetStrings(2))
    self.assertEqual(['Chrome 2.0.169'], UserAgentGroup.GetStrings(3))

    is_done = UserAgentGroup.ReleaseRebuild()
    self.assertTrue(is_done)
    self.assertEqual(['Chrome', 'IE'], UserAgentGroup.GetStrings(0))
    self.assertEqual(['Chrome 2', 'IE 8'], UserAgentGroup.GetStrings(1))
    self.assertEqual(['Chrome 2.0', 'IE 8.0'], UserAgentGroup.GetStrings(2))
    self.assertEqual(['Chrome 2.0.169', 'IE 8.0'], UserAgentGroup.GetStrings(3))

  def testAbandonedUserAgentGroupDeleted(self):
    chrome_ua_string = (
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/530.1 '
        '(KHTML, like Gecko) Chrome/2.0.169.1 Safari/530.1')
    ie_ua_string = (
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; '
        '.NET CLR 2.0.50727; .NET CLR 1.1.4322')
    chrome_ua = UserAgent.factory(chrome_ua_string)
    chrome_ua.update_groups()
    ie_ua = UserAgent.factory(ie_ua_string)
    ie_ua.update_groups()
    user_agent_strings = UserAgentGroup.GetStrings(0)
    UserAgentGroup.UpdateGroups(ie_ua.get_string_list(), is_rebuild=True)
    UserAgentGroup.ReleaseRebuild()
    self.assertEqual(['IE 8.0'], UserAgentGroup.GetStrings(3))
    UserAgentGroup.ClearMemcache(3)
    self.assertEqual(['IE 8.0'], UserAgentGroup.GetStrings(3))


class TestReleaseUserAgentGroups(unittest.TestCase):
  def setUp(self):
    self.client = Client()
    self.old_ReleaseRebuild = UserAgentGroup.ReleaseRebuild

  def tearDown(self):
    UserAgentGroup.ReleaseRebuild = self.old_ReleaseRebuild

  def testReleaseRebuildCalled(self):
    # ReleaseRebuild is tested by testUserAgentGroupUpdatedForRebuild
    self.num_release_rebuild_calls = 0
    @classmethod
    def MockReleaseRebuild(cls):
      self.num_release_rebuild_calls += 1
      return True
    UserAgentGroup.ReleaseRebuild = MockReleaseRebuild
    params = {}
    response = self.client.get('/admin/ua/release', params)
    self.assertEqual(200, response.status_code)
    response_params = simplejson.loads(response.content)
    self.assertTrue(response_params['is_done'])
    self.assertEqual(1, self.num_release_rebuild_calls)
