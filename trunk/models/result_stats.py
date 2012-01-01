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

"""Shared models."""

import logging
import sys

from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.runtime import DeadlineExceededError

from categories import all_test_sets
from models.user_agent import UserAgent

BROWSER_NAV = (
  # version_level, label
  ('top', 'Top Browsers'),
  ('top-d', 'Top Desktop'),
  ('top-m', 'Top Mobile'),
  ('top-d-e', 'Top Desktop Edge'),
  ('top-all', 'Top Browsers(all)'),
  ('0', 'Browser Families'),
  ('1', 'Major Versions'),
  ('2', 'Minor Versions'),
  ('3', 'All Versions')
)

TOP_DESKTOP_BROWSERS = (
  'Chrome 16',
  'Firefox 8', 'Firefox 9',
  'IE 8', 'IE 9',
  'Opera 11.6',
  'RockMelt 0.9',
  'Safari 5.1'
)

TOP_DESKTOP_EDGE_BROWSERS = (
  'Chrome 17', 'Chrome 18',
  'Firefox Beta 10',
  'IE Platform Preview 10', 'IE 10',
  'Opera 12',
  'Safari 5.1.3'
)

TOP_MOBILE_BROWSERS = (
  'Android 2.3', 'Android 3',
  'Blackberry 7',
  'IE Mobile 7', 'IE Mobile 9',
  'iPhone 3.1', 'iPhone 4',
  'Nokia 950',
  'Opera Mobile 11',
  'Palm webOS 2.1', 'Palm webOS 2.2'
)

TOP_BROWSERS = TOP_DESKTOP_BROWSERS + TOP_DESKTOP_EDGE_BROWSERS + TOP_MOBILE_BROWSERS

