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

"""User models, where user means logged in Browserscope users."""

import re
import logging
import sys
import urllib2
from urlparse import urlparse

from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext import deferred

from categories import test_set_base


class User(db.Model):
  email = db.StringProperty()
  created = db.DateTimeProperty(auto_now_add=True)
  modified = db.DateTimeProperty(auto_now=True)


class TestSet(test_set_base.TestSet):
  def GetTestScoreAndDisplayValue(self, test_key, raw_scores):
    raw_score = raw_scores.get(test_key, 0)
    if raw_score is None:
      raw_score = ''
    else:
      raw_score = str(raw_score)
    return 0, raw_score

  def GetRowScoreAndDisplayValue(self, results):
    return 0, ''


def update_test_keys(key, test_keys):
  test = Test.get_mem(key)
  dirty = False
  for test_key in test_keys:
    if not test_key in test.test_keys:
      test.test_keys.append(test_key)
      dirty = True
  if dirty:
    test.save()
    test.add_memcache()

class Test(db.Model):
  user = db.Reference(User)
  name = db.StringProperty(required=True)
  test_keys = db.StringListProperty()
  url = db.LinkProperty(required=True)
  hosted = db.BooleanProperty(required=True, default=False)
  description = db.TextProperty()
  created = db.DateTimeProperty(auto_now_add=True)
  modified = db.DateTimeProperty(auto_now=True)

  def get_base_url(self):
    o = urlparse(self.url)
    base_url = '%s://%s/' % (o.scheme, o.netloc)
    return base_url

  # def get_mirrored_content(self):
  #   mirrored_content = mirror.MirroredContent.get_by_key_name(
  #       self.get_memcache_keyname())
  #   return mirrored_content

  def get_memcache_keyname(self):
    return Test.get_memcache_keyname_static(self.key())

  def add_memcache(self):
    self.delete_memcache()
    memcache.add(self.get_memcache_keyname(), self, 360)

  def delete_memcache(self):
    memcache.delete(self.get_memcache_keyname())

  def get_test_set_from_test_keys(self, test_keys):
    test_set_tests = []
    max_value = 10000
    for test_key in test_keys:
      test = test_set_base.TestBase(key=test_key,
                                    name=test_key,
                                    url='',
                                    doc='',
                                    min_value=0,
                                    max_value=max_value)
      test_set_tests.append(test)
    test_set = TestSet(category=self.get_memcache_keyname(),
                       category_name=self.name,
                       tests=test_set_tests,
                       test_page='%s' % self.url)
    return test_set

  @staticmethod
  def get_mem(key):
    memcache_keyname = Test.get_memcache_keyname_static(key)
    test = memcache.get(memcache_keyname)
    if not test:
      test = Test.get(key)
    if not test:
      return None
    test.add_memcache()
    return test

  @staticmethod
  def get_prefix():
   return 'usertest'

  @staticmethod
  def get_memcache_keyname_static(key):
    return '%s_%s' % (Test.get_prefix(), key)

  @staticmethod
  def get_test_set_from_results_str(category, results_str):
    category_prefix = '%s_' % Test.get_prefix()
    if category_prefix not in category:
      return None
    [category, key] = category.split('_')
    if category != Test.get_prefix():
      return None
    test = Test.get_mem(key)
    if not test:
      return None

    test_scores = [x.split('=') for x in str(results_str).split(',')]
    test_keys = sorted([x[0] for x in test_scores])
    deferred.defer(update_test_keys, key, test_keys, _countdown=60)
    test_set = test.get_test_set_from_test_keys(test_keys)
    return test_set

  @staticmethod
  def get_test_set_from_category(category):
    if re.match(Test.get_prefix(), category):
      [category, key] = category.split('_')
      if category != Test.get_prefix():
        return None
      test = Test.get_mem(key)
      return test.get_test_set_from_test_keys(test.test_keys)
    else:
      return None

  @staticmethod
  def get_test_set_from_data(content):
    """Extracts the test_set out of content."""
    match = re.search(r'.+var _bTestSet\s?=\s?(\[[^\]]+\]);', content)
    logging.info('match: %s' % match )
    if match is None:
      return None
    return match