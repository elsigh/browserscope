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

"""Test set class."""

__author__ = 'slamm@google.com (Stephen Lamm)'


import logging

from models import result_ranker

import settings

class Error(Exception):
  """Base exception for test_set_base."""
  pass


class ParseResultsKeyError(Error):
  """The keys in the result string do not match the defined tests."""
  def __init__(self, expected, actual):
    self.expected = expected
    self.actual = actual

  def __str__(self):
    return ("Keys mismatch: expected=%s, actual=%s" %
            (self.expected, self.actual))


class ParseResultsValueError(Error):
  """The values in the result string do not parse as integers."""
  pass


class TestBase(object):
  def __init__(self, key, name, url, doc, min_value, max_value,
               test_set=None, is_hidden_stat=False, cell_align='right',
               url_prepend='', halt_tests_on_fail=False):
    self.key = key
    self.name = name
    self.url = url
    self.doc = doc
    self.min_value = min_value
    self.max_value = max_value
    self.test_set = test_set
    self.is_hidden_stat = is_hidden_stat
    self.cell_align = cell_align
    if (min_value, max_value) == (0, 1):
      self.score_type = 'boolean'
    else:
      self.score_type = 'custom'
    self.url_prepend = url_prepend
    # must use 0 and 1 so that the javascript side can use it
    if halt_tests_on_fail:
      self.halt_tests_on_fail = 1
    else:
      self.halt_tests_on_fail = 0

  def GetRanker(self, browser, params_str=None):
    if params_str is None and self.test_set.default_params:
      params_str = str(self.test_set.default_params)
    return result_ranker.GetRanker(self, browser, params_str)

  def GetOrCreateRankers(self, browsers, params_str=None):
    test_browsers = [(self, b) for b in browsers]
    return result_ranker.GetOrCreateRankers(test_browsers, params_str)

  def IsVisible(self):
    return not hasattr(self, 'is_hidden_stat') or not self.is_hidden_stat

