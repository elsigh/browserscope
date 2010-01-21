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

"""Compute scores from locally downloaded data.

Compare local numbers with online numbers.
"""

# Each level
# Each test_set

import bisect
import datetime
import getopt
import logging
import MySQLdb
import os
import re
import sys

sys.path.append('/usr/local/google/google_appengine')
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from categories import all_test_sets

BROWSERS_SQL = """
    SELECT family, v1, v2, v3
    FROM user_agent
    GROUP BY family, v1, v2, v3
    ;"""

SCORE_SQL = """
    SELECT %(columns)s
    FROM result_time
    LEFT JOIN result_parent USING (result_parent_key)
    LEFT JOIN user_agent USING (user_agent_key)
    WHERE
      category = %%(category)s AND
      test = %%(test)s AND
      family = %%(family)s
      %(v_clauses)s
      %(limit_clause)s
    ;"""

CATEGORY_BROWSERS_SQL = """
    SELECT family, v1, v2, v3
    FROM scores
    WHERE category=%s AND family IS NOT NULL
    GROUP BY family, v1, v2, v3
    ;"""

CATEGORY_COUNTS_SQL = """
    SELECT category, count(*) FROM scores GROUP BY category
    ;"""

SCORES_SQL = """
    SELECT %(columns)s
    FROM scores
    WHERE
      category=%%(category)s AND
      test=%%(test)s AND
      family=%%(family)s
      %(v_clauses)s
      %(limit_clause)s
    ;"""


class UserAgent(object):
  @staticmethod
  def pretty_print(family, v1=None, v2=None, v3=None):
    """Pretty browser string."""
    if v3:
      if v3[0].isdigit():
        return '%s %s.%s.%s' % (family, v1, v2, v3)
      else:
        return '%s %s.%s%s' % (family, v1, v2, v3)
    elif v2:
      return '%s %s.%s' % (family, v1, v2)
    elif v1:
      return '%s %s' % (family, v1)
    return family


  @classmethod
  def parts_to_string_list(cls, family, v1=None, v2=None, v3=None):
    """Return a list of user agent version strings.

    e.g. ['Firefox', 'Firefox 3', 'Firefox 3.5']
    """
    key = family, v1, v2, v3
    string_list = []
    if family:
      string_list.append(family)
      if v1:
        string_list.append(cls.pretty_print(family, v1))
        if v2:
          string_list.append(cls.pretty_print(family, v1, v2))
          if v3:
            string_list.append(cls.pretty_print(family, v1, v2, v3))
    return string_list


class LastNRanker(object):
  MAX_NUM_SAMPLED_SCORES = 100

  def __init__(self):
    self.num_scores = 0
    self.scores = []

  def GetMedianAndNumScores(self):
    """Return the median of the last N scores."""
    num_sampled_scores = len(self.scores)
    if num_sampled_scores:
      return self.scores[num_sampled_scores / 2], self.num_scores
    else:
      return None, 0

  def Add(self, score):
    """Add a score into the last N scores.

    If needed, drops the score that is furthest away from the given score.
    """
    num_sampled_scores = len(self.scores)
    if num_sampled_scores < self.MAX_NUM_SAMPLED_SCORES:
      bisect.insort(self.scores, score)
    else:
      index_left = bisect.bisect_left(self.scores, score)
      index_right = bisect.bisect_right(self.scores, score)
      index_center = index_left + (index_right - index_left) / 2
      self.scores.insert(index_left, score)
      if index_center < num_sampled_scores / 2:
        self.scores.pop()
      else:
        self.scores.pop(0)
    self.num_scores += 1

  def GetValues(self):
    return self.scores


class CountRanker(object):
  """Maintain a list of score counts.

  The minimum score is assumed to be 0.
  The maximum score must be MAX_SCORE or less.
  """
  MIN_SCORE = 0
  MAX_SCORE = 100

  def __init__(self):
    self.counts = []

  def GetMedianAndNumScores(self):
    median = None
    num_scores = sum(self.counts)
    median_rank = num_scores / 2
    index = 0
    for score, count in enumerate(self.counts):
      median = score
      index += count
      if median_rank < index:
        break
    return median, num_scores

  def Add(self, score):
    if score < self.MIN_SCORE:
      score = self.MIN_SCORE
      logging.warn('CountRanker(key_name=%s) value out of range (%s to %s): %s',
                   self.key().name(), self.MIN_SCORE, self.MAX_SCORE, score)
    elif score > self.MAX_SCORE:
      score = self.MAX_SCORE
      logging.warn('CountRanker(key_name=%s) value out of range (%s to %s): %s',
                   self.key().name(), self.MIN_SCORE, self.MAX_SCORE, score)
    slots_needed = score - len(self.counts) + 1
    if slots_needed > 0:
      self.counts.extend([0] * slots_needed)
    self.counts[score] += 1

  def GetValues(self):
    return self.counts


def CreateRanker(test, browser, params_str=None):
  if test.min_value >= 0 and test.max_value <= CountRanker.MAX_SCORE:
    return CountRanker()
  else:
    return LastNRanker()


def DumpRankers(fh, rankers):
  for (category, browser, test_key), ranker in sorted(rankers.items()):
    fields = [
        category,
        test_key,
        browser,
        ranker.__class__.__name__,
        ]
    median, num_scores = ranker.GetMedianAndNumScores()
    fields.append(str(median))
    fields.append(str(num_scores))
    fields.append('|'.join(map(str, ranker.GetValues())))
    print >>fh, ','.join(fields)