class CategoryBrowserManager(db.Model):
  """Track the browsers that belong in each category/version level."""

  MEMCACHE_NAMESPACE = 'category_level_browsers'

  browsers = db.StringListProperty(default=[], indexed=False)

  @classmethod
  def AddUserAgent(cls, category, user_agent):
    """Adds a user agent's browser strings to version-level groups.

    AddUserAgent assumes that it does not receive overlapping calls.
    - It should only get called by the update-user-groups task queue.

    Adds a browser for every version level.
    If a level does not have a string, then use the one from the previous level.
    For example, "Safari 4.3" would increment the following:
        level  browser
            0  Safari
            1  Safari 4
            2  Safari 4.3
            3  Safari 4.3

    Args:
      category: a category string like 'network' or 'reflow'.
      user_agent: a UserAgent instance.
    """
    key_names = [cls.KeyName(category, v) for v in range(4)]
    version_levels = range(4)
    if category in [t.category for t in all_test_sets.GetVisibleTestSets()]:
      key_names.extend([cls.KeyName('summary', v) for v in range(4)])
      version_levels.extend(range(4))
    level_browsers = memcache.get_multi(key_names,
                                        namespace=cls.MEMCACHE_NAMESPACE)
    browser_key_names = []
    ua_browsers = user_agent.get_string_list()
    max_ua_browsers_index = len(ua_browsers) - 1
    for version_level, key_name in zip(version_levels, key_names):
      browser = ua_browsers[min(max_ua_browsers_index, version_level)]
      if browser not in level_browsers.get(key_name, []):
        browser_key_names.append((browser, key_name))
    managers = cls.get_by_key_name([x[1] for x in browser_key_names])

    updated_managers = []
    memcache_mapping = {}
    for (browser, key_name), manager in zip(browser_key_names, managers):
      if manager is None:
        manager = cls.get_or_insert(key_name)
      if browser not in manager.browsers:
        cls.InsortBrowser(manager.browsers, browser)
        updated_managers.append(manager)
        memcache_mapping[key_name] = manager.browsers
    if updated_managers:
      db.put(updated_managers)
      memcache.set_multi(memcache_mapping, namespace=cls.MEMCACHE_NAMESPACE)

  @classmethod
  def GetBrowsers(cls, category, version_level):
    """Get all the browsers for a version level.

    Args:
      category: a category string like 'network' or 'reflow'.
      version_level: 'top', 0 (family), 1 (major), 2 (minor), 3 (3rd)
    Returns:
      ['Firefox 3.1', 'Safari 4.0', 'Safari 4.5', ...]
    """
    if version_level == 'top':
      browsers = list(TOP_BROWSERS)
    elif version_level == 'top-d':
      browsers = list(TOP_DESKTOP_BROWSERS)
    elif version_level == 'top-m':
      browsers = list(TOP_MOBILE_BROWSERS)
    elif version_level == 'top-d-e':
      browsers = list(TOP_DESKTOP_EDGE_BROWSERS)
    else:
      # If this is an aliased UserTest (like HTML5), use its key instead.
      test_set = all_test_sets.GetTestSet(category)
      if test_set is not None and test_set.user_test_category is not None:
        category = test_set.user_test_category

      key_name = cls.KeyName(category, version_level)
      browsers = memcache.get(key_name, namespace=cls.MEMCACHE_NAMESPACE)
      if browsers is None:
        manager = cls.get_by_key_name(key_name)
        browsers = manager and manager.browsers or []
        memcache.set(key_name, browsers, namespace=cls.MEMCACHE_NAMESPACE)
    return browsers

  @classmethod
  def GetAllBrowsers(cls, category):
    """Get all the browsers for a category.

    Args:
      category: a category string like 'network' or 'reflow'.
    Returns:
      ('Firefox', 'Firefox 3', 'Firefox 3.1', 'Safari', 'Safari 4', ...)
      # Order is undefined
    """
    all_browsers = set()
    for version_level in range(4):
      all_browsers.update(cls.GetBrowsers(category, version_level))
    return list(all_browsers)

  @classmethod
  def GetFilteredBrowsers(cls, category, filters):
    """Get browsers based on a filter (prefixes for now).

    Args:
      category: a category string like 'network' or 'reflow'.
      filters: a list of filters like 'Firefox*' (prefix) or 'Firefox 3' (exact)
    Returns:
      ('Firefox 3.1', 'Safari 4.0', 'Safari 4.5', ...)
    """
    filtered_browsers = []
    for browser in cls.GetBrowsers(category, version_level=3):
      for filtr in filters:
        if filtr[-1:] == '*':
          if (browser.startswith(filtr[:-1]) and
              (filtr != 'Opera*' or not browser.startswith('Opera Mini'))):
            filtered_browsers.append(browser)
        elif browser == filtr:
          filtered_browsers.append(browser)
    return filtered_browsers

  @classmethod
  def SetBrowsers(cls, category, version_level, browsers):
    cls.SortBrowsers(browsers)
    key_name = cls.KeyName(category, version_level)
    memcache.set(key_name, browsers, namespace=cls.MEMCACHE_NAMESPACE)
    manager = cls.get_or_insert(key_name)
    manager.browsers = browsers
    manager.put()

  @classmethod
  def UpdateSummaryBrowsers(cls, categories):
    for version_level in range(4):
      browsers = set()
      for category in categories:
        browsers.update(cls.GetBrowsers(category, version_level))
      browsers = list(browsers)
      cls.SortBrowsers(browsers)
      cls.SetBrowsers('summary', version_level, browsers)

  @classmethod
  def SortBrowsers(cls, browsers):
    """Sort browser strings in-place.

    Args:
      browsers: a list of strings
          e.g. ['iPhone 3.1', 'Firefox 3.01', 'Safari 4.1']
    """
    browsers.sort(key=cls.BrowserKey)

  @classmethod
  def InsortBrowser(cls, browsers, browser):
    """Insert a browser, in-place, into a sorted list of browsers.

    Args:
      browsers: a list of strings (e.g. ['iPhone 3.1', 'Safari 4.1'])
      browser: a list of strings
    """
    browser_key = cls.BrowserKey(browser)
    low, high = 0, len(browsers)
    while low < high:
      mid = (low + high) / 2
      if browser_key < cls.BrowserKey(browsers[mid]):
        high = mid
      else:
        low = mid + 1
    if not hasattr(browsers, 'insert'):
      logging.fatal('Unexpected browsers list: %s', browsers)
    browsers.insert(low, browser)

  @classmethod
  def BrowserKey(cls, browser):
    VERSION_DIGITS = 8
    MAX_VERSION = 99999999
    family, v1, v2, v3 = UserAgent.parse_pretty(browser.lower())
    extra = None
    if family[-1] == ')':
      family, extra = family.split(' ', 1)
    return (family.lower(),
            cls._BrowserKeyPart(v1),
            cls._BrowserKeyPart(v2),
            cls._BrowserKeyPart(v3),
            extra)

  @classmethod
  def _BrowserKeyPart(cls, v):
    if v is None:
      return ''
    elif v.isdigit():
      digits = int(v or 0) + 1
      nondigits = ' ' * 8
    else:
      nondigit_index = 0
      while v[nondigit_index].isdigit():
        nondigit_index += 1
      digits, nondigits = int(v[:nondigit_index] or 0), v[nondigit_index:]
    return '%.08d %-8s' % (digits, nondigits)


  @classmethod
  def KeyName(cls, category, version_level):
    return '%s_%s' % (category, version_level)

  @classmethod
  def DeleteMemcacheValue(cls, category, version_level):
    key_name = cls.KeyName(category, version_level)
    memcache.delete(key_name, namespace=cls.MEMCACHE_NAMESPACE)


