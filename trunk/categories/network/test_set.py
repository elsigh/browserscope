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

"""Network Tests Definitions."""

import logging

from categories import test_set_base


_CATEGORY = 'network'


class NetworkTest(test_set_base.TestBase):
  TESTS_URL_PATH = '/%s/tests' % _CATEGORY

  def __init__(self, key, name, url_name, doc, min_value, max_value,
               is_hidden_stat=False, cell_align='center'):
    """Initialze a network test.

    Args:
      key: key for this in dict's
      name: a human readable label for display
      url_name: the name used in the url
      doc: a description of the test
      min_value: an integer
      max_value: an integer
      is_hidden_stat: whether or not the test shown in the stats table
      cell_align: 'right', 'left', or 'center' for output formating
    """
    test_set_base.TestBase.__init__(
        self,
        key=key,
        name=name,
        url='/%s/tests/%s' % (_CATEGORY, url_name),
        doc=doc,
        min_value=min_value,
        max_value=max_value,
        cell_align=cell_align,
        is_hidden_stat=is_hidden_stat)
    self.url_name = url_name


class BooleanNetworkTest(NetworkTest):
  def __init__(self, key, name, url_name, doc, **kwds):
    """Initialze a boolean network test.

    Args:
      key: key for this in dict's
      name: a human readable label for display
      url_name: the name used in the url
      doc: a description of the test
      kwds: any addition keyword parameters
    """
    NetworkTest.__init__(self, key, name, url_name, doc,
                         min_value=0, max_value=1, **kwds)


