#!/usr/bin/python2.5
#
# Copyright 2009 Palm Inc.
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

"""Handlers for Cookies Tests.

Example beacon request:
  http://localhost:8080/beacon?category=network&results=latency=123,hostconn=6,
     maxconn=29,parscript=0,parsheet=1,parcssjs=0,cacheexp=1,cacheredir=0,
     cacheresredir=0,prefetch=1,gzip=1,du=1
"""

__author__ = 'etlovett@cs.stanford.edu (Eric Lovett)'


from categories import all_test_sets
from base import decorators
from base import util

from django import http
from datetime import datetime, timedelta
from math import floor, ceil
import settings


CATEGORY = 'cookies'


def About(request):
  """About page."""
  return util.About(request, 'cookies')


def ClearCookies(request):
  num_cookies_found = len(request.COOKIES)
  
  cookies_to_set = {}
  num_system_cookies = 0
  name_chars_found = 0
  value_chars_found = 0
  for name, value in request.COOKIES.items():
    if name not in settings.SYSTEM_COOKIES:
      cookies_to_set[name] = value
      
      # assume that for size, it is safe to just use the data from the
      # last non-system one, since there should only be one such cookie
      name_chars_found = len(name)
      value_chars_found = len(value)
    else:
      num_system_cookies += 1
  
  redirect_to = request.GET.get('redirect_to')
  if '?' in redirect_to:
    redirect_to = "%s&" % request.GET.get('redirect_to')
  else:
    redirect_to = "%s?" % request.GET.get('redirect_to')
  
  if not 'reset' in request.GET:
    redirect_to = "%snum_cookies_found=%d&num_system_cookies=%d&name_chars_found=%d&value_chars_found=%d" \
                  % (redirect_to, num_cookies_found, num_system_cookies, \
                    name_chars_found, value_chars_found)
  
  params = {
    'page_title': 'Clearing Cookies',
    'redirect_to': redirect_to,
  }
  response = util.Render(request, 'templates/tests/clear-cookies.html', params, 
                        CATEGORY)
  
  # add the cookies to the response, expired, so that they'll be cleared
  expires = datetime.strftime(datetime.utcnow() + timedelta(hours=-5), 
                                      "%a, %d-%b-%Y %H:%M:%S GMT")
  
  for name, value in cookies_to_set.items():
    response.set_cookie(name, value, expires=expires)
  
  return response


EXPIRESCOOKIE1 = 'ExpiresTestCookie1'
EXPIRESCOOKIE2 = 'ExpiresTestCookie2'
EXPIRESCOOKIE3 = 'ExpiresTestCookie3'

def Expires(request):
  """Cookie Expires Test (1 of 2)"""

  params = {
    'page_title': 'Cookie Expires Test',
  }
  response = util.Render(request, 'templates/tests/expires.html', params, 
                         CATEGORY)
  
  expiresInPast = datetime.strftime(datetime.utcnow() + timedelta(hours=-5), 
                                    "%a, %d-%b-%Y %H:%M:%S GMT")
  expiresInFuture = datetime.strftime(datetime.utcnow() + timedelta(hours=5), 
                                      "%a, %d-%b-%Y %H:%M:%S GMT")
  
  # test one each of: cookie with past expires date, session cookie, cookie 
  # with future expires date
  response.set_cookie(EXPIRESCOOKIE1, value="Cookie", expires=expiresInPast)
  response.set_cookie(EXPIRESCOOKIE2, value="Cookie", expires=None)
  response.set_cookie(EXPIRESCOOKIE3, value="Cookie", expires=expiresInFuture)
  return response


