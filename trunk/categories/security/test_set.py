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

"""Benchmark Tests Definitions."""

import logging

from categories import test_set_base


_CATEGORY = 'security'


class SecurityTest(test_set_base.TestBase):
  TESTS_URL_PATH = '/%s/test' % _CATEGORY

  def __init__(self, key, name, doc):
    """Initialze a benchmark test.

    Args:
      key: key for this in dict's
      name: a human readable label for display
      url_name: the name used in the url
      score_type: 'boolean' or 'custom'
      doc: a description of the test
      value_range: (min_value, max_value) as integer values
    """
    test_set_base.TestBase.__init__(
        self,
        key=key,
        name=name,
        url=self.TESTS_URL_PATH,
        score_type='boolean',
        doc=doc,
        min_value=0,
        max_value=1)


_TESTS = (
  # key, name, doc
  SecurityTest('postMessage API', 'postMessage API', 
  '''Checks whether the browser supports the 
  <a href="http://www.whatwg.org/specs/web-apps/current-work/multipage/comms.html#crossDocumentMessages">HTML 5 
  cross-document messaging</a> API that enables secure communication between origins.'''),
  SecurityTest('JSON.parse API', 'JSON.parse API', 
  '''Checks whether the browser natively supports the <a href="http://json.org/js.html">JSON.parse</a> API. 
  Native JSON parsing is safer than using eval.'''),
  SecurityTest('toStaticHTML API', 'toStaticHTML API', 
  '''Checks whether the browser supports the 
  <a href="http://msdn.microsoft.com/en-us/library/cc848922%28VS.85%29.aspx">toStaticHTML API</a> 
  for sanitizing untrusted inputs.'''),
  SecurityTest('httpOnly cookie API', 'httpOnly cookie API', 
  '''Checks whether the browser supports the
  <a href="http://tools.ietf.org/html/draft-abarth-cookie-02#section-5.1.6">httpOnly cookie attribute</a>,
  which is a mitigation for cross-site scripting attacks.'''),
  SecurityTest('Block reflected XSS', 'Block reflected XSS', 
  '''Checks whether the browser blocks execution of JavaScript code that appears in the request 
  URL. Browser-based XSS filters mitigate some classes of cross-site scripting attacks.'''),
  SecurityTest('Block location spoofing', 'Block location spoofing', 
  '''The global "location" object can be used by JavaScript to determine what page it is
  executing on. It is used by Flash Player, Google AJAX API, and many bookmarklets. 
  Browsers should block 
  <a href="http://www.adambarth.com/papers/2009/adida-barth-jackson.pdf">JavaScript rootkits</a>
  that try to overwrite the location object.'''),
  SecurityTest('Block window.top spoofing', 'Block window.top spoofing',
  '''The global "top" variable is used by JavaScript to determine the URL of the main frame of the current
  tab. It is used for frame busting, and Flash Player also uses it
  to enforce its third-party cookie blocking policy. Browsers should block
  <a href="http://www.adambarth.com/papers/2009/adida-barth-jackson.pdf">JavaScript rootkits</a>
  that try to overwrite the top object.'''),
  SecurityTest('Block JSON hijacking', 'Block JSON hijacking',
  '''Documents encoded in JSON format can be read across domains if the browser
  supports a 
  <a href="http://www.fortify.com/advisory.jsp">mutable Array constructor</a>
  that is called when array literals are encountered. JSON hijacking is also possible if the
  browser supports a 
  <a href="http://haacked.com/archive/2009/06/25/json-hijacking.aspx">mutable setter function</a>
  for the Object prototype that is called when object literals are encountered.'''),
  SecurityTest('Block CSS expressions', 'Block CSS expressions', 
  '''CSS Expressions are commonly used by attackers to evade server-side XSS filters.
  They are proprietary to Internet Explorer and their support has been 
  <a href="http://blogs.msdn.com/ie/archive/2008/10/16/ending-expressions.aspx">discontinued
  in IE8 standards mode</a>.'''),
  SecurityTest('Block cross-origin document', 'Block cross-origin document',
  '''Browsers should block cross-origin access to a frame's document to reduce the risk of
  <a href="http://www.adambarth.com/papers/2009/barth-weinberger-song.pdf">cross-origin capability leaks</a>.
  Accessing this property across origins is 
  <a href="http://www.whatwg.org/specs/web-apps/current-work/multipage/browsers.html#security-2">prohibited
  by HTML5</a>.'''),
  SecurityTest('Block cross-origin contentDocument',
               'Block cross-origin contentDocument', 
  '''Browsers should block cross-origin access to a frame's contentDocument to reduce the risk of
  <a href="http://www.adambarth.com/papers/2009/barth-weinberger-song.pdf">cross-origin capability leaks</a>.
  Accessing this property across origins is 
  <a href="http://www.whatwg.org/specs/web-apps/current-work/multipage/browsers.html#security-2">prohibited
  by HTML5</a>.'''),
  SecurityTest('Block UTF-7 sniffing', 'Block UTF-7 sniffing',
  '''This test checks whether the browser will automatically detect UTF-7 
  encoded HTML documents.
  <a href="http://code.google.com/p/browsersec/wiki/Part2">UTF-7 sniffing 
  is not recommended</a> because an attacker may use it to bypass cross-site
  scripting filters.'''),
  SecurityTest('Block all UTF-7', 'Block all UTF-7',
  '''The UTF-7 encoding is prone to cross-site scripting attacks and is not 
  recommended for HTML documents. This test checks to see whether UTF-7 encoding
  is completely blocked.'''),
)


class SecurityTestSet(test_set_base.TestSet):

  def GetRowScoreAndDisplayValue(self, results):
    """Get the overall score for this row of results data.
    Args:
      results: A dictionary that looks like:
      {
        'testkey1': {'score': 1-10, 'median': median, 'display': 'celltext'},
        'testkey2': {'score': 1-10, 'median': median, 'display': 'celltext'},
        etc...
      }

    Returns:
      A tuple of (score, display)
      Where score is a value between 1-100.
      And display is the text for the cell.

    """
    #logging.info('network getrowscore results: %s' % results)

    total_tests = 0
    total_valid_tests = 0
    total_score = 0
    tests = self.tests
    for test in tests:
      total_tests += 1
      if results.has_key(test.key):
        score = results[test.key]['score']
        #logging.info('test: %s, score: %s' % (test.key, score))
        total_valid_tests += 1
        # For booleans, when "score" is 10 that's test_type true.
        if score == 10:
          total_score += 1

    #logging.info('%s, %s, %s' % (total_score, total_tests, total_valid_tests))
    score = int(round(100 * total_score / total_tests))
    display = '%s/%s' % (total_score, total_valid_tests)

    return score, display


TEST_SET = SecurityTestSet(
    category=_CATEGORY,
    category_name='Security',
    tests=_TESTS,
    test_page='/%s/static/%s.html' % (_CATEGORY, _CATEGORY)
)
