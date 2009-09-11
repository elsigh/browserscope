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
from categories import test_set_params
from categories import all_test_sets
from models.user_agent import UserAgent
from models.result import ResultParent
from models.result import ResultTime

def GetUserAgentString():
  return ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) '
          'Gecko/2009011912 Firefox/3.0.6')

def GetUserAgent():
  return UserAgent.factory(GetUserAgentString())

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

  def GetScoreAndDisplayValue(self, median, medians=None, is_uri_result=False):
    """Custom scoring function.

    Args:
      median: The actual median for this test from all scores.
      medians: A dict of the medians for all tests indexed by key.
      is_uri_result: Boolean, if results are in the url, i.e. home page.
    Returns:
      (score, display)
      Where score is a value between 1-100.
      And display is the text for the cell.
    """
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
        self, category, category, TESTS, default_params=params)
    all_test_sets.AddTestSet(self)


class MockTestSetWithAdjustResults(MockTestSet):
  def AdjustResults(self, results):
    for result in results:
      # Add the raw value to be expando'd and store a munged value in score.
      result['expando'] = result['score']
      result['score'] = int(round(result['score'] / 2))
    return results


def AddFiveResultsAndIncrementAllCounts():
  test_set = MockTestSet('category')
  for scores in ((500, 0), (200, 1), (300, 2), (100, 3), (400, 4)):
    result = ResultParent.AddResult(test_set, '12.2.2.25', GetUserAgentString(),
                                    'testDisplay=%s,testVisibility=%s' % scores)
    result.increment_all_counts()
  return test_set

def AddThreeResultsWithParamsAndIncrementAllCounts():
  test_set = MockTestSet(
      'category-w-params',
      params=test_set_params.Params('w-params', 'a=b', 'c=d', 'e=f'))
  params_str = str(test_set.default_params)
  for scores in ((2, 0), (1, 1), (200, 2)):
    result = ResultParent.AddResult(test_set, '12.2.2.25', GetUserAgentString(),
                                    'testDisplay=%s,testVisibility=%s' % scores,
                                    params_str=params_str)
    result.increment_all_counts()
  return test_set

def AddOneTest():
  test_set = MockTestSet('category-one')
  result = ResultParent.AddResult(test_set, '12.2.2.25', GetUserAgentString(),
                                  'testDisplay=500,testVisibility=0')
  result.increment_all_counts()
  return test_set

def AddOneTestUsingAddResult():
  test_set = MockTestSet('category-addresult')
  result = ResultParent.AddResult(test_set, '12.2.2.25', GetUserAgentString(),
                                  'testDisplay=500,testVisibility=200')
  return result

def AddOneTestUsingAddResultWithAdjustResults():
  test_set = MockTestSetWithAdjustResults('category-addresult-withparseresults')
  result = ResultParent.AddResult(test_set, '12.2.2.25', GetUserAgentString(),
                                  'testDisplay=500,testVisibility=200')
  return result

def AddOneTestUsingAddResultWithExpando():
  test_set = MockTestSet('category-addresult-withexpando')
  def AdjustResults(results):
    for result in results:
      if result['key'] == 'testDisplay':
        result['expando'] = 20
      elif result['key'] == 'testVisibility':
        result['expando'] = 'testeroo'
    return results
  test_set.AdjustResults = AdjustResults
  parent = ResultParent.AddResult(test_set, '12.2.2.25', GetUserAgentString(),
                                  'testDisplay=500,testVisibility=200')
  return parent