def Expires2(request):
  """Cookie Expires Test (2 of 2)"""

  # number 1 should have been deleted, numbers 2 and 3 shouldn't have been
  if None == request.COOKIES.get(EXPIRESCOOKIE1) \
    and not None == request.COOKIES.get(EXPIRESCOOKIE2) \
    and not None == request.COOKIES.get(EXPIRESCOOKIE3):
    
    cookie_deleted = 1
  else:
    cookie_deleted = 0

  params = {
    'page_title': 'Cookie Expires Test',
    'cookie_deleted': cookie_deleted,
  }
  response = util.Render(request, 'templates/tests/expires2.html', params, 
                         CATEGORY)
  # now delete number 2 to clear the way for future tests
  expires = datetime.strftime(datetime.utcnow() + timedelta(hours=-1), 
                              "%a, %d-%b-%Y %H:%M:%S GMT")
  response.set_cookie(EXPIRESCOOKIE2, value="", expires=expires)
  return response


def MaxPerHost(request):
  """Max Cookies per Host Test"""

  # constants for this test
  cookie_inc_factor = 2
  cookie_name_prefix = "TestCookie"
  cookie_value_prefix = "TestCookieValue"
  expires = datetime.strftime(datetime.utcnow() + timedelta(hours=24), 
                                      "%a, %d-%b-%Y %H:%M:%S GMT")
  
  # get the parameters used last time around
  last_attempt = int(request.GET.get('last_attempt', 0))
  max_working = int(request.GET.get('max_working', 0))
  min_failing = int(request.GET.get('min_failing', -1))
  # these two set by ClearCookies
  num_cookies_found = int(request.GET.get('num_cookies_found', -1))
  num_system_cookies = int(request.GET.get('num_system_cookies', 0))
  
  if max_working + 1 == min_failing:
    # then we know how many cookies we can receive from the browser, so stop
    params = {
      'page_title': 'Max Cookies per Host Test',
      'max_cookies': max_working
    }
    return util.Render(request, 'templates/tests/max-per-host2.html', params, 
                      CATEGORY)
  else:
    # we need to send a different number of cookies
    
    # if we got a new num_cookies_found, then update max_working 
    # and last_attempt
    if not -1 == num_cookies_found:
      if num_cookies_found > max_working:
        # then we can store more than we knew before
        max_working = num_cookies_found
      if num_cookies_found < last_attempt:
        # then we can't store as many as we thought
        min_failing = last_attempt
    
    # figure out how many cookies to try
    if -1 == min_failing:
      if 0 == max_working:
        new_cookie_count = 1
      else:
        new_cookie_count = max_working * cookie_inc_factor
    else:
      new_cookie_count = int(floor((max_working + min_failing) / 2))
    
    query = http.QueryDict('').copy()
    redirect = "max-per-host?max_working=%d&min_failing=%d&last_attempt=%d" \
                  % (max_working, min_failing, new_cookie_count)
    query['redirect_to'] = redirect
    
    # set up the response
    params = {
      'page_title': 'Max Cookies per Host Test',
      'query_string': query.urlencode(),
      'max_working': str(max_working),
      'min_failing': str(min_failing),
      'last_attempt': str(last_attempt),
      'new_cookie_count': str(new_cookie_count)
    }
    response = util.Render(request, 'templates/tests/max-per-host.html', params, 
                     CATEGORY)
    
    # add the cookies to the response
    for i in range(new_cookie_count - num_system_cookies):
      name = cookie_name_prefix + str(i)
      value = cookie_value_prefix + str(i)
      response.set_cookie(name, value, expires=expires)
    
    return response


NAME_TEST_TYPE = 'Name'
VALUE_TEST_TYPE = 'Value'
TOTAL_TEST_TYPE = 'Total'

def MaxNameSize(request):
  """Max Single Cookie Name Size Test"""
  
  def get_num_test_chars(name_chars_found, value_chars_found):
    return name_chars_found
  
  def get_cookie_fields(length, ch):
    return (''.ljust(length, ch), ch)
  
  return MaxSizeTest(request, NAME_TEST_TYPE, VALUE_TEST_TYPE, 'inline',
                    get_num_test_chars, get_cookie_fields)


