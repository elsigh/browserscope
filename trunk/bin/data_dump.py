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

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from third_party.appengine_tools import appengine_rpc

RESTART_OVERLAP_MINUTES=15
CREATE_TABLES_SQL = (
    """CREATE TABLE IF NOT EXISTS result_parent (
    result_parent_key VARCHAR(100) NOT NULL PRIMARY KEY,
    user_agent_key VARCHAR(100) NOT NULL,
    ip VARCHAR(100),
    user_id VARCHAR(100),
    created DATETIME,
    params_str VARCHAR(1024),
    loader_id INT(10)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8;""",
    """CREATE TABLE IF NOT EXISTS result_time (
    result_time_key VARCHAR(100) NOT NULL PRIMARY KEY,
    result_parent_key VARCHAR(100) NOT NULL,
    test VARCHAR(50) NOT NULL,
    score INT(10) NOT NULL
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8;""",
    """CREATE TABLE IF NOT EXISTS user_agent (
    user_agent_key VARCHAR(100) NOT NULL PRIMARY KEY,
    string TEXT,
    family VARCHAR(32),
    v1 VARCHAR(10),
    v2 VARCHAR(10),
    v3 VARCHAR(10),
    confirmed INT(2),
    created DATETIME,
    js_user_agent_string TEXT
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8;""",
    )


INSERT_SQL = {
    'ResultParent': """REPLACE result_parent SET
        result_parent_key=%(result_parent_key)s,
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
    }
MAX_CREATED_SQL = {
    'ResultParent': 'SELECT MAX(created) FROM result_parent',
    'UserAgent': 'SELECT MAX(created) FROM user_agent',
    }



class DataDumpRpcServer(object):
  PATH = '/admin/data_dump'

  def __init__(self, host, user):
    self.user = user
    self.path = self.PATH
    self.host = host
    self.rpc_server = appengine_rpc.HttpRpcServer(
        self.host, self.GetCredentials, user_agent=None, source='',
        save_cookies=True)

  def GetCredentials(self):
    # TODO: Grab email/password from config
    return self.user, getpass.getpass('Password for %s: ' % self.user)

  def Send(self, **kwds):
    # Drop parameters with value=None. Otherwise, the string 'None' gets sent.
    rpc_params = dict((key, value)
                      for key, value in kwds.items() if value is not None)

    # "payload=None" forces a GET request instead of a POST (default).
    logging.info('http://%s%s%s', self.host, self.path,
                 rpc_params and '?%s' % '&'.join(['%s=%s' % (k, v) for k, v in sorted(rpc_params.items())]) or '')
    response_data = self.rpc_server.Send(self.path, payload=None, **rpc_params)
    return simplejson.loads(response_data)

  def Run(self, mysql_default_file, run_start, params_str):
    params = {}
    if params_str:
      params = dict(y.split('=', 1) for y in params_str.split('&'))
    # Create tables
    db = MySQLdb.connect(read_default_file=mysql_default_file)
    cursor = db.cursor()
    for create_sql in CREATE_TABLES_SQL:
      cursor.execute(create_sql)
    for model in ('ResultParent', 'UserAgent'):
      cursor.execute(MAX_CREATED_SQL[model])
      max_created = cursor.fetchone()[0]
      if max_created:
        params['created'] = max_created - datetime.timedelta(
            minutes=RESTART_OVERLAP_MINUTES)
      params['model'] = model
      elapsed_time = datetime.timedelta()
      request_time = datetime.timedelta()
      while not params.get('is_done', False):
        logging.info('elapsed=%s, request=%s: Run() params: %s',
                     str(elapsed_time)[:-7],
                     str(request_time)[:-7],
                     params)
        request_start = datetime.datetime.now()
        params = self.Send(**dict((str(x), y) for x, y in params.items()))
        elapsed_time = datetime.datetime.now() - run_start
        request_time = datetime.datetime.now() - request_start
        for row in params['data']:
          cursor.execute(INSERT_SQL[row['model_class']], row)
        del params['data']
        if params['bookmark'] is None:
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
  DataDumpRpcServer(host, user).Run(mysql_default_file, start, params)
  end = datetime.datetime.now()
  print '  start: %s' % start
  print '    end: %s' % end
  print 'elapsed: %s' % str(end - start)[:-7]


if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)
  main(sys.argv)
