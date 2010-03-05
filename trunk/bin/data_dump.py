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


"""Perform administrative tasks across multiple requests.

App Engine has restrictions on individual requests, so this script breaks
tasks into multiple requests.

To get started:
  $ mysql
  mysql> create database browserscope DEFAULT CHARACTER SET utf8;
  mysql> grant all on browserscope.* to bs@localhost identified by 'XXXX';

  $ cat > ~/bs.cnf
[mysql]
no-auto-rehash

[client]
host=localhost
database=browserscope
user=bs
password=XXXX
pager=less
default_character_set=utf8

"""

__author__ = 'slamm@google.com (Stephen Lamm)'

import datetime
import getopt

import getpass
import logging
import MySQLdb
import os
import simplejson
import sys
import urllib

import local_scores

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from third_party.appengine_tools import appengine_rpc

MAX_ENTITIES_REQUESTED = 100
MAX_RANKERS_UPLOADED = 40
RESTART_OVERLAP_MINUTES=15

CREATE_TABLES_SQL = (
    """CREATE TABLE IF NOT EXISTS result_parent_key (
      result_parent_key VARCHAR(100) NOT NULL PRIMARY KEY
    ) ENGINE=MyISAM DEFAULT CHARACTER SET utf8 COLLATE utf8_bin
    ;""",
    """CREATE TABLE IF NOT EXISTS result_parent (
      result_parent_key VARCHAR(100) NOT NULL PRIMARY KEY,
      category VARCHAR(100),
      user_agent_key VARCHAR(100) NOT NULL,
      ip VARCHAR(100),
      user_id VARCHAR(100),
      created DATETIME,
      params_str VARCHAR(1024),
      loader_id INT(10)
    ) ENGINE=MyISAM DEFAULT CHARACTER SET utf8 COLLATE utf8_bin
    ;""",
    """CREATE TABLE IF NOT EXISTS result_time (
      result_time_key VARCHAR(100) NOT NULL PRIMARY KEY,
      result_parent_key VARCHAR(100) NOT NULL,
      test VARCHAR(50) NOT NULL,
      score INT(10) NOT NULL
    ) ENGINE=MyISAM DEFAULT CHARACTER SET utf8 COLLATE utf8_bin
    ;""",
    """CREATE TABLE IF NOT EXISTS user_agent (
      user_agent_key VARCHAR(100) NOT NULL PRIMARY KEY,
      string TEXT,
      family VARCHAR(32),
      v1 VARCHAR(9),
      v2 VARCHAR(9),
      v3 VARCHAR(12),
      confirmed INT(2),
      created DATETIME,
      js_user_agent_string TEXT
    ) ENGINE=MyISAM DEFAULT CHARACTER SET utf8 COLLATE utf8_bin
    ;""",
    """CREATE TABLE IF NOT EXISTS scores (
      result_parent_key VARCHAR(100),
      result_time_key VARCHAR(100) NOT NULL PRIMARY KEY,
      user_agent_key VARCHAR(100),
      category VARCHAR(100),
      test VARCHAR(50),
      family VARCHAR(32),
      v1 VARCHAR(9),
      v2 VARCHAR(9),
      v3 VARCHAR(12),
      string TEXT,
      js_user_agent_string TEXT,
      result_parent_created DATETIME,
      user_agent_created DATETIME,
      score INT(10),
      INDEX (category, test, family, v1, v2, v3),
      INDEX (user_agent_key),
      INDEX (result_parent_key)
    ) ENGINE=MyISAM DEFAULT CHARACTER SET utf8 COLLATE utf8_bin
    ;""",
    )


