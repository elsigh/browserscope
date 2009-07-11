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
import logging

from google.appengine.ext import db

from models.user_agent import UserAgent
from models.result import ResultParent
from models.result import ResultTime


def GetUserAgent():
  ua_string = ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) '
               'Gecko/2009011912 Firefox/3.0.6')
  ua = UserAgent.factory(ua_string)
  return ua


FIVE_TEST_CATEGORY = 'category'
def AddFiveResultsAndIncrementAllCounts():
  user_agent = GetUserAgent()

  result1 = ResultParent()
  result1.category = FIVE_TEST_CATEGORY
  result1.user_agent = user_agent
  result1.user_agent_list = user_agent.get_string_list()
  result1.ip = '12.2.2.255'
  result1.put()
  result1_time1 = ResultTime(parent=result1)
  result1_time1.test = 'testDisplay'
  result1_time1.score = 500
  result1_time2 = ResultTime(parent=result1)
  result1_time2.test = 'testVisibility'
  result1_time2.score = 0
  db.put([result1_time1, result1_time2])
  result1.increment_all_counts()

  result2 = ResultParent()
  result2.category = FIVE_TEST_CATEGORY
  result2.user_agent = user_agent
  result2.user_agent_list = user_agent.get_string_list()
  result2.ip = '12.2.2.255'
  result2.put()
  result2_time1 = ResultTime(parent=result2)
  result2_time1.test = 'testDisplay'
  result2_time1.score = 200
  result2_time2 = ResultTime(parent=result2)
  result2_time2.test = 'testVisibility'
  result2_time2.score = 1
  db.put([result2_time1, result2_time2])
  result2.increment_all_counts()

  result3 = ResultParent()
  result3.category = FIVE_TEST_CATEGORY
  result3.user_agent = user_agent
  result3.user_agent_list = user_agent.get_string_list()
  result3.ip = '12.2.2.255'
  result3.put()
  result3_time = ResultTime(parent=result3)
  result3_time.test = 'testDisplay'
  result3_time.score = 300
  result3_time.put()
  result3_time = ResultTime(parent=result3)
  result3_time.test = 'testVisibility'
  result3_time.score = 2
  result3_time.put()
  result3.increment_all_counts()

  result4 = ResultParent()
  result4.category = FIVE_TEST_CATEGORY
  result4.user_agent = user_agent
  result4.user_agent_list = user_agent.get_string_list()
  result4.ip = '12.2.2.255'
  result4.put()
  result4_time = ResultTime(parent=result4)
  result4_time.test = 'testDisplay'
  result4_time.score = 100
  result4_time.put()
  result4_time = ResultTime(parent=result4)
  result4_time.test = 'testVisibility'
  result4_time.score = 3
  result4_time.put()
  result4.increment_all_counts()

  result5 = ResultParent()
  result5.category = FIVE_TEST_CATEGORY
  result5.user_agent = user_agent
  result5.user_agent_list = user_agent.get_string_list()
  result5.ip = '12.2.2.255'
  result5.put()
  result5_time = ResultTime(parent=result5)
  result5_time.test = 'testDisplay'
  result5_time.score = 400
  result5_time.put()
  result5_time = ResultTime(parent=result5)
  result5_time.test = 'testVisibility'
  result5_time.score = 4
  result5_time.put()
  result5.increment_all_counts()


