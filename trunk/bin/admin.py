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
"""

__author__ = 'slamm@google.com (Stephen Lamm)'

import datetime
import getopt
import getpass
import logging
import os
import simplejson
import sys


sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from third_party.appengine_tools import appengine_rpc


COMMAND_PATHS = {
  'results_update': '/admin/update_result_parents',
  'ranker_rebuild': '/admin/rankers/rebuild',
  'ranker_release': '/admin/rankers/release_next',
  'ranker_reset': '/admin/rankers/reset_next',
  'ua_rebuild': '/admin/ua/rebuild',
  'ua_release': '/admin/ua/release',
  }


class AdminRpcServer(object):
  def __init__(self, host, user, path):
    self.user = user
    self.path = path
    self.rpc_server = appengine_rpc.HttpRpcServer(
        host, self.GetCredentials, user_agent=None, source='',
        save_cookies=True)

  def GetCredentials(self):
    # TODO: Grab email/password from config
    return self.user, getpass.getpass('Password for %s: ' % self.user)

  def Send(self, **kwds):
    # Drop parameters with value=None. Otherwise, the string 'None' gets sent.
    rpc_params = dict((key, value)
                      for key, value in kwds.items() if value is not None)

    # "payload=None" forces a GET request instead of a POST (default).
    response_data = self.rpc_server.Send(self.path, payload=None, **rpc_params)
    return simplejson.loads(response_data)

  def Run(self, run_start, params_str):
    params = {}
    if params_str:
      params = dict(y.split('=', 1) for y in params_str.split('&'))
    while not params.get('is_done', False):
      request_start = datetime.datetime.now()
      params = self.Send(**dict((str(x), y) for x, y in params.items()))
      request_end = datetime.datetime.now()
      logging.info('elapsed=%s, request=%s: Run() params: %s',
                   str(request_end - run_start)[:-7],
                   str(request_end - request_start)[:-7],
                   params)


def ParseArgs(argv):
  options, args = getopt.getopt(
      argv[1:],
      'h:u:p:',
      ['host=', 'gae_user=', 'params='])
  host = None
  gae_user = None
  params = None
  for option_key, option_value in options:
    if option_key in ('-h', '--host'):
      host = option_value
    elif option_key in ('-u', '--gae_user'):
      gae_user = option_value
    elif option_key in ('-p', '--params'):
      params = option_value
  return host, gae_user, params, args


def main(argv):
  host, user, params, argv = ParseArgs(argv)
  if not argv or argv[0] not in COMMAND_PATHS:
    commands = '|'.join(sorted(COMMAND_PATHS.keys()))
    logging.fatal("usage: ranker_updater.py -h HOST -u GAE_USER -p params (%s)",
                  commands)
  else:
    start = datetime.datetime.now()
    AdminRpcServer(host, user, COMMAND_PATHS[argv[0]]).Run(start, params)
    end = datetime.datetime.now()
    print '  start: %s' % start
    print '    end: %s' % end
    print 'elapsed: %s' % str(end - start)[:-7]


if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)
  main(sys.argv)