def BuildRankers(db, category):
  cursor = db.cursor()
  cursor.execute('''
      SELECT test, family, v1, v2, v3, score
      FROM scores
      WHERE category=%s AND test IS NOT NULL AND family IS NOT NULL
      ORDER by test, family, v1, v2, v3
      ;''', category)
  test_set = all_test_sets.GetTestSet(category)
  last_test_key = None
  last_parts = None
  rankers = {}
  for test_key, family, v1, v2, v3, score in cursor.fetchall():
    if test_key != last_test_key:
      last_test_key = test_key
      test = test_set.GetTest(test_key)
    if test is None:
      continue
    parts = family, v1, v2, v3
    if parts != last_parts:
      browsers = UserAgent.parts_to_string_list(family, v1, v2, v3)
    for browser in browsers:
      browser_rankers = rankers.setdefault(browser, {})
      if test_key not in browser_rankers:
        ranker = browser_rankers[test_key] = CreateRanker(test, browser)
      else:
        ranker = browser_rankers[test_key]
      ranker.Add(score)
  return rankers


def GetCategoryBrowsers(db, category):
  cursor = db.cursor()
  cursor.execute(CATEGORY_BROWSERS_SQL, category)
  level_browsers = [set() for version_level in range(4)]
  for family, v1, v2, v3 in cursor.fetchall():
    ua_browsers = UserAgent.parts_to_string_list(family, v1, v2, v3)
    max_ua_browsers_index = len(ua_browsers) - 1
    for version_level in range(4):
      level_browsers[version_level].add(
          ua_browsers[min(max_ua_browsers_index, version_level)])
  return level_browsers

def GetCategories():
  return [test_set.category for test_set in all_test_sets.GetTestSets()]


def CheckTests(db):
  cursor = db.cursor()
  cursor.execute('''
      SELECT category, test, count(*)
      FROM scores
      WHERE category IS NOT NULL
      GROUP BY category, test
      ORDER BY category, test
      ;''')

  for category, test_key, num_scores in cursor.fetchall():
    test_set = all_test_sets.GetTestSet(category)
    if not test_set:
      logging.warn('No test_set for category: %s (num_scores=%s)',
                   category, num_scores)
      continue
    test = test_set.GetTest(test_key)
    if not test:
      logging.warn('No test: %s, %s (num_scores=%s)',
                   category, test_key, num_scores)


def DumpScores(db):
  cursor = db.cursor()
  cursor.execute(CREATE_TEMP_SCORES_SQL)
  cursor.execute(TEMP_CATEGORY_COUNTS_SQL)
  for category, count in cursor.fetchall():
    logging.info("Num scores for category, %s: %s", category, count)
  cursor.execute(BROWSERS_SQL)
  browser_parts = cursor.fetchall()
  for test_set in all_test_sets.GetTestSets():
    category = test_set.category
    logging.info("Dump scores for category: %s", category)
    for family, v1, v2, v3 in browser_parts:
      v_clauses = ''
      for column, value in (('v1', v1), ('v2', v2), ('v3', v3)):
        if value is None:
          v_clauses += ' AND %s IS NULL' % column
        else:
          v_clauses += ' AND %s = "%s"' % (column, value)
      max_num_scores = 0
      medians = []
      for test in test_set.tests:
        sql_params = {
            'category': category,
            'test': test.key,
            'family': family,
            }
        sql = TEMP_SCORES_SQL % {
            'columns': 'count(*)',
            'v_clauses': v_clauses,
            'limit_clause': '',
            }
        sql = re.sub(r'\s+', ' ', sql)
        #print sql, str(sql_params)
        cursor.execute(sql, sql_params)
        num_scores = cursor.fetchone()[0]
        if num_scores:
          max_num_scores = max(max_num_scores, num_scores)
          sql = TEMP_SCORES_SQL % {
              'columns': 'score',
              'v_clauses': v_clauses,
              'limit_clause': 'limit %d,1' % (num_scores / 2),
              }
          #print sql, str(sql_params)
          cursor.execute(sql, sql_params)
          medians.append(cursor.fetchone()[0])
        else:
          medians.append(None)
      if max_num_scores > 0:
        print '%s,"%s",%s,%s' % (category, pretty_print(family, v1, v2, v3),
                              ','.join(map(str, medians)), max_num_scores)


def ParseArgs(argv):
  options, args = getopt.getopt(
      argv[1:],
      'h:e:p:f:',
      ['host=', 'email=', 'params=', 'mysql_default_file='])
  host = None
  gae_user = None
  params = None
  mysql_default_file = None
  for option_key, option_value in options:
    if option_key in ('-h', '--host'):
      host = option_value
    elif option_key in ('-e', '--email'):
      gae_user = option_value
    elif option_key in ('-p', '--params'):
      params = option_value
    elif option_key in ('-f', '--mysql_default_file'):
      mysql_default_file = option_value
  return host, gae_user, params, mysql_default_file, args


def main(argv):
  host, user, params, mysql_default_file, argv = ParseArgs(argv)
  start = datetime.datetime.now()
  db = MySQLdb.connect(read_default_file=mysql_default_file)
  #DumpScores(db)
  rankers = BuildRankers(db)
  DumpRankers(sys.stdout, rankers)
  #CheckTests(db)
  end = datetime.datetime.now()
  logging.info('  start: %s', start)
  logging.info('    end: %s', end)
  logging.info('elapsed: %s', str(end - start)[:-7])


if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)
  main(sys.argv)
