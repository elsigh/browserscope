from google.appengine.ext import db

from controllers import test_set_base
from controllers import all_test_sets
from models.user_agent import UserAgent
from models.result import ResultParent
from models.result import ResultTime


def GetUserAgent():
  ua_string = ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) '
               'Gecko/2009011912 Firefox/3.0.6')
  ua = UserAgent.factory(ua_string)
  return ua


class MockTest(object):
  """Mock test object."""
  def __init__(self, key, name, url, score_type):
    self.key = key
    self.name = name
    self.url = url
    self.score_type = score_type
    self.min_value = 0
    self.max_value = 10000

  def GetScoreAndDisplayValue(self, median):
    if self.key == 'testDisplay':
      return 86, '%iX' % int((median or 0)/100)
    else:
      return None


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
