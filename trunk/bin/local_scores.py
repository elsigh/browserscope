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

CREATE_TEMP_SCORES_SQL = """
    CREATE TEMPORARY TABLE temp_scores (
      category VARCHAR(12),
      test VARCHAR(32),
      family VARCHAR(32),
      v1 VARCHAR(6),
      v2 VARCHAR(6),
      v3 VARCHAR(9),
      created DATETIME,
      score INT,
      INDEX (category, test, family, v1, v2, v3)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8
    SELECT
      category, test,
      family, v1, v2, v3, string,
      result_parent.created as result_parent_created,
      user_agent.created as user_agent_created,
      score
    FROM result_time
    LEFT JOIN result_parent USING (result_parent_key)
    LEFT JOIN user_agent USING (user_agent_key)
    ;"""

TEMP_SCORE_SQL = """
    SELECT %(columns)s
    FROM temp_scores
    WHERE
      category = %%(category)s AND
      test = %%(test)s AND
      family = %%(family)s
      %(v_clauses)s
      %(limit_clause)s
    ;"""

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


def DumpScores(db):
  cursor = db.cursor()
  cursor.execute(CREATE_TEMP_SCORES_SQL)
  cursor.execute(BROWSERS_SQL)
  browser_parts = cursor.fetchall()
  for test_set in all_test_sets.GetTestSets():
    category = test_set.category
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
        sql = TEMP_SCORE_SQL % {
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
          sql = TEMP_SCORE_SQL % {
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
    break


def ParseArgs(argv):
  options, args = getopt.getopt(
      argv[1:],
      'h:u:p:f:',
      ['host=', 'gae_user=', 'params=', 'mysql_default_file='])
  host = None
  gae_user = None
  params = None
  mysql_default_file = None
  for option_key, option_value in options:
    if option_key in ('-h', '--host'):
      host = option_value
    elif option_key in ('-u', '--gae_user'):
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
  DumpScores(db)
  end = datetime.datetime.now()
  print '  start: %s' % start
  print '    end: %s' % end
  print 'elapsed: %s' % str(end - start)[:-7]


if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)
  main(sys.argv)
