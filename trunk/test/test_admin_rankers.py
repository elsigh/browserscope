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
    self.assertEqual(1, ranker.TotalRankedScores())
    self.assertEqual(500, ranker.GetMedian())

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
    self.assertEqual(3, ranker.TotalRankedScores())
    self.assertEqual(300, ranker.GetMedian())

    ranker = result_ranker.ResultRanker.Get(
        'catogrey', test_set.GetTest('testVisibility'), 'Firefox',
        params_str=params_str, ranker_version='next')
    self.assertEqual(5, ranker.TotalRankedScores())
    self.assertEqual(2, ranker.GetMedian())


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
      self.assertEqual(score, ranker.GetMedian())

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
      self.assertEqual(score, ranker.GetMedian())
