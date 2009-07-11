#!/usr/bin/python

import code
import getpass
import os
import sys
import time


sys.path.append('../../')
sys.path.append('../../../google_appengine')
sys.path.append('../../../google_appengine/lib/yaml/lib')
sys.path.append('../../../google_appengine/lib/webob')
sys.path.append('../../../google_appengine/lib/antlr3')
print sys.path

from google.appengine.ext.remote_api import remote_api_stub
from google.appengine.ext import db

os.environ['SERVER_SOFTWARE'] = 'REMOTE'
from appengine_django import InstallAppengineHelperForDjango
InstallAppengineHelperForDjango()

from models.result import *
from models.user_agent import *

# Data structures for reflow testing.
from run_reflow_timer import TEST_PAGES


TOP_USER_AGENTS = [
  'Chrome 1', 'Chrome 2',
  'Firefox 3.0', 'Firefox 3.1',
  'IE 6', 'IE 7',
  'Opera 9', 'Opera 10',
  'Safari 3', 'Safari 4'
]
#TOP_USER_AGENTS = ['IE 8']

TEST_PAGE = 'foo'
TESTS = (
  ('testDisplay', 'Display Block', '%s?t=testDisplay' % TEST_PAGE, 'custom'),
  ('testVisibility', 'Visiblility None', '%s?t=testVisibility' % TEST_PAGE, 'custom'),
  ('testNonMatchingClass', 'Non Matching by Class', '%s?t=testNonMatchingClass' % TEST_PAGE, 'custom'),
  ('testFourClassReflows', 'Four Reflows by Class', '%s?t=testFourReflowsClass' % TEST_PAGE, 'custom'),
  ('testFourScriptReflows', 'Four Reflows by Script', '%s?t=testFourScriptReflows' % TEST_PAGE, 'custom'),
  ('testTwoScriptReflows', 'Two Reflows by Script', '%s?t=testTwoScriptReflows' % TEST_PAGE, 'custom'),
  ('testMarginPx', 'Margin px', '%s?t=testMarginPx' % TEST_PAGE, 'custom'),
  ('testPaddingPx', 'Padding px', '%s?t=testPaddingPx' % TEST_PAGE, 'custom'),
  ('testPaddingLeftPx', 'Padding Left px', '%s?t=testPaddingLeftPx' % TEST_PAGE, 'custom'),
  ('testFontSizeEm', 'Font Size em', '%s?t=testFontSizeEm' % TEST_PAGE, 'custom'),
  ('testWidthPercent', 'Width %', '%s?t=testWidthPercent' % TEST_PAGE, 'custom'),
  ('testBackground', 'Background Color', '%s?t=testBackground' % TEST_PAGE, 'custom'),
  ('testOverflowHidden', 'Overflow Hidden', '%s?t=testOverflowHidden' % TEST_PAGE, 'custom'),
  ('testSelectorMatchTime', 'Selector Match Time', '%s?t=testSelectorMatchTime' % TEST_PAGE, 'custom'),
  ('testGetOffsetHeight', 'Do Nothing / OffsetHeight', '%s?t=testSelectorMatchTime' % TEST_PAGE, 'custom'),
)

def ConstructTestPageParamCombinations(params, url_type):
  """A list of category,param=val,param2=val2, etc..:
  [u'nested_anchors', u'num_elements=1000', u'num_nest=10',
   u'css_selector=%23g-content%20div', u'num_css_rules=0',
   u'css_text=border%3A%201px%20solid%20%230C0%3B%20padding%3A%208px%3B']
  """

  param_combos = []
  if url_type == 'nested_anchors':
    num_element_key = -1
    for num_elements in params['num_elements']:
      num_element_key += 1
      num_nest_key = -1
      for num_nest in params['num_nest']:
        num_nest_key += 1
        css_selector_key = -1
        for css_selector in params['css_selector']:
          css_selector_key += 1
          num_css_rules_key = -1
          for num_css_rules in params['num_css_rules']:
            num_css_rules_key += 1
            css_text_key = -1
            for css_text in params['css_text']:
              css_text_key += 1
              params_array = [url_type,
                              'num_elements=%s' % num_elements,
                              'num_nest=%s' % num_nest,
                              'css_selector=%s' % css_selector,
                              'num_css_rules=%s' % num_css_rules,
                              'css_text=%s' % css_text]
              params_keys = [num_element_key, num_nest_key, css_selector_key,
                             num_css_rules_key, css_text_key]
              param_combos.append((params_array, params_keys))
  elif url_type == 'nested_divs' or url_type == 'nested_tables':
    for num_nest in params['num_nest']:
      params_array = [url_type, 'num_nest=%s' % num_nest]
      param_combos.append(params_array)
  return param_combos

def auth_func():
  return raw_input('Username:'), getpass.getpass('Password:')

if len(sys.argv) < 2:
  print 'Usage: %s app_id [host]' % (sys.argv[0],)
app_id = 'ua-profiler'
host= '%s.appspot.com' % app_id

#if len(sys.argv) > 2:
#  host = sys.argv[2]
#else:
#  host = '%s.appspot.com' % app_id

remote_api_stub.ConfigureRemoteDatastore(app_id, '/remote_api', auth_func, host)

url_type = 'nested_anchors'
params = TEST_PAGES[url_type]['params']
param_combos = ConstructTestPageParamCombinations(params, url_type)
#param_combos = param_combos[0:3]
#print param_combos


total_data_points = len(param_combos) * len(TOP_USER_AGENTS) * len(TESTS)

category = 'reflow'
headers = ('"num_elements", "num_nest", "css_selector", "num_css_rules", '
           '"css_text", "user_agent", "test", "median"')
f = open('/tmp/reflow.csv', 'w')
f.write('%s\n' % headers)

counter = 1
user_agent_version_key = -1
for user_agent_version in TOP_USER_AGENTS:
  user_agent_version_key += 1
  for param_combo in param_combos:
    params = param_combo[0]
    test_key = -1

    for test in TESTS:
      test_key += 1

      print 'Working on %s of %s data points...' % (counter, total_data_points)
      counter += 1

      params_keys = param_combo[1][:]
      params_keys.append(user_agent_version_key)
      params_keys.append(test_key)

      guid = ResultParent.guid(category, test.key, user_agent_version, params)
      start_time = time.time()
      try:
        print 'Working on ua: %s and params: %s' % (user_agent_version, params)

        count = ResultParent.get_total(guid)
        if count == 0:
          print 'No results yet for this one.'
          print '--------------------------------'
          continue

        median = ResultParent.get_median(guid)
        print 'Got median %s' % (median)

        end_time = time.time()
        print 'Time: %s sec.' % (end_time - start_time)

        print '--------------------------------'
        params_keys.append(median)
        f.write('%s\n' % ', '.join(map(str, params_keys)))

      except KeyboardInterrupt:
        raise

      except:
        end_time = time.time()
        print '********************************'
        print '********************************'
        print 'TIMEOUT? CRAP!'
        print 'Exception: %s' % sys.exc_info()[0]
        print 'Time: %s sec.' % (end_time - start_time)
        print '********************************'
        print '********************************'


f.close()
