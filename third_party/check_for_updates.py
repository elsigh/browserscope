#!/usr/bin/python2.5
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
#
# Author slamm@google.com (Stephen Lamm)

import logging
import os
import re
import subprocess


def GetSubversionExternals():
  subversion_externals = []
  svn_cmd = ['svn', 'propget', 'svn:externals', '.']
  output = subprocess.Popen(svn_cmd, stdout=subprocess.PIPE).communicate()[0]
  for external_entry in output.splitlines():
    if external_entry:
      local_path, svn_url = external_entry.split()
      if local_path.startswith('third_party/'):
        subversion_externals.append((local_path, svn_url))
  return dict(subversion_externals)


def GetThirdPartyDirectoriesToCheck(ignore_dirs):
  ignore_dirs = set(ignore_dirs)
  ignore_dirs.add('third_party/.svn')
  check_dirs = []
  for third_party_dir in os.listdir('third_party'):
    relative_dir = 'third_party/%s' % third_party_dir
    if (relative_dir not in ignore_dirs and
        os.path.isdir(relative_dir)):
      check_dirs.append(relative_dir)
  return check_dirs


def CheckVersion(third_party_dir):
  readme_file = open(os.path.join(third_party_dir, 'README.browserscope'))
  print '--------------------------------------------------'
  print 'Checking directory: %s' % third_party_dir
  for line in readme_file.readlines():
    line.strip()
    match = re.match(
        r'(VERSION|CHECK_VERSION|CHECK_VERSION_MANUALLY|URL):\s*(.*)', line)
    if match:
      readme_key, value = match.groups()
      if readme_key == 'URL':
        print 'URL: %s' % value
      elif readme_key == 'VERSION':
        print 'Local version:  %s' % value
      elif readme_key == 'CHECK_VERSION':
        print 'Remote version:',
        print subprocess.Popen(
            value, shell=True, stdout=subprocess.PIPE).communicate()[0].strip()
      else:
        print 'Check manually: %s' % value
  print

if __name__ == '__main__':
  if 'third_party' not in os.listdir('.'):
    os.chdir('..')
    if 'third_party' not in os.listdir('.'):
      logging.error('Must run from the application root.')
  subversion_externals = GetSubversionExternals()
  for skipping_dirs in sorted(subversion_externals.keys()):
    print "Skipping directory managed by svn:externals: %s" % skipping_dirs
  check_dirs = GetThirdPartyDirectoriesToCheck(subversion_externals.keys())
  for third_party_dir in check_dirs:
    CheckVersion(third_party_dir)
