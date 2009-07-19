#!/usr/bin/python2.5
# Copyright 2009 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the 'License')
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Author slamm@google.com (Stephen Lamm)

import os
import sys


def AddImportPaths(paths):
  site_packages_index = None
  for sys_path_index, dir_name in enumerate(sys.path):
    if dir_name.find('site-packages') != -1:
      site_packages_index = sys_path_index
      break
  if site_packages_index is None:
    sys.path.extend(paths)
  else:
    sys.path[site_packages_index:site_packages_index] = paths


third_party_path = os.path.dirname(os.path.abspath(__file__))
AddImportPaths([
    third_party_path,
    os.path.join(third_party_path, 'pymox'),  # allow 'import mox'
    ])
