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

from base import custom_filters
from categories import test_set_base

import settings

MAX_KEY_COUNT = 200
MAX_KEY_LENGTH = 200
# This value turns out to be key for aliasing, meaning we need to be
# sure that aliased test sets use it when defining their tests.
MAX_VALUE = 1000000000000

class KeyTooLong(Exception):
  """Indicates that one of the keys is too damn long."""
  pass


class KeyTooMany(Exception):
  """Indicates that there are too many keys to deal with."""
  pass


class User(db.Model):
  email = db.StringProperty()
  created = db.DateTimeProperty(auto_now_add=True)
  modified = db.DateTimeProperty(auto_now=True)


class TestSet(test_set_base.TestSet):
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
    #logging.info('GetTestScoreAndDisplayValue, %s, %s' % (test_key, raw_scores))
    score = 0
    raw_score = raw_scores.get(test_key, None)
    if raw_score is None:
      raw_score = ''

    if raw_score != '':
      test = Test.get_test_from_category(self.category)
      score = test.get_score_from_display(test_key, raw_score)

    #if test.is_boolean_test_key(test_key):
    #  if score == 1:
    #    score = 'yes'
    #  else:
    #    score = 'no'

    return score, raw_score

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
    # Right now this is only implemented as a boolean scorer.
    #logging.info('GetRowScoreAndDisplayValue %s' % results)
    total_tests = 0
    total_score = 0
    for test in self.VisibleTests():
      if results[test.key]['raw_score'] is not None:
        total_tests += 1
        total_score += results[test.key]['raw_score']
    if total_tests:
      score = int(round(100.0 * total_score / total_tests))
      display = '%s/%s' % (total_score, total_tests)
    else:
      score = 0
      display = ''
    return score, display

  def ParseResults(self, results_str, ignore_key_errors=False):
    test_scores = [x.split('=') for x in str(results_str).split(',')]
    try:
      for test_score in test_scores:
        score = int(test_score[1])
        if score > MAX_VALUE:
          raise test_set_base.ParseResultsValueError
    except:
      raise test_set_base.ParseResultsValueError
    return test_set_base.TestSet.ParseResults(self, results_str,
                                              ignore_key_errors=False)


# This reference model exists for storing values about the tests, like min/max.
class TestMeta(db.Expando):
  created = db.DateTimeProperty(auto_now_add=True)
  modified = db.DateTimeProperty(auto_now=True)
  test = db.ReferenceProperty()

  def get_memcache_keyname(self, test):
    return TestMeta.get_memcache_keyname_static(test)

  def add_memcache(self, test):
    memcache_keyname = self.get_memcache_keyname(test)
    memcache.delete(memcache_keyname)
    memcache.add(memcache_keyname, self,
                 settings.STATS_USERTEST_TIMEOUT)

  def save_memcache(self, test):
    self.save()
    self.add_memcache(test)

  @staticmethod
  def get_mem_by_test(test):
    """Gets the TestMeta from memcache and/or puts it in there."""
    memcache_keyname = TestMeta.get_memcache_keyname_static(test)
    meta = memcache.get(memcache_keyname)
    if not meta:
      meta = test.meta
    if not meta:
      meta = TestMeta(test=test)
      meta.save()
    else:
      meta.add_memcache(test)
    return meta

  @staticmethod
  def get_memcache_keyname_static(test):
    return '%s_meta' % Test.get_memcache_keyname_static(test.key())


def ValidateTestKeys(test_keys):
  if len(test_keys) > MAX_KEY_COUNT:
    raise KeyTooMany()
  for test_key in test_keys:
    if len(test_key) > MAX_KEY_LENGTH:
      raise KeyTooLong()


