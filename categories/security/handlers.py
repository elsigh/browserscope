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

"""Handlers for the Browserscope Security Tests."""

from Cookie import Morsel
import logging

from base import util
from django.http import HttpResponse
from django.http import HttpResponsePermanentRedirect

CATEGORY = 'security'


def About(request):
  """About page."""
  overview = """This page contains a suite of security tests that measure
    whether the browser supports JavaScript APIs that allow safe
    interactions between sites, and whether it follows industry
    best practices for blocking harmful interactions between sites.
    The initial set of tests were contributed by
    <a href="http://www.adambarth.com/">Adam Barth</a>,
    <a href="http://www.collinjackson.com/">Collin Jackson</a>,
    <a href="http://www.google.com/profiles/meacer">Mustafa Acer</a>,
    and <a href="http://linshunghuang.googlepages.com/">David Lin-Shung Huang</a>."""
  return util.About(request, CATEGORY, overview=overview)





def Test(request):
  response = util.Render(request, 'templates/test.html', params={},
                         category=CATEGORY)
  response.set_cookie('regularTestCookie', '1', expires=None, path='/security/')
  response.set_cookie('httpOnlyTestCookie', '1', expires=None,
                      path='/security/')

  # This is a really naughty bunch of hacks to get around that fact that we
  # switched from our own Django.zip (django1.2) to the built-in django1.1
  # in App Engine. response.set_cookie does not know about the httpOnly
  # attribute in django1.1, so we need to modify the cookie output routine
  # to append httpOnly for out httpOnlyTestCookie.
  # -elsigh
  def httpOnlyAwareMorselOutputString(self, attrs=None):
    output = self.OriginalOutputString(attrs)
    if self.__dict__['key'] == 'httpOnlyTestCookie':
      output += "; httpOnly"
    return output
  morsel = response.cookies['httpOnlyTestCookie']
  OriginalOutputString = morsel.OutputString
  instancemethod = type(Morsel.OutputString)
  morsel.OriginalOutputString = OriginalOutputString
  morsel.OutputString = instancemethod(httpOnlyAwareMorselOutputString, morsel,
      Morsel)

  return response

def XFrameOptionsTest(request):
  response = HttpResponse()
  response['X-FRAME-OPTIONS'] = 'DENY'
  response.write('<html><meta http-equiv="X-Frame-Options" content="deny"><body>LOADED')
  response.write("<script>top.xframe_options_test_fail=true;</script></body></html>")
  return response

def XContentTypeOptionsTest(request):
  response = HttpResponse()
  if 'nosniff' in request.GET:
    response['X-Content-Type-Options'] = 'nosniff'
  response['Content-Type'] = 'text/plain'
  if 'html' in request.GET:
    response.write('<html><script>top.x_content_type_options_test_fail=true;</script></html>')
  elif 'script' in request.GET:
    response.write('top.x_content_type_options_test_fail=true;')
  return response

def OriginHeaderTest(request):
  response = HttpResponse()
  if 'HTTP_ORIGIN' in request.META:
    response.write('<html>PASS</html>')
  else:
    response.write('<html>FAIL</html>')
  return response

def SetSts(request):
  if request.is_secure():
    response = HttpResponsePermanentRedirect('http://ua-profiler.appspot.com/security/test/test-sts')
    response['Strict-Transport-Security'] = 'max-age=5'
    return response

def TestSts(request):
  if request.is_secure():
    return HttpResponsePermanentRedirect('http://www.browserscope.org/security/static/sts-pass.html')
  else:
    return HttpResponsePermanentRedirect('http://www.browserscope.org/security/static/sts-fail.html')

def XContentSecurityPolicyTest(request):
  response = HttpResponse()
  response['X-Content-Security-Policy']="allow 'self'"
  response.write('''
  <html>
  <body>
  <!-- the Eval inside xcsp.js should not work -->
  <script src='../static/xcsp.js'></script>
  <div id="csp">PASS</div>
  <!-- The following inline script should not work -->
  <script>
  document.getElementById('csp').firstChild.nodeValue='FAIL'
  </script>
  </body>
  </html>
		  ''');
  return response;



def ReflectedXSSVictim(request):  
  attack_str = ""
  expected_attack = "<script>script_ran = true</script>"
  
  attack = request.GET.get("q")
  attack_part = ""
  if attack:
    attack_part = attack[0:len(expected_attack)]
    if attack_part == expected_attack:
      attack_str = attack_part
  
  html = """<html>
	<body>
	<script src='../static/config.js'></script>
	<!-- XSS filter should stop the following line from running -->
	%s
	<script type='text/javascript'>
	var success = !window.script_ran;
	document.write(\"<iframe src='\" + SAME_ORIGIN_BASE_URL + \"xss-filter-test-done.html?\" + success + \"'></iframe>\");
	</script>
	</body>
	</html>""" % attack_str
  return HttpResponse(html);

