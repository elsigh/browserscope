#!/usr/bin/python2.4
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


"""Bulk datastore changes."""

__author__ = 'slamm@google.com (Stephen Lamm)'

import getopt
import getpass
import os
import simplejson
import sys

from .third_party.appengine_tools import appengine_rpc

UPDATER_URL_PATH = '/admin/update_result_parents'


class ResultUpdater(object):
  def __init__(self, host, path, user, bookmark=None):
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

  def Send(self, bookmark, total_scanned, total_updated):
    response_data = self.rpc_server.Send(self.path, bookmark=bookmark,
                                         total_scanned=total_scanned,
                                         total_updated=total_updated)
    return simplejson.loads(response_data)


def main(argv):
  options, args = getopt.getopt(
      argv[1:],
      'h:u:',
      ['host=', 'gae_user='])
  host = None
  gae_user = None
  for option_key, option_value in options:
    if option_key in ('-h', '--host'):
      host = option_value
    elif option_key in ('-u', '--gae_user'):
      gae_user = option_value

  updater = ResultUpdater(host, UPDATER_URL_PATH, user=gae_user)
  bookmark = None
  total_scanned = 0
  total_updated = 0
  while 1:
    print 'Update batch: %s (total_scanned=%s, total_updated=%s)' % (
        bookmark or 'no_bookmark', total_scanned, total_updated)
    bookmark, total_scanned, total_updated = updater.Send(
        bookmark, total_scanned, total_updated)
    if not bookmark:
      break


if __name__ == '__main__':
  main(sys.argv)
