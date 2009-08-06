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

"""Run unit tests on the command-line.

"""

__author__ = 'slamm@google.com (Stephen Lamm)'

import logging
import sys

sys.path.extend(['.', '..'])
from third_party.appengine_tools import appengine_rpc

def GetCredentials():
  return 'test@example.com', ''

host_port = sys.argv[1]
user_agent = None
source = ''
rpc_server = appengine_rpc.HttpRpcServer(
    host_port, GetCredentials, user_agent, source)

url = '/test?format=plain'
content = rpc_server.Send('/test', payload=None, format='plain')

print content
if 'FAILED (' in content:
  sys.exit('FAILED')