class TestSet(object):
  def __init__(self, category, category_name, summary_doc, tests,
               default_params=None, test_page=None):
    """Initialize a test set.

    A test set has all the tests for a category.

    Args:
      category: a string
      category_name: a string, human-readable
      summary_doc: a brief description of test set.
      tests: a list of test instances
    """
    self.category = category
    self.category_name = category_name
    self.summary_doc = summary_doc
    self.tests = tests
    self.default_params = default_params
    self.test_page = test_page
    self.user_test_category = None
    if self.test_page is None:
      # i.e. default is like /acid3/acid3.html
      self.test_page = '/%s/static/%s.html' % (self.category, self.category)
    self._test_dict = {}
    for test in tests:
      test.test_set = self  # add back pointer to each test
      self._test_dict[test.key] = test
    self._test_keys = sorted(self._test_dict)

  def GetTest(self, test_key):
    """Gets the test from the tests dict. If a key is passed in and there's
    no test for it, which can happen if there's still data in the datastore
    but someone has deleted that test from the test_set, then return None.
    Args:
      test_key: string A test key.
    Returns:
      test: A TestBase instance or None
    """
    return self._test_dict.get(test_key, None)

  def VisibleTests(self):
    return [t for t in self.tests if t.IsVisible()]

  def IsBooleanTest(self, test_key):
    """Return true if the test_key represents a boolean test.

    Args:
      test_key: a key for a test_set test.
    Returns:
      True iff test indexed by test_key has a boolean score type.
    """
    return self.GetTest(test_key).score_type == 'boolean'

  def GetResults(self, results_str, ignore_key_errors=False):
    """Parses a results string.

    Args:
      results_str: a string like 'test_1=raw_score_1,test_2=raw_score_2, ...'.
      ignore_key_errors: if true, skip checking keys with list of tests
    Returns:
      {test_1: {'raw_score': score_1}, test_2: {'raw_score': score_2}, ...}
    """
    parsed_results = self.ParseResults(
        results_str, ignore_key_errors=ignore_key_errors)
    return self.AdjustResults(parsed_results)

  def ParseResults(self, results_str, ignore_key_errors=False):
    """Parses a results string.

    Args:
      results_str: a string like 'test_1=raw_score_1,test_2=raw_score_2, ...'.
      ignore_key_errors: if true, skip checking keys with list of tests
    Returns:
      {test_1: {'raw_score': score_1}, test_2: {'raw_score': score_2}, ...}
    """
    test_scores = [x.split('=') for x in str(results_str).split(',')]
    test_keys = sorted([x[0] for x in test_scores])
    if not ignore_key_errors and self._test_keys != test_keys:
      expected_keys = self._test_keys
      raise ParseResultsKeyError(expected=expected_keys, actual=test_keys)
    try:
      parsed_results = dict([(key, {'raw_score': int(score)})
                             for key, score in test_scores])
    except ValueError:
      logging.error('ValueError in results_str (%s): test_scores=%s',
                    results_str, test_scores)
      raise ParseResultsValueError
    return parsed_results

  def AdjustResults(self, results):
    """Rewrite the results dict before saving the results.

    Left to implementations to overload.

    Args:
      results: a list of dicts like {key_1: {'raw_score': score_1}, ...}
    Returns:
      a list of modified dicts like the following:
      {key_1: {'raw_score': modified_score_1, extra_key: extra_value}, ...}

    """
    return results

  def GetRankers(self, browser, tests=None):
    """Return the rankers for the given browser and tests (optional).

    Args:
      browser: a browser/version string like 'Firefox 3.0'.
      tests: a list of test instances
    Returns:
      [ranker_1, ranker_2, ...]
    """
    test_browsers = [(t, browser) for t in tests or self.tests]
    params_str = self.default_params and str(self.default_params) or None
    return result_ranker.GetRankers(test_browsers, params_str)

  def GetMediansAndNumScores(self, browser):
    """Return the raw scores for a given browser.

    Args:
      browser: a browser/version string like 'Firefox 3.0'.
    Returns:
      ({test_key_1: median_1, test_key_2: median_2},
       {test_key_1: num_scores_1, test_key_2: num_scores_2})
    """
    medians, num_scores = {}, {}
    for test, ranker in zip(self.tests, self.GetRankers(browser)):
      if ranker:
        medians[test.key], num_scores[test.key] = ranker.GetMedianAndNumScores()
      else:
        medians[test.key], num_scores[test.key] = None, 0
    #logging.info('GetMediansAndNumScores: category=%s, medians=%s, '
    #             'num_scores=%s' % (self.category, medians, num_scores))
    return medians, num_scores

  def GetStats(self, test_keys, raw_scores, num_scores=None):
    """Get normalized scores, display values including summary values.

    Args:
      test_keys: the test keys to include in the 'results'.
      raw_scores: {
          test_key_1: raw_score_1,
          test_key_2: raw_score_2,
          ...}
      num_scores: {
          test_key_1: num_scores_1,
          test_key_2: num_scores_2,
          ...}
    Returns:
      {
          'total_runs': total_runs,
          'summary_score': summary_score,      # value is from 1 to 100
          'summary_display': summary_display,  # text to present
          'results': {
              test_key_1: {
                  'raw_score': raw_score_1,
                  'score': score_1,
                  'display': display_1,
                  'expando': expando_1,  # (optional)
              },
              test_key_2: {...},
              },
          }
      }
    """
    logging.info('GetStats: category=%s, test_keys=%s raw_scores=%s,'
                 ' num_scores=%s',
                 self.category, test_keys, raw_scores, num_scores)
    results = {}
    total_runs = 0
    for test_key in test_keys:
      if num_scores:
        total_runs = max(total_runs, num_scores[test_key])
      raw_score = raw_scores.get(test_key)
      if self.IsBooleanTest(test_key):
        if raw_score is None:
          score, display = 0, ''
        elif raw_score:
          score, display = 100, settings.STATS_SCORE_TRUE
        else:
          score, display = 1, settings.STATS_SCORE_FALSE
      else:
        score, display = (
            self.GetTestScoreAndDisplayValue(test_key, raw_scores))
      results[test_key] = {
          'raw_score': raw_score,
          'score': score,
          'display': display,
          }
    summary_score, summary_display = self.GetRowScoreAndDisplayValue(results)
    stats = {
        'summary_score': summary_score,
        'summary_display': summary_display,
        'results': results,
        }
    if num_scores is not None:
      stats['total_runs'] = total_runs
    return stats

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
    raise NotImplementedError

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
    """
    raise NotImplementedError