class SummaryStatsManager(db.Model):
  MEMCACHE_NAMESPACE = 'summary_stats'

  #category = db.StringProperty()
  summary_score = db.IntegerProperty(indexed=False)
  summary_display = db.StringProperty(indexed=False)
  total_runs = db.IntegerProperty(indexed=False)

  @classmethod
  def UpdateStats(cls, category, stats):
    """Update the summary stats in memory and the datastore.

    This will only update part of a summary score row.

    Args:
      category: a category string like 'network'
      stats: a dict of browser stats (see CategoryStatsManager.GetStats)
    Returns:
      The summary stats that have been updated by the given stats.
      (Used by GetStats.)
    """
    browsers = [b for b in stats.keys() if b != 'total_runs']
    update_summary_stats = memcache.get_multi(
        browsers, namespace=cls.MEMCACHE_NAMESPACE)
    for browser in browsers:
      ua_summary_stats = update_summary_stats.setdefault(browser, {
          'results': {}})
      ua_summary_stats['results'][category] = {
          'score': stats[browser]['summary_score'],
          'display': stats[browser]['summary_display'],
          'total_runs': stats[browser]['total_runs'],
          }
      if category == 'acid3':
        ua_summary_stats['results']['acid3']['display'] = (
            stats[browser]['results']['score']['display'])
    memcache.set_multi(update_summary_stats, namespace=cls.MEMCACHE_NAMESPACE)
    return update_summary_stats

  @classmethod
  def _FindAndUpdateStats(cls, category, browsers):
    test_set = all_test_sets.GetTestSet(category)
    ua_stats = CategoryStatsManager.GetStats(
        test_set, browsers, [t.key for t in test_set.VisibleTests()])
    return cls.UpdateStats(category, ua_stats)

  @classmethod
  def _AddSummaryOfSummaries(cls, summary_stats):
    """Update summary_stats with row summaries."""
    grand_total_runs = 0
    for browser in summary_stats.keys():
      results = summary_stats[browser]['results']
      categories = results.keys()
      score = int(sum(results[c]['score'] for c in categories)
                  / len(categories))
      display = '%s/100' % score
      total_runs = sum(results[c]['total_runs'] for c in categories)
      grand_total_runs += total_runs
      summary_stats[browser].update({
          'summary_score': score,
          'summary_display': display,
          'total_runs': total_runs,
          })
    summary_stats['total_runs'] = grand_total_runs


  @classmethod
  def GetStats(cls, browsers, categories=None):
    """Return the summary stats for a set of browsers and categories.

    Gets stats out of summary memcache. If needed, re-aggregate them for the
    categories. These data may come from memcache or all the way from the
    datastore.

    Args:
      browsers: a list of browsers to use instead of version level.
      categories: a list of categories like ['security', 'richtext'].
    Returns:
      {
          browser_x: {
              category_y: {
                 'score': score_xy,
                 'display': display_xy,
                 'total_runs': total_runs_xy,
                 }, ...
              }, ...
      }
    """
    summary_stats = memcache.get_multi(
        browsers, namespace=cls.MEMCACHE_NAMESPACE)
    if not categories:
      categories = [t.category for t in all_test_sets.GetVisibleTestSets()]
    # Trim any unwanted stats and find any missing stats.
    missing_stats = {}
    for browser in browsers:
      ua_summary_stats = summary_stats.get(browser, {'results': {}})
      existing_categories = ua_summary_stats['results'].keys()
      for category in existing_categories:
        if category not in categories:
          del ua_summary_stats['results'][category]
      for category in categories:
        if category not in existing_categories:
          missing_stats.setdefault(category, []).append(browser)
    # Load any missing stats
    for category, browsers in missing_stats.items():
      updated_stats = cls._FindAndUpdateStats(category, browsers)
      summary_stats.update(updated_stats)

    cls._AddSummaryOfSummaries(summary_stats)
    return summary_stats

  @classmethod
  def KeyName(cls, category):
    return category


