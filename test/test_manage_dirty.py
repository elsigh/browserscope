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

"""Shared Models Unit Tests."""

__author__ = 'elsigh@google.com (Lindsey Simon)'

import logging
import unittest

from google.appengine.ext import db
from django.test.client import Client

from base import manage_dirty

from categories import all_test_sets
from models import result_ranker
from models.result import ResultParent
from models.result import ResultTime
from models.user_agent import UserAgent
from third_party import mox

import mock_data

class TestManageDirty(unittest.TestCase):

  CATEGORY = 'test_manage_dirty'

  def setUp(self):
    self.client = Client()
    self.test_set = mock_data.MockTestSet(self.CATEGORY)
    all_test_sets.AddTestSet(self.test_set)
    self.mox = mox.Mox()

  def tearDown(self):
    """Need to clean up it seems."""
    all_test_sets.RemoveTestSet(self.test_set)
    self.mox.UnsetStubs()

  def testUpdateDirtyGeneral(self):
    ua_string = ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) '
                 'Gecko/2009011912 Firefox/3.0.6')

    self.mox.StubOutWithMock(manage_dirty, 'ScheduleCategoryUpdate')
    manage_dirty.ScheduleCategoryUpdate(mox.IgnoreArg())
    self.mox.ReplayAll()
    # AddResult schedules the dirty update.
    result_parent = ResultParent.AddResult(
        self.test_set, '12.2.2.11', ua_string, 'apple=0,banana=99,coconut=101')
    self.mox.VerifyAll()
    self.assertEqual([False, False, False],
                     [x.dirty for x in result_parent.GetResultTimes()])

  def xxxNOT_WORKING_YETxxxtestUpdateDirtyWithResultTimeKey(self):
    ua_string = ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) '
                 'Gecko/2009011912 Firefox/3.0.6')
    result_parent = ResultParent.AddResult(
        self.test_set, '12.2.2.11', ua_string, 'apple=0,banana=99,coconut=101',
        skip_update_dirty=True)
    skip_rt, update_rt, next_rt = result_parent.GetResultTimes()

    # Make so there is only one ResultTime to schedule after first update.
    skip_rt.dirty = False
    skip_rt.put()

    self.mox.StubOutWithMock(ResultTime, 'UpdateStats')
    self.mox.StubOutWithMock(ResultParent, 'ScheduleUpdateDirty')

    ResultTime.UpdateStats(update_rt)
    ResultParent.ScheduleUpdateDirty(next_rt.key())

    self.mox.ReplayAll()
    response = self.client.get('/admin/update_dirty/some_category',
                               {'result_time_key': update_rt.key()},
                               **mock_data.UNIT_TEST_UA)
    self.mox.VerifyAll()


# TODO: Add more tests
#   * Call UpdateDirty with result_time_key
#     - Only update times under same parent
#   * Call UpdateDirty with result_parent_key
#   * Call UpdateDirty with no params
#   * Make sure schedule next is called
#   * Make sure category update


if __name__ == '__main__':
  unittest.main()
