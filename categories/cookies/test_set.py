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


_CATEGORY = 'cookies'


class CookiesTest(test_set_base.TestBase):
  TESTS_URL_PATH = '/%s/tests' % _CATEGORY

  def __init__(self, key, name, url_name, score_type, doc,
               value_range=None, is_hidden_stat=False, cell_align='center', 
               halt_tests_on_fail=False):
    """Initialze a cookies test.

    Args:
      key: key for this in dict's
      name: a human readable label for display
      url_name: the name used in the url
      score_type: 'boolean' or 'custom'
      doc: a description of the test
      value_range: (min_value, max_value) as integer values
      is_hidden_stat: whether or not the test shown in the stats table
      halt_tests_on_fail: whether to kill the whole test run if this test fails
    """
    self.url_name = url_name
    self.is_hidden_stat = is_hidden_stat
    # must use 0 and 1 so that the javascript side can use it
    if halt_tests_on_fail:
      self.halt_tests_on_fail = 1
    else:
      self.halt_tests_on_fail = 0
    
    if value_range:
      min_value, max_value = value_range
    elif score_type == 'boolean':
      min_value, max_value = 0, 1
    else:
      #TODO(eric): different default for range here?
      min_value, max_value = 0, 60
    test_set_base.TestBase.__init__(
        self,
        key=key,
        name=name,
        url='%s/test?testurl=%s' % (_CATEGORY, url_name),
        score_type=score_type,
        doc=doc,
        min_value=min_value,
        max_value=max_value,
        cell_align=cell_align)


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
    #logging.info('Cookies.GetScoreAndDisplayValue '
    #             'test: %s, median: %s, medians: %s' % (self.key, median, 
    #             len(medians)))

    #TODO(eric): change this method

    score = 0
    if 'hostconn' == self.key:
      if median > 2:
        score = 100
      elif median == 2:
        score = 50
      else:
        score = 0

    elif 'maxconn' == self.key:
      if median > 20:
        score = 100
      elif median >= 10:
        score = 50
      else:
        score = 0
    return score, str(median)


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


_TESTS = (
  # key, name, url_name, score_type, doc
  CookiesTest(
    'expires', 'Cookie Expiration', 'expires', 'boolean',
    '''Determine whether the browser correctly expires cookies.''',
    # Because we depend on being able to delete cookies, if this test fails 
    # then most of the others won't work properly, so we should just halt 
    # testing.
    halt_tests_on_fail=True),
  CookiesTest(
    'maxPerHost', 'Max Per Host', 'max-per-host', 'custom',
    '''Determine the maximum number of cookies that a single host can set and 
retrieve.''',
    #TODO(eric): different default for range here?
    value_range=(0, 60000)),
  CookiesTest(
    'maxNameSize', 'Max Name Size', 'max-name-size', 'custom',
    '''Determine the maximum length of the name of a single cookie that can be 
set and retrieved.''',
    #TODO(eric): different default for range here?
    value_range=(0, 60000)),
  CookiesTest(
    'maxValueSize', 'Max Value Size', 'max-value-size', 'custom',
    '''Determine the maximum length of the value of a single cookie that can be 
set and retrieved.''',
    #TODO(eric): different default for range here?
    value_range=(0, 60000)),
  CookiesTest(
    'maxTotalSize', 'Max Total Size', 'max-total-size', 'custom',
    '''Determine the maximum length of the name and value of a single cookie 
that can be set and retrieved.''',
    #TODO(eric): different default for range here?
    value_range=(0, 60000)),
)


class CookiesTestSet(test_set_base.TestSet):

  def GetRowScoreAndDisplayValue(self, results):
    """Get the overall score for this row of results data.
    Args:
      results: A dictionary that looks like:
      {
        'testkey1': {'score': 1-10, 'median': median, 'display': 'celltext'},
        'testkey2': {'score': 1-10, 'median': median, 'display': 'celltext'},
        etc...
      }

    Returns:
      A tuple of (score, display)
      Where score is a value between 1-100.
      And display is the text for the cell.

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
    tests = self.tests
    visible_tests = [test for test in tests
                       if not hasattr(test, 'is_hidden_stat') or
                       not test.is_hidden_stat]
    for test in visible_tests:
      total_tests += 1
      if results.has_key(test.key):
        score = results[test.key]['score']
        #logging.info('test: %s, score: %s' % (test.key, score))
        total_valid_tests += 1
        # boolean 1 = 10, and steve's custom score for hostconn & maxconn map
        # simply to 10 for good, 5 for ok, and 0 for fail, but we only award
        # a point for a 10 on those.
        if score == 10:
          total_score += 1

    #logging.info('%s, %s, %s' % (total_score, total_tests, total_valid_tests))
    score = int(round(100 * total_score / total_tests))
    display = '%s/%s' % (total_score, total_valid_tests)

    return score, display


TEST_SET = CookiesTestSet(
    category=_CATEGORY,
    category_name='Cookies',
    tests=_TESTS,
    test_page='/%s/frameset' % _CATEGORY,
)
