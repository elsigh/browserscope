#!/usr/bin/python
#
# Copyright 2009 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Big honkin reflow timer runner"""

__author__ = 'elsigh@google.com (Lindsey Simon)'
__version__ = '0.1'

import getopt
import logging
import re
import sys
import time
import os


SELENIUM_HOST = '127.0.0.1'

# Switches for this script.
CLI_OPTS = ['selenium_host=',
            'start_index=',
            'browser=']


# SELENIUM-RC browser_start_command's
#'*custom C:\\Program Files\\Mozilla Firefox 3.1\\firefox.exe'
# '*custom C:\\Program Files\\Mozilla Firefox 2\\firefox.exe',
# '*custom C:\\Program Files\\Mozilla Firefox 1.5\\firefox.exe'

# '*custom C:\\Program Files\\Opera 10 Preview\\opera.exe',
# '*custom C:\\Program Files\\Opera\\opera.exe

# '*custom C:\\Program Files\\Safari\\Safari.exe'
#'*custom C:\\Program Files\\Safari 4\\Safari.exe'

#'*custom C:\\Documents and Settings\\elsigh\\Local Settings\\Application Data\\Google\\Chrome\\Application\\chrome.exe -disable-popup-blocking'

# '*iexplore'
# '*firefox'



def runReflowTimer(selenium_host, browser, url):
  """Calls reflow_timer.py appropriately."""
  cmd_start_time = time.time()
  cmd = ('./reflow_timer.py '
         '--selenium_host="%s" '
         '--browser_start_command="%s" '
         '--do_beacon=0 '
         '--browser_urls="%s" ' %
         (selenium_host, browser, url))
  print 'Running cmd: %s' % cmd
  os.system(cmd)
  cmd_end_time = time.time()
  cmd_run_time = cmd_end_time - cmd_start_time
  print 'Command run time was %s seconds.' % cmd_run_time


def GetTop100URLs():
  """Reads out of top-1m.csv (Alexa's top 1million) the top 100."""
  f = open('top-1m.csv', 'r')
  lines_to_read = 100
  urls = []
  for line in f:
    i, url = line.split(',')
    # strip the newline
    url = url[:-1]
    urls.append('http://%s' % url)
    if int(i) == lines_to_read:
      break
  return urls


def main(argv):
  try:
    opts, args = getopt.getopt(argv, 'hg:d', CLI_OPTS)
  except getopt.GetoptError:
    print 'Cannot parse your flags.'
    sys.exit(2)

  # Set the defaults
  selenium_host = SELENIUM_HOST
  browser = '*firefox'
  start_index = 0

  # Parse the arguments to override the defaults.
  for opt, arg in opts:
    if opt == '--selenium_host':
      selenium_host = arg
    elif opt == '--browser':
      browser = arg
    elif opt == '--start_index':
      start_index = arg

  browsers = browser.split(',')
  start_index = int(start_index)

  print '%s' % __file__
  for opt in CLI_OPTS:
    print ' - w/ %s%s' % (opt, eval(opt.replace('=', '')))

  urls = GetTop100URLs()
  urls = urls[start_index:]

  start_time = time.time()

  total_runs = len(browsers)

  print 'Total Runs: %s, URLs: %s, starting at %s' % (total_runs, len(urls),
                                                      start_time)
  print '--------------------------------------'
  time.sleep(3)

  i = 1
  for browser in browsers:
    print '>---------------->'
    print '%s of %s' % (i, total_runs)
    runReflowTimer(selenium_host, browser, ','.join(urls))
    print 'DONE'
    print '<----------------<'
    # Just a little bit of sleepy room.
    time.sleep(2)
    i += 1


  end_time = time.time()
  total_time = end_time - start_time
  print '--------------------------------------'
  print 'Total time was %s seconds.' % total_time
  print 'Now go to Oasis.'
  print '--------------------------------------'


if __name__ == '__main__':
  main(sys.argv[1:])