THREE_TEST_CATEGORY = 'category-w-params'
THREE_TEST_PARAMS = ['a=b', 'c=d', 'e=f']
def AddThreeResultsWithParamsAndIncrementAllCounts():
  user_agent = GetUserAgent()

  result1 = ResultParent()
  result1.category = THREE_TEST_CATEGORY
  result1.user_agent = user_agent
  result1.user_agent_list = user_agent.get_string_list()
  result1.ip = '12.2.2.255'
  result1.params = THREE_TEST_PARAMS
  result1.put()
  result1_time = ResultTime(parent=result1)
  result1_time.test = 'testDisplay'
  result1_time.score = 2
  result1_time.put()
  result1.increment_all_counts()

  result2 = ResultParent()
  result2.category = THREE_TEST_CATEGORY
  result2.user_agent = user_agent
  result2.user_agent_list = user_agent.get_string_list()
  result2.ip = '12.2.2.255'
  result2.params = THREE_TEST_PARAMS
  result2.put()
  result2_time = ResultTime(parent=result2)
  result2_time.test = 'testDisplay'
  result2_time.score = 1
  result2_time.put()
  result2.increment_all_counts()

  result3 = ResultParent()
  result3.category = THREE_TEST_CATEGORY
  result3.user_agent = user_agent
  result3.user_agent_list = user_agent.get_string_list()
  result3.ip = '12.2.2.255'
  result3.params = THREE_TEST_PARAMS
  result3.put()
  result3_time = ResultTime(parent=result3)
  result3_time.test = 'testDisplay'
  result3_time.score = 200
  result3_time.put()
  result3.increment_all_counts()


ONE_TEST_CATEGORY = 'category-one'
def AddOneTest():
  user_agent = GetUserAgent()
  result = ResultParent()
  result.category = ONE_TEST_CATEGORY
  result.user_agent = user_agent
  result.user_agent_list = user_agent.get_string_list()
  result.ip = '12.2.2.255'
  result.put()
  result_time1 = ResultTime(parent=result)
  result_time1.test = 'testDisplay'
  result_time1.score = 500
  result_time2 = ResultTime(parent=result)
  result_time2.test = 'testVisibility'
  result_time2.score = 0
  db.put([result_time1, result_time2])
  result.increment_all_counts()


class ResultTest(unittest.TestCase):

  def test_guid(self):
    guid = ResultParent.guid('category', 'test', 'user_agent_version')
    self.assertEqual('category_test_user_agent_version', guid)

  def test_guid_with_params(self):
    guid = ResultParent.guid('category', 'test', 'user_agent_version',
                             ['param1=val1', 'param2=val2', 'param3=val3'])
    self.assertEqual(
        'category_test_user_agent_version_1c565ba4056b84201ed4fe4c4b6b2e42',
        guid)

  def test_get_total(self):
    AddOneTest()

    guid = ResultParent.guid(ONE_TEST_CATEGORY, 'testDisplay', 'Firefox 3')
    self.assertEqual(1, ResultParent.get_total(guid))

    guid = ResultParent.guid(ONE_TEST_CATEGORY, 'testDisplay', 'Firefox 3.0')
    self.assertEqual(1, ResultParent.get_total(guid))

    guid = ResultParent.guid(ONE_TEST_CATEGORY, 'testVisibility', 'Firefox 3')
    self.assertEqual(1, ResultParent.get_total(guid))

    guid = ResultParent.guid(ONE_TEST_CATEGORY, 'testDisplay', 'Firefox 3.0.6')
    self.assertEqual(1, ResultParent.get_total(guid))


  def test_get_median(self):

    AddFiveResultsAndIncrementAllCounts()

    guid = ResultParent.guid(FIVE_TEST_CATEGORY, 'testDisplay', 'Firefox 3')
    self.assertEqual(300, ResultParent.get_median(guid))

    guid = ResultParent.guid(FIVE_TEST_CATEGORY, 'testVisibility', 'Firefox 3')
    self.assertEqual(2, ResultParent.get_median(guid))

    # Passing in return_total as second param.
    self.assertEqual(5, ResultParent.get_median(guid, True)[1])


  def test_get_median_with_params(self):
    AddThreeResultsWithParamsAndIncrementAllCounts()

    guid = ResultParent.guid(THREE_TEST_CATEGORY, 'testDisplay',
                         'Firefox 3', THREE_TEST_PARAMS)
    self.assertEqual(2, ResultParent.get_median(guid))