INSERT_SQL = {
    'result_parent_key': """INSERT IGNORE result_parent_key SET
        result_parent_key=%s;""",
    'ResultParent': """REPLACE result_parent SET
        result_parent_key=%(result_parent_key)s,
        category=%(category)s,
        user_agent_key=%(user_agent_key)s,
        ip=%(ip)s,
        user_id=%(user_id)s,
        created=%(created)s,
        params_str=%(params_str)s,
        loader_id=%(loader_id)s;""",
    'ResultTime': """REPLACE result_time SET
        result_time_key=%(result_time_key)s,
        result_parent_key=%(result_parent_key)s,
        test=%(test)s,
        score=%(score)s;""",
    'UserAgent': """REPLACE user_agent SET
        user_agent_key=%(user_agent_key)s,
        string=%(string)s,
        family=%(family)s,
        v1=%(v1)s,
        v2=%(v2)s,
        v3=%(v3)s,
        confirmed=%(confirmed)s,
        created=%(created)s,
        js_user_agent_string=%(js_user_agent_string)s;""",
    'lost-UserAgent': """REPLACE user_agent SET
        user_agent_key=%s;"""
    }

UPDATE_SCORES = """
    INSERT IGNORE scores
    SELECT
      result_parent_key,
      result_time_key,
      user_agent_key,
      category,
      test,
      family,
      v1,
      v2,
      v3,
      string,
      js_user_agent_string,
      result_parent.created,
      user_agent.created,
      score
    FROM result_time
    LEFT JOIN result_parent USING (result_parent_key)
    LEFT JOIN user_agent USING (user_agent_key)
    ;"""


MAX_CREATED_SQL = {
    'ResultParent': 'SELECT MAX(created) FROM result_parent',
    'UserAgent': 'SELECT MAX(created) FROM user_agent',
    }