_TESTS = (
  # key, name, url_name, score_type, doc
  NetworkTest(
    'latency', 'Check Latency', 'latency',
    '''This isn't actually a test.
Many of the tests measure how long it takes for a resource to load, but the load time can vary greatly depending on the user's network latency.
This page measures the average latency to the UA Profiler server, and then adjusts the timing thresholds throughout the remaining
test pages accordingly.
If you have high latency (slow network connection), the tests take longer to load.
If you have low latency (fast network connection), the tests are run faster.''',
    min_value=0, max_value=60000,
    is_hidden_stat=True),
  NetworkTest(
    'hostconn', 'Connections per Hostname', 'connections-per-hostname',
    '''When HTTP/1.1 was introduced with persistent connections enabled by default, the suggestion was that browsers open only
two connections per hostname.
Pages that had 10 or 20 resources served from a single hostname loaded slowly because the resources were downloaded two-at-a-time.
Browsers have been increasing the number of connections opened per hostname, for example, IE went from 2 in IE7 to 6 in IE8.
This test measures how many HTTP/1.1 connections are opened for the browser being tested.''',
    min_value=0, max_value=60,
    cell_align='right'),
  NetworkTest(
    'maxconn', 'Max Connections', 'max-connections',
    '''The previous test measures maximum connections for a single hostname.
This test measures the maximum number of connections a browser will open total - across all hostnames.
The upper limit is 60, so if a browser actually supports more than that it'll still show up as 60.''',
    min_value=0, max_value=60,
    cell_align='right'),
  # parscript is deprecated.
  #BooleanNetworkTest(
  #  'parscript', '|| Scripts', 'scripts-block', '', is_hidden_stat=True),
  BooleanNetworkTest(
    'parscriptscript', '|| Script Script', 'scripts-block-scripts',
    '''When some browsers start downloading an external script, they wait until the script is done downloading, parsed, and executed
before starting any other downloads. Although <i>parsing and executing</i> scripts in order is important for maintaining code dependencies,
it's possible to safely <i>download</i> scripts in parallel with other resources in the page (including other scripts).
This test determines if the browser downloads scripts in parallel with other scripts in the page.'''),
  BooleanNetworkTest(
    'parscriptstylesheet', '|| Script Stylesheet', 'scripts-block-stylesheets',
    '''When some browsers start downloading an external script, they wait until the script is done downloading, parsed, and executed
before starting any other downloads. Although <i>parsing and executing</i> scripts in order is important for maintaining code dependencies,
it's possible to safely <i>download</i> scripts in parallel with other resources in the page (including other scripts).
This test determines if the browser downloads scripts in parallel with other stylesheets in the page.'''),
  BooleanNetworkTest(
    'parscriptimage', '|| Script Image', 'scripts-block-images',
    '''When some browsers start downloading an external script, they wait until the script is done downloading, parsed, and executed
before starting any other downloads. Although <i>parsing and executing</i> scripts in order is important for maintaining code dependencies,
it's possible to safely <i>download</i> scripts in parallel with other resources in the page (including other scripts).
This test determines if the browser downloads scripts in parallel with other images in the page.'''),
  BooleanNetworkTest(
    'parscriptiframe', '|| Script Iframe', 'scripts-block-iframes',
    '''When some browsers start downloading an external script, they wait until the script is done downloading, parsed, and executed
before starting any other downloads. Although <i>parsing and executing</i> scripts in order is important for maintaining code dependencies,
it's possible to safely <i>download</i> scripts in parallel with other resources in the page (including other scripts).
This test determines if the browser downloads scripts in parallel with other iframes in the page.'''),
  BooleanNetworkTest(
    'scriptasync', 'Async Scripts', 'scripts-async',
    '''HTML5 introduced the async attribute for script tags.  This allows page authors to specify that their scripts can safely load
in the background, independent of the other scripts in the page.  This test determines if the browser supports the async attribute.'''),
  BooleanNetworkTest(
    'parsheet', '|| CSS', 'stylesheets-block',
    '''Similar to scripts, some browsers block all downloads once they start downloading a stylesheet.
This test determines if stylesheets can be downloaded in parallel with other resources in the page.'''),
  BooleanNetworkTest(
    'parcssjs', '|| CSS + Inline Script',
    'inline-script-after-stylesheet',
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
  BooleanNetworkTest(
    'cacheexp', 'Cache Expires', 'cache-expires',
    '''This test determines if a resource with a future expiration date is correctly read from the browser's cache, or issues an unnecessary HTTP request.
This is really testing the browser's memory cache.'''),
  BooleanNetworkTest(
    'cacheredir', 'Cache Redirects', 'cache-redirects',
    '''Many pages use redirects to send users from one page to another,
for example <a href="http://google.com/">http://google.com/</a> redirects to <a href="http://www.google.com/">http://www.google.com/</a>.
Unfortunately, most browsers don't pay attention to the cache headers of these redirects, and force the user to endure the redirect over and over again.
This test measures if a redirect for the page is cached when it has a future expiration date.'''),
  BooleanNetworkTest(
    'cacheresredir', 'Cache Resource Redirects', 'cache-resource-redirects',
    '''Whereas the previous test measures redirect caching for the main page, this test measures redirect caching for resources in the page.'''),
  BooleanNetworkTest(
    'prefetch', 'Link Prefetch', 'link-prefetch',
    '''This test determines if the prefetch keyword for the link tag works.
(See the link prefetch description in this <a href="http://developer.mozilla.org/en/Link_prefetching_FAQ">MDC FAQ</a>
and in a working draft of the <a href="http://www.whatwg.org/specs/web-apps/current-work/#link-type10">HTML 5</a> spec.)
Prefetch is an easy way for web developers to download resources they know the user will need in the future.'''),
  BooleanNetworkTest(
    'gzip', 'Compression Supported', 'gzip',
    '''Compressing text responses typically reduces the number of bytes transmitted by approximately 70%.
This test measures if the browser sends an <code>Accept-Encoding</code> header announcing support for compression.'''),
  BooleanNetworkTest(
    'du', 'data: URLs', 'data-urls',
    '''A "data:" URL (aka an inline image), is a technique for embedding other resources directly into the main HTML document.
Doing this avoids an extra HTTP request.
This test checks if an image inserted using a "data:" URL is rendered correctly.'''),
  #BooleanNetworkTest(
  #  'trailer', 'Headers in trailer', 'trailer',
  #  '''This test checks if sending headers in the trailer of a chunked HTTP #response is supported by the browser.'''),
)


class NetworkTestSet(test_set_base.TestSet):

  def GetTestScoreAndDisplayValue(self, test_key, raw_scores):
    """Get a normalized score (0 to 100) and a value to output to the display.

    Args:
      test_key: a key for a test_set test.
      raw_scores: a dict of raw_scores indexed by test keys.
    Returns:
      score, display_value
          # score is from 0 to 100.
          # display_value is the text for the cell.
    """
    score = 0
    raw_score = raw_scores.get(test_key, None)
    if raw_score is None:
      return 0, ''
    if test_key == 'hostconn':
      if raw_score > 2:
        score = 100
      elif raw_score == 2:
        score = 50
      elif raw_score == 1:
        score = 1
      else:
        score = 0
    elif test_key == 'maxconn':
      if raw_score > 20:
        score = 100
      elif raw_score >= 10:
        score = 50
      elif raw_score > 1:
        score = 1
      else:
        score = 0
    return score, str(raw_score)

  def GetRowScoreAndDisplayValue(self, results):
    """Get the overall score for this row of results data.

    Args:
      results: {
          'test_key_1': {'score': score_1, 'raw_score': raw_score_1, ...},
          'test_key_2': {'score': score_2, 'raw_score': raw_score_2, ...},
          ...
          }
    Returns:
      score, display_value
          # score is from 0 to 100.
          # display_value is the text for the cell.

    Why do we use totalTests as the divisor for "score", but totalValidTests as the divisor for "display"?
    There are going to be old browsers that are no longer tested. They might have gotten 6/8 (75%)
    back in the old days, but now we've added more tests and they'd be lucky to get 6/12 (50%). If
    we compare 6/8 to newer browsers that get 8/12, the old browser would win, even though it would
    fail in side-by-side testing, so we have to use totalTests as the divisor for "score".
    But we can't misrepresent the actual tests that were performed, so we have to show the user the
    actual number of tests for which we have results, which means using totalValidTests as the divisor
    for "display".
    """
    total_tests = 0
    total_valid_tests = 0
    total_score = 0
    for test in self.VisibleTests():
      total_tests += 1
      if test.key in results and results[test.key]['score'] is not None:
        # For booleans, when "score" is 100 that's test_type true.
        # steve's custom score for hostconn & maxconn map
        # simply to 10 for good, 5 for ok, and 0 for fail, but we only award
        # a point for a 10 on those.
        if results[test.key]['score'] == 100:
          total_score += 1
        total_valid_tests += 1
    score = int(round(100.0 * total_score / total_tests))
    display = '%s/%s' % (total_score, total_valid_tests)
    return score, display


TEST_SET = NetworkTestSet(
    category=_CATEGORY,
    category_name='Network',
    tests=_TESTS,
#    test_page=util.MULTI_TEST_DRIVER_TEST_PAGE
    test_page='/multi_test_frameset'
)
