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

"""Mock out data structures used by the tests."""

__author__ = 'slamm@google.com (Stephen Lamm)'

from google.appengine.ext import db

from categories import test_set_base
from categories import all_test_sets
from models.user_agent import UserAgent
from models.result import ResultParent
from models.result import ResultTime

_UA_STRING = ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) '
              'Gecko/2009011912 Firefox/3.0.6')
def GetUserAgent():
  ua = UserAgent.factory(_UA_STRING)
  return ua


class MockTest(test_set_base.TestBase):
  """Mock test object."""
  def __init__(self, key, name, url, score_type):
    test_set_base.TestBase.__init__(
        self,
        key=key,
        name=name,
        url=url,
        doc='doc',
        score_type=score_type,
        min_value=0,
        max_value=10000)

  def GetScoreAndDisplayValue(self, median):
    if self.key == 'testDisplay':
      return 86, '%iX' % int((median or 0)/100)
    else:
      return None


UNIT_TEST_UA = {'HTTP_USER_AGENT': 'silly-human', 'REMOTE_ADDR': '127.0.0.1'}


TESTS = (
    MockTest('testDisplay', 'Display Block', 'testpage', 'custom'),
    MockTest('testVisibility', 'Visiblility None', 'testpage', 'boolean'),
    )


class MockTestSet(test_set_base.TestSet):
  def __init__(self, category, params=None):
    test_set_base.TestSet.__init__(
        self, category, category, TESTS, {'subnav1': '/url1'},
        "Some Home Intro text", default_params=params)
    all_test_sets.AddTestSet(self)


class MockTestSetWithParseResults(MockTestSet):
  def ParseResults(self, results):
    for result in results:
      # Add the raw value to be expando'd and store a munged value in score.
      result['expando'] = result['score']
      result['score'] = int(round(result['score'] / 2))
    return results


def AddFiveResultsAndIncrementAllCounts():
  test_set = MockTestSet('category')
  user_agent = GetUserAgent()
  result1 = ResultParent()
  result1.category = test_set.category
  result1.user_agent = user_agent
  result1.user_agent_pretty = user_agent.pretty()
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
  result2.category = test_set.category
  result2.user_agent = user_agent
  result2.user_agent_pretty = user_agent.pretty()
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
  result3.category = test_set.category
  result3.user_agent = user_agent
  result3.user_agent_pretty = user_agent.pretty()
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
  result4.category = test_set.category
  result4.user_agent = user_agent
  result4.user_agent_pretty = user_agent.pretty()
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
  result5.category = test_set.category
  result5.user_agent = user_agent
  result5.user_agent_pretty = user_agent.pretty()
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

  return test_set


def AddThreeResultsWithParamsAndIncrementAllCounts():
  test_set = MockTestSet('category-w-params', params=['a=b', 'c=d', 'e=f'])
  user_agent = GetUserAgent()

  result1 = ResultParent()
  result1.category = test_set.category
  result1.user_agent = user_agent
  result1.user_agent_pretty = user_agent.pretty()
  result1.ip = '12.2.2.255'
  result1.params = test_set.default_params
  result1.put()
  result1_time = ResultTime(parent=result1)
  result1_time.test = 'testDisplay'
  result1_time.score = 2
  result1_time.put()
  result1.increment_all_counts()

  result2 = ResultParent()
  result2.category = test_set.category
  result2.user_agent = user_agent
  result2.user_agent_pretty = user_agent.pretty()
  result2.ip = '12.2.2.255'
  result2.params = test_set.default_params
  result2.put()
  result2_time = ResultTime(parent=result2)
  result2_time.test = 'testDisplay'
  result2_time.score = 1
  result2_time.put()
  result2.increment_all_counts()

  result3 = ResultParent()
  result3.category = test_set.category
  result3.user_agent = user_agent
  result3.user_agent_pretty = user_agent.pretty()
  result3.ip = '12.2.2.255'
  result3.params = test_set.default_params
  result3.put()
  result3_time = ResultTime(parent=result3)
  result3_time.test = 'testDisplay'
  result3_time.score = 200
  result3_time.put()
  result3.increment_all_counts()
  return test_set

def AddOneTest():
  test_set = MockTestSet('category-one')
  user_agent = GetUserAgent()
  result = ResultParent()
  result.category = test_set.category
  result.user_agent = user_agent
  result.user_agent_pretty = user_agent.pretty()
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
  return test_set

def AddOneTestUsingAddResult():
  test_set = MockTestSet('category-addresult')
  ip = '12.2.2.555'
  user_agent_string = _UA_STRING
  results = [{'key': 'testDisplay', 'score': 500},
             {'key': 'testVisibility', 'score': 200}]
  parent = ResultParent.AddResult(test_set, ip, user_agent_string, results)
  return parent

def AddOneTestUsingAddResultWithParseResults():
  test_set = MockTestSetWithParseResults('category-addresult-withparseresults')
  ip = '12.2.2.555'
  user_agent_string = _UA_STRING
  results = [{'key': 'testDisplay', 'score': 500},
             {'key': 'testVisibility', 'score': 200}]
  parent = ResultParent.AddResult(test_set, ip, user_agent_string, results)
  return parent

def AddOneTestUsingAddResultWithExpando():
  test_set = MockTestSet('category-addresult-withexpando')
  ip = '12.2.2.555'
  user_agent_string = _UA_STRING
  results = [{'key': 'testDisplay', 'score': 500, 'expando': 20},
             {'key': 'testVisibility', 'score': 200, 'expando': 'testeroo'}]
  parent = ResultParent.AddResult(test_set, ip, user_agent_string, results)
  return parent