class DataDumpRpcServer(object):

  def __init__(self, host, user):
    self.user = user
    self.host = host
    self.rpc_server = appengine_rpc.HttpRpcServer(
        self.host, self.GetCredentials, user_agent=None, source='',
        save_cookies=True)

  def GetCredentials(self):
    # TODO: Grab email/password from config
    return self.user, getpass.getpass('Password for %s: ' % self.user)

  def Send(self, path, params, method='POST', json_response=True):
    # Drop parameters with value=None. Otherwise, the string 'None' gets sent.
    rpc_params = dict((str(k), v) for k, v in params.items() if v is not None)
    logging.info(
        'http://%s%s%s', self.host, path, rpc_params and '?%s' % '&'.join(
        ['%s=%s' % (k, v) for k, v in sorted(rpc_params.items())]) or '')
    # "payload=None" would a GET instead a POST.
    if method == 'GET':
      response_data = self.rpc_server.Send(path, payload=None, **rpc_params)
    else:
      response_data = self.rpc_server.Send(
          path, payload=urllib.urlencode(rpc_params))
    if response_data.startswith('bailing'):
      logging.fatal(response_data)
      raise RuntimeError
    elif json_response:
      return simplejson.loads(response_data)
    else:
      return response_data

  def GetKeys(self, model, max_created=None):
    """Yield a list of keys for the given model."""
    params = {
        'count': 0,
        'model': model,
        }
    if max_created:
      params['created'] = max_created - datetime.timedelta(
          minutes=RESTART_OVERLAP_MINUTES)
    while 1:
      params = self.Send('/admin/data_dump_keys', params)
      yield params['keys']
      del params['keys']
      if params['bookmark'] is None:
        break

  def DumpEntities(self, db, model, keys):
    logging.info('DumpEntities: model=%s, num_entities=%s', model, len(keys))
    cursor = db.cursor()
    index = 0
    needed_keys = set(keys)
    while needed_keys:
      logging.info('DumpEntities: model=%s, num_needed=%s', model, len(needed_keys))
      next_keys = []
      for i, key in enumerate(sorted(needed_keys)):
        next_keys.append(key)
        if i == MAX_ENTITIES_REQUESTED:
          break
      if len(next_keys) == 1:
        params = {
            'model': model,
            'keys': next_keys[0],
            }
      else:
        key_prefix = os.path.commonprefix(next_keys)
        prefix_len = len(key_prefix)
        params = {
            'model': model,
            'key_prefix': key_prefix,
            'keys': ','.join([key[prefix_len:] for key in next_keys]),
            }
      start = datetime.datetime.now()
      params = self.Send('/admin/data_dump', params)
      logging.info('request_time=%s', str(datetime.datetime.now() - start)[:-7])

      for row in params['data']:
        if 'lost_key' in row:
          lost_key = row['lost_key']
          lost_model = row['model_class']
          logging.info('Skipping unfound key: %s, model=%s',
                       lost_key, lost_model)
          needed_keys.discard(lost_key)
          if lost_model == 'UserAgent':
            cursor.execute(INSERT_SQL['lost-UserAgent'], lost_key)
        elif 'dirty_key' in row:
          dirty_key = row['dirty_key']
          logging.info('Skipping dirty ResultParent: %s')
          needed_keys.discard(dirty_key)
        else:
          cursor.execute(INSERT_SQL[row['model_class']], row)
          if 'result_parent_key' in row:
            needed_keys.discard(row['result_parent_key'])
          elif 'user_agent_key' in row:
            needed_keys.discard(row['user_agent_key'])
      del params['data']

  def NeededResultParentKeys(self, db):
    cursor = db.cursor()
    cursor.execute("""
        SELECT result_parent_key.result_parent_key
            FROM result_parent_key
            LEFT JOIN result_parent USING(result_parent_key)
            WHERE result_parent.result_parent_key IS NULL
            ORDER BY result_parent_key.result_parent_key;""")
    return [row[0] for row in cursor.fetchall()]

  def NeededUserAgentKeys(self, db):
    cursor = db.cursor()
    cursor.execute("""
        SELECT result_parent.user_agent_key
        FROM result_parent
        LEFT JOIN user_agent USING(user_agent_key)
        WHERE user_agent.user_agent_key IS NULL
        GROUP BY result_parent.user_agent_key
        ORDER BY result_parent.user_agent_key;""")
    return [row[0] for row in cursor.fetchall()]

  def UpdateResultParentKeys(self, db):
    cursor = db.cursor()
    cursor.execute(MAX_CREATED_SQL['ResultParent'])
    max_created = cursor.fetchone()[0]
    for keys in self.GetKeys('ResultParent', max_created):
      cursor.executemany(INSERT_SQL['result_parent_key'], keys)


  def CreateTables(self, db):
    cursor = db.cursor()
    for create_sql in CREATE_TABLES_SQL:
      cursor.execute(create_sql)

  def DownloadEntities(self, db, run_start):
    self.CreateTables(db)

    needed_result_parent_keys = self.NeededResultParentKeys(db)
    if not needed_result_parent_keys:
      self.UpdateResultParentKeys(db)
      needed_result_parent_keys = self.NeededResultParentKeys(db)

    is_score_updated_needed = False
    if needed_result_parent_keys:
      self.DumpEntities(db, 'ResultParent', needed_result_parent_keys)
      is_score_updated_needed = True

    needed_user_agent_keys = self.NeededUserAgentKeys(db)
    if needed_user_agent_keys:
      self.DumpEntities(db, 'UserAgent', needed_user_agent_keys)
      is_score_updated_needed = True

    if is_score_updated_needed:
      logging.info('Update "scores" table.')
      cursor = db.cursor()
      cursor.execute(UPDATE_SCORES)

  def PauseDirtyManager(self):
    self.rpc_server.Send('/admin/pause_dirty')

  def UnpauseDirtyManager(self):
    self.rpc_server.Send('/admin/unpause_dirty')

  def UploadRankers(self, category, rankers):
    def GetRankerBatches(rankers, batch_size):
      ranker_batch = []
      for browser in rankers:
        for test_key, ranker in rankers[browser].items():
          if len(ranker_batch) < batch_size:
            ranker_batch.append((browser, test_key, ranker))
          else:
            yield ranker_batch
            ranker_batch = []
      if ranker_batch:
        yield ranker_batch

    num_to_upload = sum(len(x) for x in rankers.values())
    num_uploaded = {}
    for ranker_batch in GetRankerBatches(rankers, MAX_RANKERS_UPLOADED):
      logging.info('Rankers to update: %s', num_to_upload)
      test_key_browsers = []
      ranker_values = []
      completed_browsers = []
      for browser, test_key, ranker in ranker_batch:
        test_key_browsers.append([
            test_key,
            browser])
        median, num_scores = ranker.GetMedianAndNumScores()
        ranker_values.append([
            median,
            num_scores,
            '|'.join(map(str, ranker.GetValues())),
            ])
        num_to_upload -= 1
        num_uploaded.setdefault(browser, 0)
        num_uploaded[browser] += 1
        if num_uploaded[browser] == len(rankers[browser]):
          completed_browsers.append(browser)
      params = {
          'category': category,
          'test_key_browsers_json': simplejson.dumps(test_key_browsers),
          'ranker_values_json': simplejson.dumps(ranker_values),
          }
      num_retries = 0
      while 1:
        response_params = self.Send('/admin/rankers/upload', params)
        if 'message' not in response_params:
          break
        logging.info('Server message: %s', response_params['message'])
        if num_retries == 2:
          logging.info('Giving up after two retries.')
          break
        logging.info('Retrying.')
        num_retries += 1
      if completed_browsers:
        self.Send('/admin/update_stats_cache', {
            'category': category,
            'browsers': ','.join(completed_browsers),
            }, method='GET', json_response=False)

  def UploadCategoryBrowsers(self, category, version_level, browsers):
    params = {
        'category': category,
        'version_level': version_level,
        'browsers': ','.join(list(browsers)),
        }
    self.Send('/admin/upload_category_browsers', params, json_response=False)