class CategoryStatsManager(object):
  """Manage statistics for a category."""

  MEMCACHE_NAMESPACE_PREFIX = 'category_stats'

  @classmethod
  def GetStats(cls, test_set, browsers, test_keys, use_memcache=True):
    """Get stats table for a given test_set.

    Args:
      test_set: a TestSet instance
      browsers: a list of browsers to use instead of version level
      test_keys: a list of test keys to include in 'results'.
      use_memcache: whether to use memcache or not
    Returns:
      {
          browser: {
              'summary_score': summary_score,
              'summary_display': summary_display,
              'total_runs': total_runs,
              'results': {
                  test_key_1: {
                      'raw_score': raw_score_1,
                      'score': score_1,
                      'display': display_1,
                      'expando': expando_1
                      },
                  test_key_2: {...},
                  },
              },
          ...
          'total_runs': total_runs_for_all_browsers_combined,
      }
    """
    category = test_set.category
    dirty = False
    stats = {}
    if use_memcache:
      memcache_params = cls.MemcacheParams(category)
      stats = memcache.get_multi(browsers, **memcache_params)
      #logging.info('result_stats.GetStats browsers=%s, stats(cache)=%s' %
      #             (browsers, stats))
    total_runs = 0
    try:
      for browser in browsers:
        #logging.info('result_stats.GetStats for browser=%s' % browser)
        if browser not in stats:
          dirty = True
          medians, num_scores = test_set.GetMediansAndNumScores(browser)
          stats[browser] = test_set.GetStats(test_keys, medians, num_scores)
          # Store memcache incrementally if we're working a *big* test.
          if len(test_keys) > 30:
            memcache.set_multi(stats, **memcache_params)
        else:
          logging.info('result_stats.GetStats found it cached for browser=%s'
                       % (browser))
        total_runs += stats[browser].get('total_runs', 0)
    except DeadlineExceededError:
      # Try to get what we got in memcache.
      logging.info('DeadlineExceededError caught! Trying to memcahce %s' %
                   stats)
      memcache.set_multi(stats, **memcache_params)
      logging.info('Whew, made it.')

    if use_memcache and dirty:
      logging.info('result_stats.GetStats saving memcache %s' % stats)
      memcache.set_multi(stats, **memcache_params)
    stats['total_runs'] = total_runs
    return stats

  @classmethod
  def FindUncachedStats(cls, category, browsers):
    """Find which stats are not cached.

    Also, resets the summary stats for the stats that are found in memcache.

    Args:
      category: a category string like 'network'
      browsers: a list of browsers like ['Firefox 3.6', 'IE 8.0']
    Returns:
      a list of browsers without stats in memcache.
    """
    stats = memcache.get_multi(browsers, **cls.MemcacheParams(category))
    SummaryStatsManager.UpdateStats(category, stats)
    return [b for b in browsers if b not in stats]


  @classmethod
  def UpdateStatsCache(cls, category, browsers):
    """Update the memcache of stats for all the tests for each browser.

    This is also where the summary stats get updated.

    Args:
      category: a category string like 'network'
      browsers: a list of browsers like ['Firefox 3.6', 'IE 8.0']
    Returns:
      a list of browsers that were not processed due to a timeout.
    """
    test_set = all_test_sets.GetTestSet(category)
    test_keys = [t.key for t in test_set.VisibleTests()]
    ua_stats = {}
    unhandled_browsers = []
    is_timed_out = False
    for browser in browsers:
      try:
        medians, num_scores = test_set.GetMediansAndNumScores(browser)
      except db.Timeout:
        is_timed_out = True
      if is_timed_out:
        logging.info('Timed out \'%s\' in UpdateStatsCache doing '
                     'GetMediansAndNumScores for %s', category, browser)
        unhandled_browsers.append(browser)
      else:
        stats = test_set.GetStats(test_keys, medians, num_scores)
        ua_stats[browser] = stats
    memcache.set_multi(ua_stats, **cls.MemcacheParams(category))
    if not is_timed_out:
      SummaryStatsManager.UpdateStats(category, ua_stats)
    return unhandled_browsers

  @classmethod
  def MemcacheParams(cls, category):
    return {
        'namespace': '_'.join((cls.MEMCACHE_NAMESPACE_PREFIX, category))
        }

  @classmethod
  def DeleteMemcacheValues(cls, category, browsers):
    memcache.delete_multi(browsers, **cls.MemcacheParams(category))


def UpdateCategory(category, user_agent):
  logging.info('result.stats.UpdateCategory for %s, %s', category,
               user_agent.pretty())
  CategoryBrowserManager.AddUserAgent(category, user_agent)
  CategoryStatsManager.UpdateStatsCache(category, user_agent.get_string_list())
