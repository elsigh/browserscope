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


"""Bulk upload network performance tests.

This script queries MySQL and sends network scores to the GAE.

"""

__author__ = 'slamm@google.com (Stephen Lamm)'

import datetime
import getopt
import getpass
import logging
import os
import MySQLdb
import simplejson
import sys
import urlparse

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from third_party.appengine_tools import appengine_rpc

logging.basicConfig(level=logging.INFO)

LOADER_URL_PATH = '/network/loader'
MAX_RETRIES = 1
BATCH_SIZE = 100  # takes about 21 seconds to load on ua-profiler-sandbox.

SCORE_COLUMNS = (
    'latency',
    'hostconn',
    'maxconn',
    'parscript',
    'parsheet',
    'parcssjs',
    'cacheexp',
    'cache25k',
    'cacheredir',
    'cacheresredir',
    'prefetch',
    'gzip',
    'du'
    )

MAX_TEST_ID_SQL = """
  SELECT MAX(testid) FROM testsdev;
"""
TEST_RESULTS_SQL = """
  SELECT
    testid,
    createdate,
    useragent,
    ip,
    %(score_columns)s
  FROM testsdev
  WHERE testid > %(last_test_id)s
  ORDER BY testid
  LIMIT %(batch_size)s;
  """


def Connect(default_file):
  return MySQLdb.connect(read_default_file=default_file)


def MaxTestId(db):
  cursor = db.cursor()
  cursor.execute(MAX_TEST_ID_SQL)
  return cursor.fetchone()[0]

def Results(db, last_test_id, batch_size):
  results = []
  cursor = db.cursor()
  sql = TEST_RESULTS_SQL % {
      'score_columns': ',\n'.join(SCORE_COLUMNS),
      'last_test_id': last_test_id,
      'batch_size': batch_size,
      }
  logging.debug('Results sql: %s', sql)
  cursor.execute(sql)
  for row in cursor.fetchall():
    test_id, create_timestamp, user_agent_string, ip = row[:4]
    if not user_agent_string:
      logging.info('Skipping test with no useragent: testid=%s', test_id)
      continue
    test_scores = ','.join(['%s=%s' % (name, value) for name, value
                            in zip(SCORE_COLUMNS, row[4:])
                            if value is not None])
    results.append([
        test_id,
        ip,
        user_agent_string,
        int(create_timestamp),
        test_scores])
  return results


class ResultsSender(object):
  def __init__(self, host, path, user):
    self.path = path
    self.user = user
    user_agent = None
    # TODO: figure out a value for 'source'.
    #   Doc says, "The source to specify in authentication requests."
    source = ''
    self.rpc_server = appengine_rpc.HttpRpcServer(
        host, self.GetCredentials, user_agent, source, save_cookies=True)

  def GetCredentials(self):
    # TODO: Grab email/password from config
    return self.user, getpass.getpass('Password for %s: ' % self.user)

  def Send(self, results):
    response = self.rpc_server.Send(self.path, simplejson.dumps(results))
    if response.isdigit():
      last_loader_id = int(response)
    else:
      logging.warning('Error on server side: %s', response)
      last_loader_id = None
    return last_loader_id


def main(argv):
  options, args = getopt.getopt(
      argv[1:],
      'bf:h:u:',
      ['mysql_default_file=', 'host=', 'gae_user='])
  is_one_batch = None
  mysql_default_file = None
  host = None
  gae_user = None
  print options
  for option_key, option_value in options:
    if option_key == '-b':
      is_one_batch = True
    elif option_key in ('-f', '--mysql_default_file'):
      mysql_default_file = option_value
    elif option_key in ('-h', '--host'):
      host = option_value
    elif option_key in ('-u', '--gae_user'):
      gae_user = option_value

  db = Connect(mysql_default_file)
  sender = ResultsSender(host, LOADER_URL_PATH, user=gae_user)
  last_test_id = sender.Send([]) or 0
  logging.info('Last test id on target server: %d', last_test_id)
  max_test_id = MaxTestId(db)
  logging.info('Last test id on source server: %d', max_test_id)
  retries = 0
  num_entries = 0
  start = datetime.datetime.now()
  while last_test_id < max_test_id:
    results = Results(db, last_test_id, BATCH_SIZE)
    batch_start = datetime.datetime.now()
    last_test_id = sender.Send(results)
    batch_end = datetime.datetime.now()
    num_entries += BATCH_SIZE
    logging.info('total=%s, total_time=%s, batch_time=%s, last_test_id=%s,'
                 ' batch_size=%s, max_test_id=%s',
                 num_entries,
                 str(batch_end - start)[:-7],
                 str(batch_end - batch_start)[:-7],
                 last_test_id, BATCH_SIZE, max_test_id)
    if last_test_id:
      retries = 0
    else:
      retries += 1
      if retries <= MAX_RETRIES:
        logging.info('Retrying batch.')
      else:
        logging.info('Upload failed.')
        break
    if is_one_batch:
      break


if __name__ == '__main__':
  main(sys.argv)
