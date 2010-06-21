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

import logging

from google.appengine.ext import db

from categories import test_set_base
from categories import all_test_sets
from models.user_agent import UserAgent
from models import user_test

def GetUserAgentString(browser):
  browser_user_agents = {
      'Firefox 2.5.1': ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) '
                        'Gecko/2009011912 Firefox/2.5.1'),
      'Firefox 3.0.7': ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) '
                        'Gecko/2009011912 Firefox/3.0.7'),
      'Firefox 3.1.7': ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) '
                        'Gecko/2009011912 Firefox/3.1.7'),
      'Firefox 3.1.8': ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) '
                        'Gecko/2009011912 Firefox/3.1.8'),
      'Firefox 3.5': ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) '
                        'Gecko/2009011912 Firefox/3.5'),
      'IE 7.0': ('Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; '
                 'Trident/4.0; .NET CLR 2.0.50727; .NET CLR 1.1.4322; '
                 '.NET CLR 3.0.04506.648; .NET CLR 3.5.21022)'),
      'Opera 9.70': ('Opera/9.70 (Linux ppc64 ; U; en) Presto/2.2.1'),
      'Opera Mini 4.0.10031': ('Opera/9.50 (J2ME/MIDP; '
                               'Opera Mini/4.0.10031/298; U; en)'),
      }
  return browser_user_agents[browser]

def GetUserAgent(browser):
  return UserAgent.factory(GetUserAgentString(browser))

UNIT_TEST_UA = {'HTTP_USER_AGENT': 'silly-human', 'REMOTE_ADDR': '127.0.0.1'}


class MockTest(test_set_base.TestBase):
  """Mock test object."""
  def __init__(self, key, min_value, max_value, **kwds):
    test_set_base.TestBase.__init__(
        self,
        key=key,
        name='name for %s' % key,
        url='url for %s' % key,
        doc='doc for %s' % key,
        min_value=min_value,
        max_value=max_value,
        **kwds)


class MockTestSet(test_set_base.TestSet):
  def __init__(self, category='mockTestSet', params=None):
    tests = (
        MockTest('apple', min_value=0, max_value=1),
        MockTest('banana', min_value=0, max_value=100),
        MockTest('coconut', min_value=0, max_value=1000),
        )
    test_set_base.TestSet.__init__(
        self, category, category.capitalize(), '', tests, default_params=params)

  def GetTestScoreAndDisplayValue(self, test_key, raw_scores):
    raw_score = raw_scores[test_key]
    score = raw_score * 2
    display = 'd:%s' % str(score)
    return score, display

  def GetRowScoreAndDisplayValue(self, results):
    score = sum(x['score'] for x in results.values())
    display = str(sum(x['raw_score'] for x in results.values()))
    return score, display


class MockUserTestSet(test_set_base.TestSet):
  def __init__(self, category='mockTestSet', params=None):
    # matches user_test max_value
    tests = (
        MockTest('apple', min_value=0, max_value=user_test.MAX_VALUE),
        MockTest('banana', min_value=0, max_value=user_test.MAX_VALUE),
        MockTest('coconut', min_value=0, max_value=user_test.MAX_VALUE),
        )
    test_set_base.TestSet.__init__(
        self, category, category.capitalize(), '', tests, default_params=params)

  def GetTestScoreAndDisplayValue(self, test_key, raw_scores):
    raw_score = raw_scores[test_key]
    score = raw_score * 2
    display = 'd:%s' % str(score)
    logging.info('GetTestScoreAndDisplayValue %s: %s - %s' % (test_key, score, display))
    return score, display

  def GetRowScoreAndDisplayValue(self, results):
    score = sum(x['score'] for x in results.values())
    display = str(sum(x['raw_score'] for x in results.values()))
    logging.info('GetRowScoreAndDisplayValue %s, %s' % (score, display))
    return score, display