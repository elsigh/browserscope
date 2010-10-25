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

# This value turns out to be key for aliasing, meaning we need to be
# sure that aliased test sets use it when defining their tests.
MAX_VALUE = 10000


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


# This reference model exists for storing values about the tests, like min/max.
class TestMeta(db.Expando):
  created = db.DateTimeProperty(auto_now_add=True)
  modified = db.DateTimeProperty(auto_now=True)
  test = db.ReferenceProperty()


class Test(db.Model):
  user = db.Reference(User)
  name = db.StringProperty(required=True)
  test_keys = db.StringListProperty()
  url = db.LinkProperty(required=True)
  hosted = db.BooleanProperty(required=True, default=False)
  description = db.TextProperty()
  sandboxid = db.StringProperty()
  meta = db.ReferenceProperty(TestMeta)
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

  def get_test_set_tests_from_test_keys(self, test_keys):
    test_set_tests = []
    for test_key in test_keys:
      test = test_set_base.TestBase(key=test_key,
                                    name=test_key,
                                    url='',
                                    doc='',
                                    min_value=0,
                                    max_value=MAX_VALUE)
      test_set_tests.append(test)
    return test_set_tests

  def get_test_set_from_test_keys(self, test_keys):
    test_set_tests = self.get_test_set_tests_from_test_keys(test_keys)
    test_set = TestSet(category=self.get_memcache_keyname(),
                       category_name=self.name,
                       summary_doc='',
                       tests=test_set_tests,
                       test_page='%s' % self.url)
    test_set.sandboxid = self.sandboxid
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
    """Creates a runtime version of a browserscope TestSet by parsing strings.
    Args:
      category: A string that looks like 'usertest_sad7dsa987sa9dsa7dsa9'.
      results_str: A string that looks like 'test_1=0,test_2=1'.

    Returns:
      A models.user_test.TestSet instance.
    """
    category_prefix = '%s_' % Test.get_prefix()
    if category_prefix not in category:
      return None
    key = category.replace(category_prefix, '')
    test = Test.get_mem(key)
    if not test:
      return None

    test_scores = [x.split('=') for x in str(results_str).split(',')]
    test_keys = sorted([x[0] for x in test_scores])

    # If it's test run #1, save what we've got for test keys and swap
    # memcache.
    if not test.test_keys:
      test.test_keys = test_keys
      test.save()
      test.add_memcache()
    else:
      deferred.defer(update_test_keys, key, test_keys)

    # Regardless we'll defer updating the TestMeta reference.
    deferred.defer(update_test_meta, key, test_scores)

    test_set = test.get_test_set_from_test_keys(test_keys)
    return test_set

  @staticmethod
  def is_user_test_category(category):
    if re.match(Test.get_prefix(), category):
      return True
    else:
      return False

  @staticmethod
  def get_test_set_from_category(category):
    if re.match(Test.get_prefix(), category):
      category_prefix = '%s_' % Test.get_prefix()
      if category_prefix not in category:
        return None
      key = category.replace(category_prefix, '')
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


def update_test_keys(key, test_keys):
  """Deferred task handler for ensuring TestMeta stays in sync.
  Args:
    key: Test key.
    test_keys: A list of strings, the test_key values for each test.
  """
  test = Test.get_mem(key)
  dirty = False
  for test_key in test_keys:
    if not test_key in test.test_keys:
      test.test_keys.append(test_key)
      dirty = True
  if dirty:
    test.save()
    test.add_memcache()


def update_test_meta(key, test_scores):
  """Deferred task handler for ensuring Test.test_keys stays in sync.
  Args:
    key: Test key.
    test_scores: A tuple of string ('test_key', 'score') from a recent beacon.
  """
  dirty = False
  test = Test.get_mem(key)
  meta = test.meta

  # Just in case?, we want to make sure our test has a meta reference.
  if not meta:
    meta = TestMeta()
    meta.save()
    test.meta = meta
    test.save()
    test.add_memcache()

  if meta.test is None:
    meta.test = test
    dirty = True

  for test_key, test_value in test_scores:
    min_key = '%s_min_value' % test_key
    max_key = '%s_max_value' % test_key

    # Convert test_value into an int from a string.
    test_value = int(test_value)

    if not hasattr(meta, min_key):
      setattr(meta, min_key, test_value)
      setattr(meta, max_key, test_value)
      dirty = True
    else:
      if test_value < getattr(meta, min_key):
        setattr(meta, min_key, test_value)
        dirty = True
      elif test_value > getattr(meta, max_key):
        setattr(meta, max_key, test_value)
        dirty = True

      #logging.info('finally %s %s: %s, %s: %s' %
      #             (test_key, getattr(meta, min_key), min_key,
      #              getattr(meta, max_key), max_key))

  if dirty:
    meta.save()

