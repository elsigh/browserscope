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


SERVER = 'ua-profiler.appspot.com'
#SERVER = 'localhost:8084'


# Override so we can test one page, our canonical one, a bunch of tims.
# TEST_PAGES['nested_anchors']['params'] = {
#   'num_elements': ['400'],
#   'num_nest': ['4'],
#   'css_selector': ['%23g-content%20*',],
#   'num_css_rules': ['400'],
#   'css_text': ['border%3A%201px%20solid%20%230C0%3B'
#                '%20padding%3A%208px%3B']
# }

# controllers/reflows.py uses this too.
TEST_PAGES = {
  'nested_anchors': {
    'url':  'http://%s/reflow/test/nested_anchors?'
            'num_elements=&num_nest=&num_css_rules=&css_selector='
            '&css_text=' % SERVER,
    'params': {'num_elements': ['200', '400', '800', '1000'],
               'num_nest': ['2', '4', '8', '10'],
               'css_selector': ['%23g-content%20div',
                                '%23g-content%20html',
                                '%23g-content%20a',
                                '%23g-content%20*',],
               'num_css_rules': ['0', '200', '400', '1000'],
               'css_text': ['border%3A%201px%20solid%20%230C0%3B'
                            '%20padding%3A%208px%3B']
              }

  },
  'nested_divs': {
    'url': 'http://%s/reflow/test/nested_divs?num_nest=' % SERVER,
    'params': {'num_nest': ['2', '4', '8', '10', '16', '20', '200']},
  },
  'nested_tables': {
    'url': 'http://%s/reflow/test/nested_tables?num_nest=' % SERVER,
    'params': {'num_nest': ['2', '4', '8', '10', '16', '20', '200']},
  }
}

SELENIUM_HOST = '172.18.110.195'

# 1 means hit run_reflows.py for each url in its own selenium-rc session.
# 2 means send run_reflows.py the big honkin list of urls, i.e. one selenium-rc
# session that runs through all the URLs.
RUN_STYLE = '2'

# Switches for this script.
CLI_OPTS = ['selenium_host=',
            'browser=',
            'url_type=',
            'run_style=',
            'start_index=',
            'num_runs=']

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


def ConstructReflowTimerUrls(url, url_params, url_type):
  # TODO(elsigh: Figure out how to write a program to do this.
  #              and get rid of url_type as a param.
  urls = []
  if url_type == 'nested_anchors':
    for num_elements in url_params['num_elements']:
      for num_nest in url_params['num_nest']:
        for css_selector in url_params['css_selector']:
          for num_css_rules in url_params['num_css_rules']:
            for css_text in url_params['css_text']:
              urls.append(
                url.replace(
                  'num_elements=', 'num_elements=%s' % num_elements).replace(
                  'num_css_rules=', 'num_css_rules=%s' % num_css_rules).replace(
                  'num_nest=', 'num_nest=%s' % num_nest).replace(
                  'css_selector=', 'css_selector=%s' % css_selector).replace(
                  'css_text=', 'css_text=%s' % css_text))
  elif url_type == 'nested_divs' or url_type == 'nested_tables':
    for num_nest in url_params['num_nest']:
      urls.append(url.replace('num_nest=', 'num_nest=%s' % num_nest))

  #print 'URLs %s' % (urls)
  return urls

def runReflowTimer(selenium_host, browser, url):
  """Calls reflow_timer.py appropriately."""
  cmd_start_time = time.time()
  cmd = ('./reflow_timer.py '
         '--selenium_host="%s" '
         '--browser_start_command="%s" '
         '--browser_urls="%s" ' %
         (selenium_host, browser, url))
  print 'Running cmd: %s' % cmd
  os.system(cmd)
  cmd_end_time = time.time()
  cmd_run_time = cmd_end_time - cmd_start_time
  print 'Command run time was %s seconds.' % cmd_run_time


def main(argv):
  try:
    opts, args = getopt.getopt(argv, 'hg:d', CLI_OPTS)
  except getopt.GetoptError:
    print 'Cannot parse your flags.'
    sys.exit(2)

  # Set the defaults
  selenium_host = SELENIUM_HOST
  browser = '*firefox'
  run_style = RUN_STYLE
  url_type = 'nested_anchors'
  start_index = 0
  num_runs = 1

  # Parse the arguments to override the defaults.
  for opt, arg in opts:
    if opt == '--selenium_host':
      selenium_host = arg
    elif opt == '--browser':
      browser = arg
    elif opt == '--run_style':
      run_style = arg
    elif opt == '--url_type':
      url_type = arg
    elif opt == '--start_index':
      start_index = arg
    elif opt == '--num_runs':
      num_runs = int(arg)

  browsers = browser.split(',')
  start_index = int(start_index)

  print '%s' % __file__
  for opt in CLI_OPTS:
    print ' - w/ %s%s' % (opt, eval(opt.replace('=', '')))

  if url_type == 'nested_divs_vs_tables':
    urls1 = ConstructReflowTimerUrls(
        url=TEST_PAGES['nested_divs']['url'],
        url_params=TEST_PAGES['nested_divs']['params'],
        url_type='nested_divs')
    urls2 = ConstructReflowTimerUrls(
        url=TEST_PAGES['nested_tables']['url'],
        url_params=TEST_PAGES['nested_tables']['params'],
        url_type='nested_tables')
    urls = '%s,%s' % (','.join(urls1), ','.join(urls2))
    urls = urls.split(',')

  else:
    urls = ConstructReflowTimerUrls(
        url=TEST_PAGES[url_type]['url'],
        url_params=TEST_PAGES[url_type]['params'],
        url_type=url_type)

  urls = urls[start_index:]

  start_time = time.time()

  if run_style == '1':
    total_runs = len(urls) * len(browsers)
  else:
    total_runs = len(browsers)

  # wanna do it even more?
  tmpurls = urls[:]
  if num_runs > 1:
   for i in xrange(num_runs):
     print 'i:%s' % i
     for url in urls:
       print 'url: %s' % url
       tmpurls.append(url)
   urls = tmpurls[1:]

  print 'Total Runs: %s, URLs: %s, starting at %s' % (total_runs, len(urls),
                                                      start_time)
  print '--------------------------------------'
  time.sleep(3)

  i = 1
  for browser in browsers:
    if run_style == '1':
      for url in urls:
        print '>---------------->'
        print '%s of %s' % (i, total_runs)
        runReflowTimer(selenium_host, browser, url)
        print 'DONE'
        print '<----------------<'
        # Just a little bit of sleepy room.
        time.sleep(2)
        i += 1
    elif run_style == '2':
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

