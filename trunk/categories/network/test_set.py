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


from categories import test_set_base


_CATEGORY = 'network'


class NetworkTest(test_set_base.TestBase):
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
    self.url_name = url_name
    self.is_hidden_stat = is_hidden_stat
    if value_range:
      min_value, max_value = value_range
    elif score_type == 'boolean':
      min_value, max_value = 0, 1
    else:
      min_value, max_value = 0, 60
    test_set_base.TestBase.__init__(
        self,
        key=key,
        name=name,
        url='%s/test?testurl=%s' % (_CATEGORY, url_name),
        score_type=score_type,
        doc=doc,
        min_value=min_value,
        max_value=max_value)

  def GetScoreAndDisplayValue(self, median, medians=None, is_uri_result=False):
    """Custom scoring function.

    Args:
      median: The actual median for this test from all scores.
      medians: A dict of the medians for all tests indexed by key.
      is_uri_result: Boolean, if results are in the url, i.e. home page.
    Returns:
      (score, display)
      Where score is a value between 1-100.
      And display is the text for the cell.
    """
    #logging.info('Network.GetScoreAndDisplayValue '
    #             'test: %s, median: %s, tests: %s' % (self.key, median, tests))

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
    '''This isn't actually a test.
Many of the tests measure how long it takes for a resource to load, but the load time can vary greatly depending on the user's network latency.
This page measures the average latency to the UA Profiler server, and then adjusts the timing thresholds throughout the remaining
test pages accordingly.
If you have high latency (slow network connection), the tests take longer to load.
If you have low latency (fast network connection), the tests are run faster.''',
    value_range=(0, 60000),
    is_hidden_stat=True),
  NetworkTest(
    'hostconn', 'Connections per Hostname', 'connections-per-hostname',
    'custom',
    '''When HTTP/1.1 was introduced with persistent connections enabled by default, the suggestion was that browsers open only
two connections per hostname.
Pages that had 10 or 20 resources served from a single hostname loaded slowly because the resources were downloaded two-at-a-time.
Browsers have been increasing the number of connections opened per hostname, for example, IE went from 2 in IE7 to 6 in IE8.
This test measures how many HTTP/1.1 connections are opened for the browser being tested.'''),
  NetworkTest(
    'maxconn', 'Max Connections', 'max-connections', 'custom',
    '''The previous test measures maximum connections for a single hostname.
This test measures the maximum number of connections a browser will open total - across all hostnames.
The upper limit is 60, so if a browser actually supports more than that it'll still show up as 60.'''),
  NetworkTest(
    'parscript', 'Parallel Scripts', 'scripts-block', 'boolean',
    '''When most browsers start downloading an external script, they wait until the script is done downloading, parsed, and executed
before starting any other downloads. Although <i>parsing and executing</i> scripts in order is important for maintaining code dependencies,
it's possible to safely <i>download</i> scripts in parallel with other resources in the page (including other scripts).
This test determines if scripts can be downloaded in parallel with other resources in the page.'''),
  NetworkTest(
    'parsheet', 'Parallel Stylesheets', 'stylesheets-block', 'boolean',
    '''Similar to scripts, some browsers block all downloads once they start downloading a stylesheet.
This test determines if stylesheets can be downloaded in parallel with other resources in the page.'''),
  NetworkTest(
    'parcssjs', 'Parallel Stylesheet and Inline Script',
    'inline-script-after-stylesheet', 'boolean',
    '''A lesser known performance problem is the problems caused when a stylesheet is followed by an inline script block.
If a browser doesn't block when downloading stylesheets (as measured by the previous test), then a stylesheet followed by
an image could both be downloaded in parallel.
But suppose an inline script block was placed between the stylesheet's <code>LINK</code> tag and the image <code>IMG</code> tag.
The result, for some browsers, is that the image isn't downloaded until the stylesheet finishes.
The reason is that the image download must occur after the inline script block is executed
(in case the script block itself inserts images or in some other way manipulates the DOM),
and the inline script block doesn't execute until after the stylesheet is downloaded and parsed
(in case the inline script block depends on CSS rules in the stylesheet).
It's important to preserve the order of the stylesheet rules being applied to the page, followed by executing the inline script block, but
there's no reason other resources shouldn't be downloaded in parallel and not applied to the page until after the inline script block is executed.
A subtlety of this test is that if the test is determined to be a failure if the inline script is executed before the stylesheet is done
downloading - although this is faster it could lead to unexpected behavior.'''),
  NetworkTest(
    'cacheexp', 'Cache Expires', 'cache-expires', 'boolean',
    '''This test determines if a resource with a future expiration date is correctly read from the browser's cache, or issues an unnecessary HTTP request.
This is really testing the browser's memory cache.'''),
  NetworkTest(
    'cacheredir', 'Cache Redirects', 'cache-redirects', 'boolean',
    '''Many pages use redirects to send users from one page to another,
for example <a href="http://google.com/">http://google.com/</a> redirects to <a href="http://www.google.com/">http://www.google.com/</a>.
Unfortunately, most browsers don't pay attention to the cache headers of these redirects, and force the user to endure the redirect over and over again.
This test measures if a redirect for the page is cached when it has a future expiration date.'''),
  NetworkTest(
    'cacheresredir', 'Cache Resource Redirects', 'cache-resource-redirects',
    'boolean' ,
    '''Whereas the previous test measures redirect caching for the main page, this test measures redirect caching for resources in the page.'''),
  NetworkTest(
    'prefetch', 'Link Prefetch', 'link-prefetch', 'boolean',
    '''This test determines if the prefetch keyword for the link tag works.
(See the link prefetch description in this <a href="http://developer.mozilla.org/en/Link_prefetching_FAQ">MDC FAQ</a>
and in a working draft of the <a href="http://www.whatwg.org/specs/web-apps/current-work/#link-type10">HTML 5</a> spec.)
Prefetch is an easy way for web developers to download resources they know the user will need in the future.'''),
  NetworkTest(
    'gzip', 'Compression Supported', 'gzip', 'boolean' ,
    '''Compressing text responses typically reduces the number of bytes transmitted by approximately 70%.
This test measures if the browser sends an <code>Accept-Encoding</code> header announcing support for compression.'''),
  NetworkTest(
    'du', 'data: URLs', 'data-urls', 'boolean' ,
    '''A "data:" URL (aka an inline image), is a technique for embedding other resources directly into the main HTML document.
Doing this avoids an extra HTTP request.
This test checks if an image inserted using a "data:" URL is rendered correctly.'''),
)

_CATEGORY = 'network'
TEST_SET = test_set_base.TestSet(
    category=_CATEGORY,
    category_name='Network',
    tests=_TESTS
)
