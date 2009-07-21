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

"""Shared Models Unit Tests."""

__author__ = 'elsigh@google.com (Lindsey Simon)'

import unittest
import random
import logging

from google.appengine.ext import db
from google.appengine.api import memcache
from django.http import HttpRequest
from django.test.client import Client

from base import cron
from base import util

from models import result_ranker
from models.result import ResultParent
from models.result import ResultTime
from models.user_agent import UserAgent

import mock_data

class TestCron(unittest.TestCase):

  CATEGORY = 'test_cron_dirty'

  def setUp(self):
    self.client = Client()

  def tearDown(self):
    """Need to clean up it seems."""
    query = db.GqlQuery("SELECT __key__ FROM ResultParent WHERE category = :1",
                        self.CATEGORY)
    for parent_key in query.fetch(1000, 0):
      query = db.GqlQuery("SELECT __key__ FROM ResultTime WHERE ANCESTOR IS :1",
                          parent_key)
      result_time_keys = query.fetch(1000, 0)
      for key in result_time_keys:
         memcache.delete(key='cron_' + str(key), seconds=0,
                         namespace=cron.UPDATE_DIRTY_MEMCACHE_NS)
      db.delete(result_time_keys + [parent_key])

  def testCronUpdateDirty(self):
    # First, create a "dirty" ResultParent
    ua_string = ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) '
                 'Gecko/2009011912 Firefox/3.0.6')
    user_agent = UserAgent.factory(ua_string)

    test_set = mock_data.MockTestSet(self.CATEGORY)
    category = self.CATEGORY
    result_parent1 = ResultParent()
    result_parent1.category = category
    result_parent1.user_agent = user_agent
    result_parent1.user_agent_pretty = user_agent.pretty()
    result_parent1.put()

    result_time1 = ResultTime(parent=result_parent1)
    result_time1.test = 'testDisplay'
    result_time1.score = 500
    result_time1.put()

    result_time2 = ResultTime(parent=result_parent1)
    result_time2.test = 'testVisibility'
    result_time2.score = 3
    result_time2.put()

    # Run it twice for the two ResultTimes
    response = self.client.get('/cron/update_dirty', {},
        **mock_data.UNIT_TEST_UA)
    self.assertEqual(200, response.status_code)
    logging.info('CONTENT: %s' % response.content)
    self.assertTrue(response.content.find('done') > -1)

    # Fake a mutex lock to see if we bail when we see one.
    memcache_keyname1 = 'cron_' + str(result_time1.key())
    memcache_keyname2 = 'cron_' + str(result_time2.key())
    memcache.set_multi(mapping={memcache_keyname1:1, memcache_keyname2:1},
                       time=30,
                       namespace=cron.UPDATE_DIRTY_MEMCACHE_NS)
    response = self.client.get('/cron/update_dirty', {},
        **mock_data.UNIT_TEST_UA)
    self.assertEqual(403, response.status_code)
    self.assertTrue(response.content.find('unable to acquire lock') > -1)

    # Fix the mutex and now we should be able to finish.
    memcache.delete_multi(keys=[memcache_keyname1, memcache_keyname2],
                          seconds=0,
                          namespace=cron.UPDATE_DIRTY_MEMCACHE_NS)

    response = self.client.get('/cron/update_dirty', {},
        **mock_data.UNIT_TEST_UA)
    self.assertEqual(200, response.status_code)
    self.assertTrue(response.content.find('done') > -1)

    # Should now return empty
    response = self.client.get('/cron/update_dirty', {},
        **mock_data.UNIT_TEST_UA)
    self.assertEqual(200, response.status_code)
    self.assertEqual(cron.UPDATE_DIRTY_DONE, response.content)

    query = db.Query(ResultParent)
    result_parent = query.get()
    result_times = ResultTime.all().ancestor(result_parent)
    for result_time in result_times:
      self.assertFalse(result_time.dirty)

    ranker = result_ranker.Factory(
        category, test_set.GetTest('testDisplay'), 'Firefox 3')
    self.assertEqual(1, ranker.TotalRankedScores())
    self.assertEqual(500, ranker.GetMedian())


if __name__ == '__main__':
  unittest.main()
