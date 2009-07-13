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

"""Network Tests Definitions."""


from controllers import test_set_base


_CATEGORY = 'network'


class NetworkTest(object):
  TESTS_URL_PATH = '/%s/tests' % _CATEGORY

  def __init__(self, key, name, url_name, score_type, doc,
               value_range=None, is_hidden_stat=False):
    """Initialze a network test.

    Args:
      key: key for this in dict's
      name: a human readable label for display
      url_name: the name used in the url
      score_type: 'boolean' or 'custom'
      doc: a description of the test
      value_range: (min_value, max_value) as integer values
      is_hidden_stat: whether or not the test shown in the stats table
    """
    self.key = key
    self.name = name
    self.url = '%s/%s' % (self.TESTS_URL_PATH, url_name)
    self.score_type = score_type
    self.doc = doc
    self.is_hidden_stat = is_hidden_stat
    if value_range:
      self.min_value, self.max_value = value_range
    elif score_type == 'boolean':
      self.min_value, self.max_value = 0, 1
    else:
      self.min_value, self.max_value = 0, 60

  def GetScoreAndDisplayValue(self, median):
    """Returns a tuple with display text for the cell as well as a 1-100 value.
    i.e. ('1X', 95)
    """
    #logging.info('CustomTestsFunction w/ %s, %s' % (test, median))
    score = 0
    if 'hostconn' == self.key:
      if median <= 2:
        score = 60
      elif median <= 4:
        score = 85
      else:
        score = 95
    return score, str(median)


_TESTS = (
  # key, name, url_name, score_type, doc
  NetworkTest(
    'latency', 'Check Latency', 'latency', 'custom',
    '''add doc''',
    value_range=(0, 60000),
    is_hidden_stat=True),
  NetworkTest(
    'hostconn', 'Connections per Hostname', 'connections-per-hostname',
    'custom',
    '''add doc'''),
  NetworkTest(
    'maxconn', 'Max Connections', 'max-connections', 'custom',
    '''add doc'''),
  NetworkTest(
    'parscript', 'Parallel Scripts', 'scripts-block', 'boolean',
    '''add doc'''),
  NetworkTest(
    'parsheet', 'Parallel Stylesheets', 'stylesheets-block', 'boolean',
    '''add doc'''),
  NetworkTest(
    'parcssjs', 'Parallel Stylesheet and Inline Script',
    'inline-script-after-stylesheet', 'boolean',
    '''add doc'''),
  NetworkTest(
    'cacheexp', 'Cache Expires', 'cache-expires', 'boolean',
    '''add doc'''),
  NetworkTest(
    'cacheredir', 'Cache Redirects', 'cache-redirects', 'boolean',
    '''add doc'''),
  NetworkTest(
    'cacheresredir', 'Cache Resource Redirects', 'cache-resource-redirects',
    'boolean' ,
    '''add doc'''),
  NetworkTest(
    'prefetch', 'Link Prefetch', 'link-prefetch', 'boolean',
    '''add doc'''),
  NetworkTest(
    'gzip', 'Compression Supported', 'gzip', 'boolean' ,
    '''add doc'''),
  NetworkTest(
    'du', 'data: URLs', 'data-urls', 'boolean' ,
    '''add doc'''),
)

_CATEGORY = 'network'
TEST_SET = test_set_base.TestSet(
    category=_CATEGORY,
    category_name='Network',
    subnav={
      'Test': '/%s/test' % _CATEGORY,
      'About': '/%s/about' % _CATEGORY,
    },
    home_intro = '''A significant performance bottleneck for web pages is
      network performance. It's true that network performance depends in
      part on the user's connection speed and geographic location. But
      the browser also plays a significant role. By supporting features
      such as <code>data:</code> URLs, prefetch links, and parallel script
      downloading, browsers can make all web pages load faster.''',
    tests=_TESTS
)
