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


from categories import all_test_sets
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
    and <a href="http://www.google.com/profiles/meacer">Mustafa Acer</a>."""
  return util.About(request, CATEGORY, overview=overview)


def Test(request):
  response = util.Render(request, 'templates/test.html', params={},
                         category=CATEGORY)
  response.set_cookie('regularTestCookie', '1', expires=None, httponly=False, path='/security/')
  response.set_cookie('httpOnlyTestCookie', '1', expires=None, httponly=True, path='/security/')
  return response

def XFrameOptionsTest(request):
  response = HttpResponse()
  response['X-FRAME-OPTIONS'] = 'DENY'
  response.write('<html><meta http-equiv="X-Frame-Options" content="deny"><body>LOADED')
  response.write("<script>top.xframe_options_test_fail=true;</script></body></html>")
  return response

def XContentTypeOptionsTest(request):
  response = HttpResponse()
  response.write('<html>LOADED <script>top.xcontenttype_options_test_fail=true;</script></html>')
  response['X-CONTENT-TYPE-OPTIONS'] = 'nosniff'
  response['Content-type'] = 'text'
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