class Test(db.Model):
  user = db.Reference(User)
  name = db.StringProperty(required=True)
  test_keys = db.StringListProperty()
  url = db.LinkProperty(required=True)
  hosted = db.BooleanProperty(required=True, default=False)
  description = db.TextProperty()
  sandboxid = db.StringProperty()
  meta = db.ReferenceProperty(TestMeta)
  beacon_count = db.IntegerProperty(indexed=True, default=0)
  created = db.DateTimeProperty(auto_now_add=True)
  modified = db.DateTimeProperty(auto_now=True)

  def get_base_url(self):
    o = urlparse(self.url)
    base_url = '%s://%s/' % (o.scheme, o.netloc)
    return base_url

  def get_memcache_keyname(self):
    return Test.get_memcache_keyname_static(self.key())

  def add_memcache(self):
    self.delete_memcache()
    memcache.add(self.get_memcache_keyname(), self,
                 settings.STATS_USERTEST_TIMEOUT)

  def save_memcache(self):
    self.save()
    self.add_memcache()

  def delete_memcache(self):
    memcache.delete(self.get_memcache_keyname())

  def get_test_set(self):
    return self.get_test_set_from_test_keys(
        self.test_keys[0:MAX_KEY_COUNT])

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

  def is_boolean_test_key(self, test_key):
    meta = TestMeta.get_mem_by_test(self)
    test_min_value = getattr(meta, '%s_min_value' % test_key)
    test_max_value = getattr(meta, '%s_max_value' % test_key)
    return test_min_value == 0 and test_max_value == 1

  def get_score_from_display(self, test_key, display):
    """Converts a displayed number value into a 1-100 score."""
    meta = TestMeta.get_mem_by_test(self)
    #logging.info('get_score_from_display meta:%s' % meta)
    if not hasattr(meta, '%s_min_value' % test_key):
      value_on_100_scale = 100  # Default to green if no min yet.
    else:
      test_min_value = getattr(meta, '%s_min_value' % test_key)
      test_max_value = getattr(meta, '%s_max_value' % test_key)
      #logging.info('min: %s, max: %s' % (test_min_value, test_max_value))
      numerator = int(display) - test_min_value
      divisor = test_max_value - test_min_value
      if numerator < 1 or divisor < 1:
        value_on_100_scale = 1  # Make it red
      else:
        value_on_100_scale = int((float(numerator)/float(divisor)) * 100)
    #logging.info('USER TEST get_score_from_display %s: %s, %s, %s, %s = %s' %
    #             (display, test_min_value, test_max_value, numerator, divisor,
    #              value_on_100_scale))
    return value_on_100_scale

  @staticmethod
  def get_prefix():
   return 'usertest'

  @staticmethod
  def get_mem(key):
    memcache_keyname = Test.get_memcache_keyname_static(key)
    is_in_memcache = True
    test = memcache.get(memcache_keyname)
    if not test:
      test = Test.get(key)
      is_in_memcache = False
    if not test:
      return None
    if is_in_memcache == False:
      test.add_memcache()
    return test

  @staticmethod
  def is_user_test_category(category):
    if re.match(Test.get_prefix(), category):
      return True
    else:
      return False

  @staticmethod
  def get_memcache_keyname_static(key):
    return '%s_%s' % (Test.get_prefix(), key)

  @staticmethod
  def get_key_from_category(category):
    if re.match(Test.get_prefix(), category):
      category_prefix = '%s_' % Test.get_prefix()
      if category_prefix not in category:
        return None
      return category.replace(category_prefix, '')
    else:
      return None

  @staticmethod
  def get_test_from_category(category):
    key = Test.get_key_from_category(category)
    if key:
      return Test.get_mem(key)
    else:
      return None

  @staticmethod
  def get_test_set_from_category(category):
    test = Test.get_test_from_category(category)
    if test:
      return test.get_test_set()
    else:
      return None

  @staticmethod
  def get_test_set_from_data(content):
    """Extracts the test_set out of content."""
    match = re.search(r'.+var _bTestSet\s?=\s?(\[[^\]]+\]);', content)
    if match is None:
      return None
    return match

  @staticmethod
  def get_test_set_from_results_str(category, results_str):
    """Creates a runtime version of a browserscope TestSet by parsing strings.
    Args:
      category: A string that looks like 'usertest_sad7dsa987sa9dsa7dsa9'.
      results_str: A string that looks like 'test_1=0,test_2=1'.

    Returns:
      A models.user_test.TestSet instance.

    Raises:
      KeyTooLong: When any of the key names is longer than MAX_KEY_LENGTH.
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
    ValidateTestKeys(test_keys)

    # If it's test run #1, save what we've got for test keys and swap
    # memcache.
    if not test.test_keys:
      test.test_keys = test_keys
      test.save_memcache()
    else:
      deferred.defer(update_test_keys, key, test_keys)

    # Regardless we'll defer updating the TestMeta reference.
    deferred.defer(update_test_meta, key, test_scores)

    test_set = test.get_test_set_from_test_keys(test_keys)
    return test_set


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
    try:
      test.save_memcache()
    except db.BadValueError:
      logging.info('db.BadValueError - bail.')


def update_test_meta(key, test_scores):
  """Deferred task handler for ensuring Test.test_keys stays in sync.
  Args:
    key: Test key.
    test_scores: A tuple of string ('test_key', 'score') from a recent beacon.
  """
  dirty = False
  test = Test.get_mem(key)
  meta = TestMeta.get_mem_by_test(test)

  # Just in case?, we want to make sure our test has a meta reference.
  if not meta:
    meta = TestMeta()
    meta.save() # here we don't want to save_memcache yet
    test.meta = meta
    test.save_memcache()

  if meta.test is None:
    meta.test = test
    dirty = True

  #logging.info('update_test_meta test_scores: %s' % test_scores)
  try:
    for test_key, test_value in test_scores:
      min_key = '%s_min_value' % test_key
      max_key = '%s_max_value' % test_key

      # Convert test_value into an int from a string.
      try:
        test_value = int(test_value)
      except ValueError:
        logging.info('ValueError for key:%s, val:%s' % (test_key, test_value))
        continue

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
  except ValueError:
    logging.info('ValueError trying to unpack malformed test_scores, bailing.')

  if dirty:
    try:
      meta.save_memcache(test)
    except db.BadPropertyError:
      logging.info('db.BadPropertyError - bail.')
    except OverflowError:
      logging.info('OverflowError - bail.')