def MaxValueSize(request):
  """Max Single Cookie Value Size Test"""
  
  def get_num_test_chars(name_chars_found, value_chars_found):
    return value_chars_found
  
  def get_cookie_fields(length, ch):
    return (ch, ''.ljust(length, ch))
  
  return MaxSizeTest(request, VALUE_TEST_TYPE, NAME_TEST_TYPE, 'inline',
                    get_num_test_chars, get_cookie_fields)


def MaxTotalSize(request):
  """Max Single Cookie Total Size Test"""
  
  def get_num_test_chars(name_chars_found, value_chars_found):
    return name_chars_found + value_chars_found
  
  def get_cookie_fields(length, ch):
    # make sure the name is longer, for the length=1 case
    name_len = int(ceil(float(length) / 2.0))
    value_len = length - name_len
    return (''.ljust(name_len, ch), ''.ljust(value_len, ch))
  
  return MaxSizeTest(request, TOTAL_TEST_TYPE, '', 'none',
                    get_num_test_chars, get_cookie_fields)


def MaxSizeTest(request, test_type, test_type_other, display_other, 
              get_num_test_chars, get_cookie_fields):
  """Helper method for max name size, max value size, and max total size 
tests"""
  
  # constants for this test
  cookie_char = 'a'
  expires = datetime.strftime(datetime.utcnow() + timedelta(hours=24), 
                                      "%a, %d-%b-%Y %H:%M:%S GMT")
  
  # get the parameters used last time around
  last_attempt = int(request.GET.get('last_attempt', 0))
  max_working = int(request.GET.get('max_working', 0))
  min_failing = int(request.GET.get('min_failing', -1))
  # these two set by ClearCookies
  name_chars_found = int(request.GET.get('name_chars_found', -1))
  value_chars_found = int(request.GET.get('value_chars_found', -1))
  
  if max_working + 1 == min_failing:
    # then we know how large a cookie name we can receive from the browser, 
    # so stop
    params = {
      'page_title': 'Max Cookie ' + test_type + ' Size Test',
      'test_type': test_type,
      'test_type_other': test_type_other,
      'display_other': display_other,
      'max_test_chars': max_working,
      'other_chars': len(cookie_char)
    }
    return util.Render(request, 'templates/tests/max-size2.html', params, 
                      CATEGORY)
  else:
    # we need to send a different size of cookie name/value
    
    # if we got a new name/value_chars_found, then update max_working 
    # and last_attempt
    if not -1 == name_chars_found and not -1 == value_chars_found:
      num_test_chars = get_num_test_chars(name_chars_found, value_chars_found)
      
      if num_test_chars > max_working:
        # then we can store more than we knew before
        max_working = num_test_chars
      if num_test_chars < last_attempt:
        # then we can't store as many as we thought
        min_failing = last_attempt
    
    # figure out what size to try
    if -1 == min_failing:
      if 0 == max_working:
        this_attempt = 1
      else:
        this_attempt = max_working * 2
    else:
      this_attempt = (max_working + min_failing) / 2

    
    # set up the response
    query = http.QueryDict('').copy()
    redirect = "max-%s-size?max_working=%d&min_failing=%d&last_attempt=%d" \
                  % (test_type.lower(), max_working, min_failing, this_attempt)
    query['redirect_to'] = redirect
    params = {
      'page_title': 'Max Cookie ' + test_type + ' Size Test',
      'test_type': test_type,
      'query_string': query.urlencode(),
      'max_working': str(max_working),
      'min_failing': str(min_failing),
      'last_attempt': str(last_attempt),
      'this_attempt': str(this_attempt)
    }
    response = util.Render(request, 'templates/tests/max-size.html', params, 
                     CATEGORY)
    
    # add the cookie to the response
    (cookie_name, cookie_value) = get_cookie_fields(this_attempt, cookie_char)
    response.set_cookie(cookie_name, cookie_value, expires=expires)
    
    return response
