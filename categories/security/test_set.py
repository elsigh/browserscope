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
      doc: a description of the test
      value_range: (min_value, max_value) as integer values
    """
    test_set_base.TestBase.__init__(
        self,
        key=key,
        name=name,
        url=self.TESTS_URL_PATH,
        doc=doc,
        min_value=0,
        max_value=1)


_TESTS = (
  # key, name, doc
  SecurityTest('postMessage API', 'postMessage',
  '''Checks whether the browser supports the
  <a href="http://www.whatwg.org/specs/web-apps/current-work/multipage/comms.html#crossDocumentMessages">HTML 5
  cross-document messaging</a> API that enables secure communication between origins.'''),
  SecurityTest('JSON.parse API', 'JSON.parse',
  '''Checks whether the browser natively supports the <a href="http://json.org/js.html">JSON.parse</a> API.
  Native JSON parsing is safer than using eval.'''),
  SecurityTest('toStaticHTML API', 'toStaticHTML',
  '''Checks whether the browser supports the
  <a href="http://msdn.microsoft.com/en-us/library/cc848922%28VS.85%29.aspx">toStaticHTML API</a>
  for sanitizing untrusted inputs.'''),
  SecurityTest('httpOnly cookie API', 'httpOnly cookies',
  '''Checks whether the browser supports the
  <a href="http://tools.ietf.org/html/draft-abarth-cookie-02#section-5.1.6">httpOnly cookie attribute</a>,
  which is a mitigation for cross-site scripting attacks.'''),
  SecurityTest('X-Frame-Options',
               'X-Frame-Options',
  '''Checks whether the browser supports the
  <a href="http://blogs.msdn.com/ie/archive/2009/01/27/ie8-security-part-vii-clickjacking-defenses.aspx">X-Frame-Options API</a>,
  which prevents clickjacking attacks by restricting how pages may be framed.'''),
  SecurityTest('X-Content-Type-Options',
               'X-Content-Type-Options',
  '''Checks whether the browser supports the <a href="http://blogs.msdn.com/ie/archive/2008/07/02/ie8-security-part-v-comprehensive-protection.aspx">X-Content-Type-Options API</a>,
  which <a href="http://www.adambarth.com/papers/2009/barth-caballero-song.pdf">prevents MIME sniffing</a>.'''),
  SecurityTest('Block reflected XSS', 'Block reflected XSS',
  '''Checks whether the browser blocks execution of JavaScript code that appears in the request
  URL. Browser-based XSS filters mitigate some classes of cross-site scripting attacks.'''),
  SecurityTest('Block location spoofing', 'Block location spoofing',
  '''The global "location" object can be used by JavaScript to determine what page it is
  executing on. It is used by Flash Player, Google AJAX API, and many bookmarklets.
  Browsers should block
  <a href="http://www.adambarth.com/papers/2009/adida-barth-jackson.pdf">JavaScript rootkits</a>
  that try to overwrite the location object.'''),
  SecurityTest('Block JSON hijacking', 'Block JSON hijacking',
  '''Documents encoded in JSON format can be read across domains if the browser
  supports a
  <a href="http://www.fortify.com/advisory.jsp">mutable Array constructor</a>
  that is called when array literals are encountered. JSON hijacking is also possible if the
  browser supports a
  <a href="http://haacked.com/archive/2009/06/25/json-hijacking.aspx">mutable setter function</a>
  for the Object prototype that is called when object literals are encountered.'''),
  SecurityTest('Block XSS in CSS', 'Block XSS in CSS',
  '''Script in stylesheets can be used by attackers to evade server-side XSS filters.
  Support for CSS expressions has been
  <a href="http://blogs.msdn.com/ie/archive/2008/10/16/ending-expressions.aspx">discontinued
  in IE8 standards mode</a> and XBL in stylesheets has been
  <a href="http://www.mozilla.org/security/announce/2009/mfsa2009-18.html">restricted
  to same-origin code in separate files</a> in Firefox. We check to make sure that script injected
  into a site via stylesheet does not execute.'''),
  SecurityTest('Sandbox attribute',
               'Sandbox attribute',
  '''Checks whether the browser supports the
  <a href="http://www.whatwg.org/specs/web-apps/current-work/#attr-iframe-sandbox">sandbox attribute</a>,
  which enables a set of extra restrictions on any content hosted by the iframe.'''),
  SecurityTest('Origin header',
               'Origin header',
  '''Checks whether the browser supports the
  <a href="http://tools.ietf.org/html/draft-abarth-origin">Origin header</a>, which is a mitigation for
  <a href="http://en.wikipedia.org/wiki/Cross-site_request_forgery">cross-site request forgery</a> (CSRF) attacks.'''),
  SecurityTest('Strict Transport Security',
               'Strict Transport Security',
  '''Checks whether the browser supports
  <a href="http://lists.w3.org/Archives/Public/www-archive/2009Sep/att-0051/draft-hodges-strict-transport-sec-05.plain.html">Strict Transport Security</a>,
  which enables web sites to declare themselves accessible only via secure connections.'''),
  SecurityTest('Cross-origin CSS loading',
               'Cross-origin CSS loading',
  '''Cross-domain stylesheet loading can be used by web attackers to steal data on victim websites via
  <a href="http://scarybeastsecurity.blogspot.com/2009/12/generic-cross-browser-cross-domain.html">CSS string injection</a>.
  We check whether the browser prevents loading cross-domain malformed stylesheets with broken MIME.'''),
)


class SecurityTestSet(test_set_base.TestSet):

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
    """
    logging.info('security getrowscore results: %s' % results)

    total_tests = 0
    total_valid_tests = 0
    total_score = 0
    tests = self.tests
    for test in tests:
      total_tests += 1

      if results.has_key(test.key) and results[test.key]['raw_score'] is not None:
        score = results[test.key]['score']
        logging.info('test: %s, score: %s' % (test.key, score))
        total_valid_tests += 1
        # For booleans, when "score" is 100 that's test_type true.
        if score == 100:
          total_score += 1
      else:
        logging.info('test: %s has no median' % test.key)

    #logging.info('%s, %s, %s' % (total_score, total_tests, total_valid_tests))
    score = int(round(100 * total_score / total_tests))
    display = '%s/%s' % (total_score, total_valid_tests)

    return score, display


TEST_SET = SecurityTestSet(
    category=_CATEGORY,
    category_name='Security',
    tests=_TESTS,
    test_page='/%s/test_tpl' % _CATEGORY
)
