#!/usr/bin/python2.4
#
# Copyright 2009 Google Inc. All Rights Reserved.

"""This is a generic test to test CSS reflow speed of a given URL."""

__author__ = 'elsigh@google.com (Lindsey Simon)'
__version__ = '0.1'

import logging
import re
import sys
import time
import getopt
import time
import os
import unittest

from selenium import selenium


logging.getLogger().setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

# Default flags.
FLAGS = {'selenium_host': 'localhost',
         'selenium_port': str(4444),
         'browser_start_command': '*firefox',
         'browser_urls': ['http://www.google.com/'],
         'do_beacon': True}

SERVER = 'ua-profiler.appspot.com'
#SERVER = 'localhost:8084'

RESULTS_F = None

class TestReflowTime(unittest.TestCase):
  """Creates a selenium farm client for testing CSS / browser rendering."""

  def setUp(self):
    """Class-level setUp function to start the Selenium connection."""
    logging.debug('setUp...')
    self.selenium_host = FLAGS['selenium_host']
    self.selenium_port = FLAGS['selenium_port']
    logging.debug('Selenium host is %s:%s' % (self.selenium_host,
                                             self.selenium_port))
    self.browser_start_command = FLAGS['browser_start_command']
    logging.debug('browser_start_command: %s' % self.browser_start_command)
    self.browser_urls = FLAGS['browser_urls']
    #logging.debug('browser_urls: %s' % self.browser_urls)

    # Start Selenium
    self.selenium = selenium(self.selenium_host, self.selenium_port,
                             self.browser_start_command, self.browser_urls[0])
    self.selenium.start()
    logging.debug('Selenium (%s) is ready.' % self.browser_start_command)


  def tearDown(self):
    """Class-level setUp function to start the Selenium connection."""
    logging.debug('tearDown...')

    # Stop the Selenium client
    if self.selenium:
      self.selenium.stop()
      time.sleep(3)

      self.selenium = None
      logging.debug('Selenium instance stopped.')


  def testReflow(self):
    """Test Reflow Time of an url by injecting our bookmarklet."""

    total_urls = len(self.browser_urls)
    i = 1
    for browserUrl in self.browser_urls:

      # Perform the tests on all browser/os combinations.
      logging.debug('Opening %s of %s, url(%s)...' %
                    (i, total_urls, browserUrl))
      i += 1
      self.selenium.set_timeout(100000)
      self.selenium.open(browserUrl)

      # Resize the window to something consistent.
      self.selenium.get_eval('this.browserbot.getCurrentWindow()' +
                             '.resizeTo(1280, 1000)')

      if FLAGS['do_beacon'] == True:
        js_file = 'reflow_timer_callback.js'
      else:
        js_file = 'reflow_timer_visual.js'
      script_src = 'http://%s/js/reflow/%s' % (SERVER, js_file)

      # Injects the script.
      bookmarklet = ("(function(){"
          "_rnd=Math.floor(Math.random()*1000);"
          "_src='%s?rnd='+_rnd;"
          "_document=selenium.browserbot.getCurrentWindow().document;"
          "_my_script=_document.createElement('SCRIPT');"
          "_my_script.type='text/javascript';_my_script.src=_src;"
          "_document.getElementsByTagName('head')[0].appendChild(_my_script);"
          "})();" % script_src)

      self.selenium.get_eval(bookmarklet)
      logging.debug('Injected the bookmarklet, running the reflow tests.')

      # Block on the creation of the hidden input with id="rt-results"
      condition_string = ("eval(selenium.browserbot.getCurrentWindow().document"
                          ".getElementById('rt-results') != null)")
      # 20 minute timeout
      timeout = 12000000
      self.selenium.wait_for_condition(condition_string, timeout);

      # The value of this hidden input element has all of the times in it.
      results = self.selenium.get_value('rt-results')
      logging.info('rez:  ' + results)

      # Format in CSV for the outfile
      result_bits = results.split(',')
      vals = [browserUrl]
      for bits in result_bits:
        token, val = bits.split(':')
        vals.append(val)

      # We'll write out to a browser specific outfile.
      filename = re.sub('[^a-zA-Z0-9_\-.() ]+', '', self.browser_start_command)
      RESULTS_F = open('reflows_%s.csv' % filename, 'a')
      RESULTS_F.write('"%s"\n' % '", "'.join(vals))
      logging.debug('Reflow complete w/ results: %s, for url:%s!' %
                    (results, browserUrl))

    self.selenium.close()
    time.sleep(5)
    # maybe it will really close, yes - seems this works!


def PrintUsage():
  """Prints out usage information."""

  print 'Example Usage:'
  print ('  ./reflow_timer.py '
         '--browser_urls="http://www.google.com/" '
         '--browser_start_command="*firefox"')


def ParseFlags(argv):
  """Parse command line flags."""
  i = 1  # Skips the program name.
  while i < len(argv):
    logging.debug('Testing flag: %s' % argv[i])
    for flag in FLAGS:
      prefix = '--' + flag + '='
      if argv[i].startswith(prefix):
        value = argv[i][len(prefix):]
        if isinstance(FLAGS[flag], list):
          FLAGS[flag] = value.split(',')
        else:
          FLAGS[flag] = value
        #logging.debug('FLAGS set %s to %s' % (flag, value))
        del argv[i]
        break

  # If argv is > 1 then we didn't strip off some flag we should've
  # and that means the user passed in an unknown flag.
  if len(argv) > 1:
    PrintUsage()
    sys.exit(2)


if __name__ == '__main__':
  ParseFlags(sys.argv)
  unittest.main()
