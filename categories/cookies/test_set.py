#!/usr/bin/python2.5
#
# Copyright 2009 Palm Inc.
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

"""Cookies Tests Definitions."""

import logging

from categories import test_set_base
from base import util


_CATEGORY = 'cookies'


class CookiesTest(test_set_base.TestBase):
  TESTS_URL_PATH = '/%s/tests' % _CATEGORY

  def __init__(self, key, name, url_name, doc,
               value_range=None, is_hidden_stat=False, cell_align='center', 
               url_prepend='', halt_tests_on_fail=False):
    """Initialze a cookies test.

    Args:
      key: key for this in dict's
      name: a human readable label for display
      url_name: the name used in the url
      doc: a description of the test
      value_range: (min_value, max_value) as integer values
      is_hidden_stat: whether or not the test shown in the stats table
      halt_tests_on_fail: whether to kill the whole test run if this test fails
    """
    self.url_name = url_name
    self.is_hidden_stat = is_hidden_stat
    test_set_base.TestBase.__init__(
        self,
        key=key,
        name=name,
        url='/%s/test?testurl=%s' % (_CATEGORY, url_name),
        doc=doc,
        min_value=value_range[0],
        max_value=value_range[1],
        cell_align=cell_align,
        url_prepend=url_prepend,
        halt_tests_on_fail=halt_tests_on_fail)



"""
Initial list of tests to include, in no particular order:
    * Max size of a single cookie.
    * Max number of cookies for a single host.
    * Max number of cookies across all hosts (though this may require a large 
        number of hosts).
    * Max number of cookies across all subdomain/path combinations of a single 
        host (if different from single-host).
    * Max size of all cookies for a single host (perhaps with subdomain/path 
        combinations as well).
    * Whether the browser honors the secure (encrypted sessions only) flag.
    * Whether the browser honors the expiration date (most easily tested by 
        setting it into the past, though maybe set one at the beginning of all 
        tests 30 seconds or so into the future).
"""


CLEAR_COOKIES_URL = '/cookies/tests/clear-cookies?reset=1&redirect_to='

_TESTS = (
  # key, name, url_name, score_type, doc
  # Because we depend on being able to delete cookies, if this test fails
  # then most of the others won't work properly, so we should just halt
  # testing.
  CookiesTest(
    'expires', 'Cookie Expiration', 'expires',
    '''Determine whether the browser correctly expires cookies.''',
    value_range=(0, 1),
    url_prepend=CLEAR_COOKIES_URL,
    halt_tests_on_fail=True),
  CookiesTest(
    'maxPerHost', 'Max Per Host', 'max-per-host',
    '''Determine the maximum number of cookies that a single host can set and 
retrieve.''',
    value_range=(0, 60000),  #TODO(eric): different default for range here?
    url_prepend=CLEAR_COOKIES_URL),
  CookiesTest(
    'maxNameSize', 'Max Name Size', 'max-name-size',
    '''Determine the maximum length of the name of a single cookie that can be 
set and retrieved.''',
    value_range=(0, 60000),  #TODO(eric): different default for range here?
    url_prepend=CLEAR_COOKIES_URL),
  CookiesTest(
    'maxValueSize', 'Max Value Size', 'max-value-size',
    '''Determine the maximum length of the value of a single cookie that can be 
set and retrieved.''',
    value_range=(0, 60000),  #TODO(eric): different default for range here?
    url_prepend=CLEAR_COOKIES_URL),
  CookiesTest(
    'maxTotalSize', 'Max Total Size', 'max-total-size',
    '''Determine the maximum length of the name and value of a single cookie 
that can be set and retrieved.''',
    value_range=(0, 60000),  #TODO(eric): different default for range here?
    url_prepend=CLEAR_COOKIES_URL),
)


class CookiesTestSet(test_set_base.TestSet):

  def GetTestScoreAndDisplayValue(self, test_key, raw_scores):
    """Get a normalized score (0 to 100) and a value to output to the display.

    Args:
      test_key: a key for a test_set test.
      raw_scores: a dict of raw_scores indexed by test keys.
    Returns:
      score, display_value
          # score is from 0 to 100.
          # display_value is the text for the cell.
    """
    #logging.info('Cookies.GetScoreAndDisplayValue '
    #             'test: %s, median: %s, medians: %s' % (self.key, median, 
    #             len(medians)))

    #TODO(eric): change this method
    median = raw_scores[test_key]
    score = 0
    if 'hostconn' == test_key:
      if median > 2:
        score = 100
      elif median == 2:
        score = 50
      else:
        score = 0

    elif 'maxconn' == test_key:
      if median > 20:
        score = 100
      elif median >= 10:
        score = 50
      else:
        score = 0
    return score, str(median)

  def GetRowScoreAndDisplayValue(self, results):
    """Get the overall score for this row of results data.

    Args:
      results: {
          'test_key_1': {'score': score_1, 'raw_score': raw_score_1, ...},
          'test_key_2': {'score': score_2, 'raw_score': raw_score_2, ...},
          ...
          }
    Returns:
      score, display_value
          # score is from 0 to 100.
          # display_value is the text for the cell.

    Why do we use totalTests as the divisor for "score", but totalValidTests as
    the divisor for "display"?
    There are going to be old browsers that are no longer tested. They might 
    have gotten 6/8 (75%) back in the old days, but now we've added more tests 
    and they'd be lucky to get 6/12 (50%). If we compare 6/8 to newer browsers 
    that get 8/12, the old browser would win, even though it would fail in 
    side-by-side testing, so we have to use totalTests as the divisor for 
    "score". But we can't misrepresent the actual tests that were performed, so
    we have to show the user the actual number of tests for which we have 
    results, which means using totalValidTests as the divisor for "display".

    """
    #logging.info('cookies getrowscore results: %s' % results)

    #TODO(eric): change this method

    total_tests = 0
    total_valid_tests = 0
    total_score = 0
    for test in self.VisibleTests():
      total_tests += 1
      if test.key in results:
        score = results[test.key]['score']
        #logging.info('test: %s, score: %s' % (test.key, score))
        total_valid_tests += 1
        # boolean 1 = 100, and steve's custom score for hostconn & maxconn map
        # simply to 100 for good, 50 for ok, and 0 for fail, but we only award
        # a point for a 100 on those.
        if score == 100:
          total_score += 1

    #logging.info('%s, %s, %s' % (total_score, total_tests, total_valid_tests))
    score = int(round(100 * total_score / total_tests))
    display = '%s/%s' % (total_score, total_valid_tests)

    return score, display


TEST_SET = CookiesTestSet(
    category=_CATEGORY,
    category_name='Cookies',
    tests=_TESTS,
#    test_page='http://mirrorrr.browsersrc.com/www.browserscope.org' + \
#                util.MULTI_TEST_DRIVER_TEST_PAGE
    test_page=util.MULTI_TEST_DRIVER_TEST_PAGE
)
