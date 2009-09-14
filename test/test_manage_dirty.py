#!/usr/bin/python2.4
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

"""Shared Models Unit Tests."""

__author__ = 'elsigh@google.com (Lindsey Simon)'

import unittest

from google.appengine.ext import db
from django.test.client import Client

from base import manage_dirty

from models import result_ranker
from models.result import ResultParent
from models.result import ResultTime
from models.user_agent import UserAgent

import mock_data

class TestManageDirty(unittest.TestCase):

  CATEGORY = 'test_manage_dirty'

  def setUp(self):
    self.old_limit = manage_dirty.UPDATE_DIRTY_RESULT_TIME_LIMIT
    self.client = Client()

  def tearDown(self):
    """Need to clean up it seems."""
    manage_dirty.UPDATE_DIRTY_RESULT_TIME_LIMIT = self.old_limit
    query = db.GqlQuery("SELECT __key__ FROM ResultParent WHERE category = :1",
                        self.CATEGORY)
    for parent_key in query.fetch(1000):
      query = db.GqlQuery("SELECT __key__ FROM ResultTime WHERE ANCESTOR IS :1",
                          parent_key)
      result_time_keys = query.fetch(1000)
      db.delete(result_time_keys + [parent_key])

  def testUpdateDirtyLocked(self):
    manage_dirty.UpdateDirtyController.AcquireLock()
    response = self.client.get('/admin/update_dirty', {},
        **mock_data.UNIT_TEST_UA)
    self.assertEqual(200, response.status_code)
    self.assertTrue(response.content.find('unable to acquire lock') > -1,
                    'content: %s' % response.content)
    manage_dirty.UpdateDirtyController.ReleaseLock()

  def testUpdateDirty(self):
    # First, create a "dirty" ResultParent
    ua_string = ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) '
                 'Gecko/2009011912 Firefox/3.0.6')

    test_set = mock_data.MockTestSet(self.CATEGORY)
    category = self.CATEGORY
    ResultParent.AddResult(test_set, '12.2.2.11', ua_string,
                           'testDisplay=500,testVisibility=3')

    response = self.client.get('/admin/update_dirty', {},
        **mock_data.UNIT_TEST_UA)
    self.assertEqual(200, response.status_code)
    self.assertEqual(manage_dirty.UPDATE_DIRTY_DONE, response.content)

    response = self.client.get('/admin/update_dirty', {},
        **mock_data.UNIT_TEST_UA)
    self.assertEqual(200, response.status_code)
    self.assertEqual(manage_dirty.UPDATE_DIRTY_DONE, response.content)

    query = db.Query(ResultParent)
    result_parent = query.get()
    result_times = ResultTime.all().ancestor(result_parent)
    self.assertEqual([False, False],
                     [x.dirty for x in result_times])

    ranker = result_ranker.GetRanker(
        category, test_set.GetTest('testDisplay'), 'Firefox 3')
    self.assertEqual(1, ranker.TotalRankedScores())
    self.assertEqual(500, ranker.GetMedian())

  def testUpdateDirtyOverMultipleRequests(self):
    # First, create a "dirty" ResultParent
    manage_dirty.UPDATE_DIRTY_RESULT_TIME_LIMIT = 1
    ua_string = ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) '
                 'Gecko/2009011912 Firefox/3.0.6')

    test_set = mock_data.MockTestSet(self.CATEGORY)
    category = self.CATEGORY
    ResultParent.AddResult(test_set, '12.2.2.11', ua_string,
                           'testDisplay=500,testVisibility=3')

    response = self.client.get('/admin/update_dirty', {},
        **mock_data.UNIT_TEST_UA)
    self.assertEqual(200, response.status_code)
    self.assertEqual(manage_dirty.UPDATE_DIRTY_ADDED_TASK, response.content)

    response = self.client.get('/admin/update_dirty', {},
        **mock_data.UNIT_TEST_UA)
    self.assertEqual(200, response.status_code)
    self.assertEqual(manage_dirty.UPDATE_DIRTY_DONE, response.content)

    query = db.Query(ResultParent)
    result_parent = query.get()
    result_times = ResultTime.all().ancestor(result_parent)
    self.assertEqual([False, False],
                     [x.dirty for x in result_times])

    ranker = result_ranker.GetRanker(
        category, test_set.GetTest('testDisplay'), 'Firefox 3')
    self.assertEqual(1, ranker.TotalRankedScores())
    self.assertEqual(500, ranker.GetMedian())

if __name__ == '__main__':
  unittest.main()
