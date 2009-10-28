#!/usr/bin/python2.4
#
# Copyright 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the 'License')
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Shared models."""

import re
import logging
import sys

from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.api.labs import taskqueue


BROWSER_NAV = [
  # version_level, label
  ('top', 'Top Browsers'),
  ('0', 'Browser Families'),
  ('1', 'Major Versions'),
  ('2', 'Minor Versions'),
  ('3', 'All Versions')
]

TOP_USER_AGENT_GROUP_STRINGS = [
  'Chrome 2', 'Chrome 3', 'Chrome 4',
  'Firefox 3.0', 'Firefox 3.5',
  'IE 6', 'IE 7', 'IE 8',
  'iPhone 2.2', 'iPhone 3.1',
  'Opera 9.64', 'Opera 10',
  'Safari 3.2', 'Safari 4.0'
]
#TOP_USER_AGENT_GROUP_STRINGS = ['Firefox 3.0.5', 'Firefox 3.5', 'IE 8']

# Mainly used for SeedDatastore
TOP_USER_AGENT_STRINGS = (
  ('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) '
   'AppleWebKit/530.1 (KHTML, like Gecko) '
   'Chrome/2.0.169 Safari/530.1'),
  ('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) '
   'AppleWebKit/530.1 (KHTML, like Gecko) '
   'Chrome/3.0.169.1 Safari/530.1'),
  ('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) '
   'AppleWebKit/530.1 (KHTML, like Gecko) '
   'Chrome/4.0.169.1 Safari/530.1'),
  ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) '
   'Gecko/2009011912 Firefox/3.0.3'),
  ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) '
   'Gecko/2009011912 Firefox/3.5.3'),
  ('Mozilla/4.0 '
   '(compatible; MSIE 6.0; Windows NT 5.1; Trident/4.0; '
   '.NET CLR 2.0.50727; .NET CLR 1.1.4322; '
   '.NET CLR 3.0.04506.648; .NET CLR 3.5.21022)'),
  ('Mozilla/4.0 '
   '(compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; '
   '.NET CLR 2.0.50727; .NET CLR 1.1.4322; '
   '.NET CLR 3.0.04506.648; .NET CLR 3.5.21022)'),
  ('Mozilla/4.0 '
   '(compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; '
   '.NET CLR 2.0.50727; .NET CLR 1.1.4322; '
   '.NET CLR 3.0.04506.648; .NET CLR 3.5.21022)'),
  'Opera/9.64 (Windows NT 5.1; U; en) Presto/2.1.1',
  'Opera/10.00 (Windows NT 5.1; U; en) Presto/2.2.0',
  ('Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_4_11; en) '
   'AppleWebKit/525.27.1 (KHTML, like Gecko) Version/3.2.1 Safari/525.27.1'),
  ('Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_4_11; en) '
   'AppleWebKit/525.27.1 (KHTML, like Gecko) Version/4.0.1 Safari/525.27.1'),
)


class UserAgentParser(object):
  def __init__(self, pattern, family_replacement=None, v1_replacement=None):
    """Initialize UserAgentParser.

    Args:
      pattern: a regular expression string
      family_replacement: a string to override the matched family (optional)
      v1_replacement: a string to override the matched v1 (optional)
    """
    self.pattern = pattern
    self.user_agent_re = re.compile(self.pattern)
    self.family_replacement = family_replacement
    self.v1_replacement = v1_replacement

  def MatchSpans(self, user_agent_string):
    match_spans = []
    match = self.user_agent_re.search(user_agent_string)
    if match:
      match_spans = [match.span(group_index)
                     for group_index in range(1, match.lastindex + 1)]
    return match_spans

  def Parse(self, user_agent_string):
    family, v1, v2, v3 = None, None, None, None
    match = self.user_agent_re.search(user_agent_string)
    if match:
      if self.family_replacement:
        if re.search(r'\$1', self.family_replacement):
          family = re.sub(r'\$1', match.group(1), self.family_replacement)
        else:
          family = self.family_replacement
      else:
        family = match.group(1)

      if self.v1_replacement:
        v1 = self.v1_replacement
      elif match.lastindex >= 2:
        v1 = match.group(2)
      if match.lastindex >= 3:
        v2 = match.group(3)
        if match.lastindex >= 4:
          v3 = match.group(4)
    return family, v1, v2, v3



browser_slash_v123_names = (
    'Jasmine|ANTGalio|Midori|Fresco|Lobo|Maxthon|Lynx|OmniWeb|Dillo|Camino|'
    'Demeter|Fluid|Fennec|Shiira|Sunrise|Chrome|Flock|Netscape|Lunascape|'
    'Epiphany|WebPilot|Vodafone|NetFront|Konqueror|SeaMonkey|Kazehakase|'
    'Vienna|Iceape|Iceweasel|IceWeasel|Iron|K-Meleon|Sleipnir|Galeon|'
    'GranParadiso|Opera Mini|iCab|NetNewsWire|Iron|Iris')

browser_slash_v12_names = (
    'Bolt|Jasmine|Maxthon|Lynx|Arora|IBrowse|Dillo|Camino|Shiira|Fennec|'
    'Phoenix|Chrome|Flock|Netscape|Lunascape|Epiphany|WebPilot|'
    'Opera Mini|Opera|Vodafone|'
    'NetFront|Konqueror|SeaMonkey|Kazehakase|Vienna|Iceape|Iceweasel|IceWeasel|'
    'Iron|K-Meleon|Sleipnir|Galeon|GranParadiso|'
    'iCab|NetNewsWire|Iron|Space Bison|Stainless|Orca')

_P = UserAgentParser
USER_AGENT_PARSERS = (
  #### SPECIAL CASES TOP ####
  # must go before Opera
  _P(r'^(Opera)/(\d+)\.(\d+) \(Nintendo Wii', family_replacement='Wii'),
  # must go before Browser/v1.v2 - eg: Minefield/3.1a1pre
  _P(r'(Namoroka|Shiretoko|Minefield)/(\d+)\.(\d+)\.(\d+(?:pre)?)',
     'Firefox ($1)'),
  _P(r'(Namoroka|Shiretoko|Minefield)/(\d+)\.(\d+)([ab]\d+[a-z]*)?',
     'Firefox ($1)'),
  _P(r'(SeaMonkey|Fennec|Camino)/(\d+)\.(\d+)([ab]?\d+[a-z]*)'),
  # e.g.: Flock/2.0b2
  _P(r'(Flock)/(\d+)\.(\d+)(b\d+?)'),

  # e.g.: Fennec/0.9pre
  _P(r'(Fennec)/(\d+)\.(\d+)(pre)'),
  _P(r'(Navigator)/(\d+)\.(\d+)\.(\d+)', 'Netscape'),
  _P(r'(Navigator)/(\d+)\.(\d+)([ab]\d+)', 'Netscape'),
  _P(r'(Netscape6)/(\d+)\.(\d+)\.(\d+)', 'Netscape'),
  _P(r'(MyIBrow)/(\d+)\.(\d+)', 'My Internet Browser'),
  _P(r'(Firefox).*Tablet browser (\d+)\.(\d+)\.(\d+)', 'MicroB'),
  # Opera will stop at 9.80 and hide the real version in the Version string.
  # see: http://dev.opera.com/articles/view/opera-ua-string-changes/
  _P(r'(Opera)/9.80.*Version\/(\d+)\.(\d+)(?:\.(\d+))?'),

  _P(r'(Firefox)/(\d+)\.(\d+)\.(\d+(?:pre)?) \(Swiftfox\)', 'Swiftfox'),
  _P(r'(Firefox)/(\d+)\.(\d+)([ab]\d+[a-z]*)? \(Swiftfox\)', 'Swiftfox'),

  # catches lower case konqueror
  _P(r'(konqueror)/(\d+)\.(\d+)\.(\d+)', 'Konqueror'),

  # Maemo

  #### END SPECIAL CASES TOP ####

  #### MAIN CASES - this catches > 50% of all browsers ####
  # Browser/v1.v2.v3
  _P(r'(%s)/(\d+)\.(\d+)\.(\d+)' % browser_slash_v123_names),
  # Browser/v1.v2
  _P(r'(%s)/(\d+)\.(\d+)' % browser_slash_v12_names),
  # Browser v1.v2.v3 (space instead of slash)
  _P(r'(iRider|Crazy Browser|SkipStone|iCab|Lunascape|Sleipnir|Maemo Browser) (\d+)\.(\d+)\.(\d+)'),
  # Browser v1.v2 (space instead of slash)
  _P(r'(iCab|Lunascape|Opera|Android) (\d+)\.(\d+)'),
  _P(r'(IEMobile) (\d+)\.(\d+)', 'IE Mobile'),
  # DO THIS AFTER THE EDGE CASES ABOVE!
  _P(r'(Firefox)/(\d+)\.(\d+)\.(\d+)'),
  _P(r'(Firefox)/(\d+)\.(\d+)(pre|[ab]\d+[a-z]*)?'),
  #### END MAIN CASES ####

  #### SPECIAL CASES ####
  #_P(r''),
  _P(r'(Obigo|OBIGO)[^\d]*(\d+)(?:.(\d+))?', 'Obigo'),
  _P(r'(MAXTHON|Maxthon) (\d+)\.(\d+)', family_replacement='Maxthon'),
  _P(r'(Maxthon|MyIE2|Uzbl|Shiira)', v1_replacement='0'),
  _P(r'(PLAYSTATION) (\d+)', family_replacement='PlayStation'),
  _P(r'(PlayStation Portable)[^\d]+(\d+).(\d+)'),
  _P(r'(BrowseX) \((\d+)\.(\d+)\.(\d+)'),
  _P(r'(Opera)/(\d+)\.(\d+).*Opera Mobi', 'Opera Mobile'),
  _P(r'(POLARIS)/(\d+)\.(\d+)', family_replacement='Polaris'),
  _P(r'(BonEcho)/(\d+)\.(\d+)\.(\d+)', 'Bon Echo'),
  _P(r'(iPhone) OS (\d+)_(\d+)(?:_(\d+))?'),
  _P(r'(Avant)', v1_replacement='1'),
  _P(r'(Nokia)[EN]?(\d+)'),
  _P(r'(Black[bB]erry)(\d+)', family_replacement='Blackberry'),
  _P(r'(OmniWeb)/v(\d+)\.(\d+)'),
  _P(r'(Blazer)/(\d+)\.(\d+)', 'Palm Blazer'),
  _P(r'(Pre)/(\d+)\.(\d+)', 'Palm Pre'),
  _P(r'(Links) \((\d+)\.(\d+)'),
  _P(r'(QtWeb) Internet Browser/(\d+)\.(\d+)'),
  _P(r'(Version)/(\d+)\.(\d+)(?:\.(\d+))?.*Safari/',
     family_replacement='Safari'),
  _P(r'(OLPC)/Update(\d+)\.(\d+)'),
  _P(r'(OLPC)/Update()\.(\d+)', v1_replacement='0'),
  _P(r'(SamsungSGHi560)', family_replacement='Samsung SGHi560'),
  _P(r'^(SonyEricssonK800i)', family_replacement='Sony Ericsson K800i'),
  _P(r'(Teleca Q7)'),
  _P(r'(MSIE) (\d+)\.(\d+)', family_replacement='IE'),
)


class UserAgentGroup(db.Model):
  """Group pretty user agents strings (e.g. 'Firefox 3.2') by version level."""

  string = db.StringProperty()
  v = db.StringProperty()  # version level

  @classmethod
  def UpdateGroups(cls, user_agent_list, is_rebuild=False):
    """Add the list of user_agents to their respective version-level groups.

    Add a string for every version level.
    If a level does not have a string, then one from the previous level.
    For example, "Safari 4.3" would add the following:
        level      string
            0  Safari
            1  Safari 4
            2  Safari 4.3
            3  Safari 4.3

    Args:
      user_agent_list: a list of user_agent_version strings
          (e.g. ['Firefox', 'Firefox 3', 'Firefox 3.5'])
    """
    max_index = len(user_agent_list) - 1
    for v in (3, 2, 1, 0):
      is_cached = cls.AddString(v, user_agent_list[min(v, max_index)],
                                is_rebuild)
      if is_cached:
        # Assume higher levels were added previously.
        break

  @classmethod
  def AddString(cls, version_level, string, is_rebuild):
    """Add a string to a particular version level.

    Args:
      version_level: an integer: 0 (family), 1 (major), 2 (minor), 3 (3rd)
      string: a user_agent_version string (e.g. 'Firefox 3')
      is_rebuild: True if creating non-live version (i.e. memcache only version)
    Returns:
      True if the string is newly added.
      False if the string was found in memcache.
    """
    is_cached = True
    memcache_key = cls._MakeMemcacheKey(version_level, is_rebuild)
    user_agent_strings = (memcache.get(memcache_key) or
                          cls._QueryStrings(version_level))
    if string not in user_agent_strings:
      key_name = cls._MakeKeyName(version_level, string)
      cls.get_or_insert(key_name, v=str(version_level), string=string)
      user_agent_strings.append(string)
      cls.SortUserAgentStrings(user_agent_strings)
      memcache.set(memcache_key, user_agent_strings)
      is_cached = False
    return is_cached

  @classmethod
  def GetStrings(cls, version_level):
    """Get all the strings for one version level.

    Args:
      version_level: an integer: 0 (family), 1 (major), 2 (minor), 3 (3rd)
    Returns:
      a sorted list of user_agent_version strings
      e.g. ['Firefox 3.1', 'Firefox 3.2', 'Safari 4.0', 'Safari 4.5', ...]
    """
    version_level = str(version_level)
    if version_level == 'top':
      user_agent_strings = TOP_USER_AGENT_GROUP_STRINGS[:]
    else:
      memcache_key = cls._MakeMemcacheKey(version_level)
      user_agent_strings = memcache.get(memcache_key)
      if not user_agent_strings:
        user_agent_strings = cls._QueryStrings(version_level)
        memcache.set(memcache_key, user_agent_strings)
    return user_agent_strings

  @classmethod
  def _QueryStrings(cls, version_level):
    user_agent_strings = [x.string for x in
                          cls.all().filter('v =', version_level).fetch(1000)]
    if len(user_agent_strings) > 900:
      # TODO: Handle more than 1000 user agents strings in a group.
      logging.warn('UserAgentGroup: Group will max out at 1000:'
                   ' version_level=%s, len(user_agent_strings)=%s',
                   version_level, len(user_agent_strings))
    cls.SortUserAgentStrings(user_agent_strings)
    return user_agent_strings

  @classmethod
  def SortUserAgentStrings(cls, user_agent_strings):
    """Sort user agent strings in-place.

    Args:
      user_agents_strings: a list of strings
          e.g. ['iPhone 3.1', 'Firefox 3.01', 'Safari 4.1']
    """
    user_agent_strings.sort(key=lambda x: x.lower())

  @classmethod
  def ReleaseRebuild(cls):
    """Move memcache version live."""
    is_rebuild_complete = False
    all_rebuild_strings = [
        memcache.get(cls._MakeMemcacheKey(v, is_rebuild=True))
        for v in range(4)]
    for version_level, rebuild_strings in enumerate(all_rebuild_strings):
      if not rebuild_strings:
        # We expect a list of strings at every version level.
        logging.warn('Missing strings for rebuild: version_level=%s',
                     version_level)
        return is_rebuild_complete
    deletions = set()
    for version_level, rebuild_strings in enumerate(all_rebuild_strings):
      existing_strings = cls.GetStrings(version_level)
      if existing_strings != rebuild_strings:
        memcache.set(cls._MakeMemcacheKey(version_level), rebuild_strings)
        deletions.update([
            (version_level, string)
            for string in set(existing_strings) - set(rebuild_strings)])
    if deletions:
      db.delete([db.Key.from_path(cls.__name__, cls._MakeKeyName(v, s))
                 for v, s in deletions])
    is_rebuild_complete = True
    return is_rebuild_complete

  @classmethod
  def ClearMemcache(cls, version_level, is_rebuild=False):
    memcache_key = cls._MakeMemcacheKey(version_level, is_rebuild)
    memcache.delete(memcache_key)

  @staticmethod
  def _MakeKeyName(version_level, user_agent_string):
    return 'key:%s_%s' % (version_level, user_agent_string)

  @staticmethod
  def _MakeMemcacheKey(version_level, is_rebuild=False):
    return 'user_agent_group_%s%s' % (
        version_level, is_rebuild and '_rebuild' or '')


class UserAgent(db.Expando):
  """User Agent Model."""
  string = db.StringProperty()
  family = db.StringProperty()
  v1 = db.StringProperty()
  v2 = db.StringProperty()
  v3 = db.StringProperty()
  confirmed = db.BooleanProperty(default=False)
  created = db.DateTimeProperty(auto_now_add=True)

  def pretty(self):
    """Invokes pretty print."""
    return self.pretty_print(self.family, self.v1, self.v2, self.v3)

  def get_string_list(self):
    """Returns a list of a strings suitable a StringListProperty."""
    return self.parts_to_string_list(self.family, self.v1, self.v2, self.v3)

  def update_groups(self):
    """Account for this user agent in the user agent groups."""
    UserAgentGroup.UpdateGroups(self.get_string_list())

  @classmethod
  def factory(cls, string, **kwds):
    """Factory function.

    Args:
      string: the http user agent string.
      kwds: any addional key/value properties.
          e.g. js_user_agent_string='Mozilla/5.0 (Windows; U; Windows NT 5.1; '
              'en-US) AppleWebKit/530.1 (KHTML, like Gecko) Chrome/2.0.169.1 '
              'Safari/530.1')
    Returns:
      a UserAgent instance
    """
    query = db.Query(cls)
    query.filter('string =', string)
    for key, value in kwds.items():
      if value is not None:
        query.filter('%s =' % key, value)
    user_agent = query.get()
    if user_agent is None:
      family, v1, v2, v3 = cls.parse(string, **kwds)
      user_agent = cls(string=string,
                       family=family,
                       v1=v1,
                       v2=v2,
                       v3=v3,
                       **kwds)
      user_agent.put()
      try:
        taskqueue.Task(method='GET', params={'key': user_agent.key()}
                      ).add(queue_name='user-agent-group')
      except:
        logging.info('Cannot add task: %s:%s' % (sys.exc_type, sys.exc_value))
    return user_agent


  @classmethod
  def parse(cls, user_agent_string, js_user_agent_string=None):
    """Parses the user-agent string and returns the bits.

    Args:
      user_agent_string: The full user-agent string.
    """
    for parser in USER_AGENT_PARSERS:
      family, v1, v2, v3 = parser.Parse(user_agent_string)
      if family:
        break
    # Override for Chrome Frame IFF Chrome is enabled.
    if (js_user_agent_string and js_user_agent_string.find('Chrome/') > -1 and
        user_agent_string.find('chromeframe') > -1):
      family = 'Chrome Frame (%s %s)' % (family, v1)
      cf_family, v1, v2, v3 = cls.parse(js_user_agent_string)
    return family or 'Other', v1, v2, v3

  @staticmethod
  def parse_pretty(pretty_string):
    """Parse a user agent pretty (e.g. 'Chrome 4.0.203') to parts.

    Args:
      pretty_string: a user agent pretty string (e.g. 'Chrome 4.0.203')
    Returns:
      [family, v1, v2, v3] e.g. ['Chrome', '4', '0', '203']
    """
    v1, v2, v3 = None, None, None
    family, sep, version_str = pretty_string.rpartition(' ')
    if not family:
      family = version_str
    else:
      version_bits = version_str.split('.')
      v1 = version_bits.pop(0)
      if not v1.isdigit():
        family = pretty_string
        v1 = None
      elif version_bits:
        v2 = version_bits.pop(0)
        if not v2.isdigit():
          nondigit_index = min(i for i, c in enumerate(v2) if not c.isdigit())
          v2, v3 = v2[:nondigit_index], v2[nondigit_index:]
        elif version_bits:
          v3 = version_bits.pop(0)
    return family, v1, v2, v3


  @staticmethod
  def MatchSpans(user_agent_string):
    """Parses the user-agent string and returns the bits.

    Used by the "Confirm User Agents" admin page to highlight matches.

    Args:
      user_agent_string: The full user-agent string.
    """
    for parser in USER_AGENT_PARSERS:
      match_spans = parser.MatchSpans(user_agent_string)
      if match_spans:
        return match_spans
    return []

  @staticmethod
  def pretty_print(family, v1=None, v2=None, v3=None):
    """Pretty browser string."""
    if v3:
      if v3[0].isdigit():
        return '%s %s.%s.%s' % (family, v1, v2, v3)
      else:
        return '%s %s.%s%s' % (family, v1, v2, v3)
    elif v2:
      return '%s %s.%s' % (family, v1, v2)
    elif v1:
      return '%s %s' % (family, v1)
    return family

  @classmethod
  def parts_to_string_list(cls, family, v1=None, v2=None, v3=None):
    """Return a list of user agent version strings.

    e.g. ['Firefox', 'Firefox 3', 'Firefox 3.5']
    """
    string_list = []
    if family:
      string_list.append(family)
      if v1:
        string_list.append(cls.pretty_print(family, v1))
        if v2:
          string_list.append(cls.pretty_print(family, v1, v2))
          if v3:
            string_list.append(cls.pretty_print(family, v1, v2, v3))
    return string_list

  @classmethod
  def parse_to_string_list(cls, pretty_string):
    """Parse a pretty string into string list."""
    return cls.parts_to_string_list(*cls.parse_pretty(pretty_string))