def ParseArgs(argv):
  options, args = getopt.getopt(
      argv[1:],
      'h:e:f:rc',
      ['host=', 'email=', 'mysql_default_file=',
       'release', 'category_browsers_only'])
  host = None
  gae_user = None
  mysql_default_file = None
  is_release = False
  is_category_browsers_only = False
  for option_key, option_value in options:
    if option_key in ('-h', '--host'):
      host = option_value
    elif option_key in ('-e', '--email'):
      gae_user = option_value
    elif option_key in ('-f', '--mysql_default_file'):
      mysql_default_file = option_value
    elif option_key in ('-r', '--release'):
      is_release = True
    elif option_key in ('-c', '--category_browsers_only'):
      is_category_browsers_only = True
  return host, gae_user, mysql_default_file, is_release, is_category_browsers_only, args


def main(argv):
  categories = local_scores.GetCategories()
  (host, user, mysql_default_file,
   is_release, is_category_browsers_only, argv) = ParseArgs(argv)
  start = datetime.datetime.now()
  db = MySQLdb.connect(read_default_file=mysql_default_file)
  if is_category_browsers_only:
    server = DataDumpRpcServer(host, user)
    for category in categories:
      category_browsers = local_scores.GetCategoryBrowsers(db, category)
      for version_level, browsers in category_browsers:
        server.UploadCategoryBrowsers(category, version_level, browsers)
  elif is_release:
    try:
      server = DataDumpRpcServer(host, user)
      # logging.info("Pause Dirty Manager")
      # server.PauseDirtyManager()
      logging.info("Download Entities for all categories.")
      server.DownloadEntities(db, start)
      for category in categories:
        logging.info("Build Rankers: %s", category)
        rankers = local_scores.BuildRankers(db, category)

        logging.info("Upload Rankers: %s", category)
        server.UploadRankers(category, rankers)

        logging.info("Upload Category Browsers: %s", category)
        category_browsers = local_scores.GetCategoryBrowsers(db, category)
        for version_level, browsers in enumerate(category_browsers):
          if not browsers:
            logging.info("Skipping empty category browsers: version_level=%s",
                         version_level)
            continue
          server.UploadCategoryBrowsers(category, version_level, browsers)
    finally:
      pass
      #      server.UnpauseDirtyManager()
  else:
    server = DataDumpRpcServer(host, user)
    server.DownloadEntities(db, start)
  end = datetime.datetime.now()
  print '  start: %s' % start
  print '    end: %s' % end
  print 'elapsed: %s' % str(end - start)[:-7]


if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO,
                      filename='/tmp/data_dump.log',
                      filemode='w')
  console = logging.StreamHandler()
  console.setLevel(logging.INFO)
  logging.getLogger('').addHandler(console)
  main(sys.argv)
