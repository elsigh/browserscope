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
  'iPhone 2.2',
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
      else:
        if match.lastindex >= 2:
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
    'GranParadiso|Opera Mini|iCab|NetNewsWire|Iron')

browser_slash_v12_names = (
    'Bolt|Jasmine|Maxthon|Lynx|Arora|IBrowse|Dillo|Camino|Shiira|Fennec|'
    'Phoenix|Chrome|Flock|Netscape|Lunascape|Epiphany|WebPilot|'
    'Opera Mini|Opera|Vodafone|'
    'NetFront|Konqueror|SeaMonkey|Kazehakase|Vienna|Iceape|Iceweasel|IceWeasel|'
    'Iron|K-Meleon|Sleipnir|Galeon|GranParadiso|'
    'iCab|NetNewsWire|Iron')

_P = UserAgentParser
USER_AGENT_PARSERS = (
  #### SPECIAL CASES TOP ####
  # must go before Opera
  _P(r'(Wii)'),
  # must go before Browser/v1.v2 - eg: Minefield/3.1a1pre
  _P(r'(Namoroka|Shiretoko|Minefield)/(\d+)\.(\d+)\.?([ab]?\d+[a-z]*)',
     'Firefox ($1)'),
  _P(r'(Namoroka|Shiretoko|Minefield)/(\d+)\.(\d+)',
     'Firefox ($1)'),
  _P(r'(SeaMonkey|Fennec|Camino)/(\d+)\.(\d+)([ab]?\d+[a-z]*)'),
  # eg: Fennec/0.9pre
  _P(r'(Fennec)/(\d+)\.(\d+)(pre)'),
  _P(r'(Navigator)/(\d+)\.(\d+)\.(\d+)', 'Netscape'),
  _P(r'(Navigator)/(\d+)\.(\d+[ab]\d+)', 'Netscape'),
  _P(r'(Netscape6)/(\d+)\.(\d+)\.(\d+)', 'Netscape'),
  _P(r'(MyIBrow)/(\d+)\.(\d+)', 'My Internet Browser'),
  _P(r'(Firefox).*Tablet browser (\d+)\.(\d+)\.(\d+)', 'MicroB'),
  # Opera will stop at 9.80 and hide the real version in the Version string.
  # see: http://dev.opera.com/articles/view/opera-ua-string-changes/
  _P(r'(Opera)/9.80.*Version\/(\d+)\.(\d+)\.(\d+)'),
  _P(r'(Opera)/9.80.*Version\/(\d+)\.(\d+)'),

  _P(r'(Firefox)/(\d+)\.(\d+)\.(\d+) \(Swiftfox\)', 'Swiftfox'),
  _P(r'(Firefox)/(\d+)\.(\d+)\.(\d+pre) \(Swiftfox\)', 'Swiftfox'),
  _P(r'(Firefox)/(\d+)\.(\d+)([ab]\d+[a-z]*) \(Swiftfox\)', 'Swiftfox'),
  _P(r'(Firefox)/(\d+)\.(\d+) \(Swiftfox\)', 'Swiftfox'),

  #### END SPECIAL CASES TOP ####

  #### MAIN CASES - this catches > 50% of all browsers ####
  # Browser/v1.v2.v3
  _P(r'(%s)/(\d+)\.(\d+)\.(\d+)' % browser_slash_v123_names),
  # Browser/v1.v2
  _P(r'(%s)/(\d+)\.(\d+)' % browser_slash_v12_names),
  # Browser v1.v2.v3 (space instead of slash)
  _P(r'(iRider|Crazy Browser|SkipStone|iCab|Lunascape|Sleipnir) (\d+)\.(\d+)\.(\d+)'),
  # Browser v1.v2 (space instead of slash)
  _P(r'(iCab|Lunascape|Opera|Android) (\d+)\.(\d+)'),
  _P(r'(IEMobile) (\d+)\.(\d+)', 'IE Mobile'),
  # DO THIS AFTER THE EDGE CASES ABOVE!
  _P(r'(Firefox)/(\d+)\.(\d+)\.(\d+)'),
  _P(r'(Firefox)/(\d+)\.(\d+)([ab]\d+[a-z]*)'),
  _P(r'(Firefox)/(\d+)\.(\d+)(pre)'),
  _P(r'(Firefox)/(\d+)\.(\d+)'),
  #### END MAIN CASES ####

  #### SPECIAL CASES ####
  #_P(r''),
  _P(r'(Obigo)[^\d]*(\d+)'),
  _P(r'OBIGO[^\d]*(\d+)', 'Obigo'),
  _P(r'(MAXTHON|Maxthon) (\d+)\.(\d+)',
     family_replacement='Maxthon'),
  _P(r'(Maxthon|MyIE2|Uzbl)', v1_replacement='0'),
  _P(r'(PLAYSTATION) (\d+)',
     family_replacement='PlayStation'),
  _P(r'(BrowseX) \((\d+)\.(\d+)\.(\d+)'),
  _P(r'(Opera)/(\d+)\.(\d+).*Opera Mobi', 'Opera Mobile'),
  _P(r'(POLARIS)/(\d+)\.(\d+)',
     family_replacement='Polaris'),
  _P(r'(BonEcho)/(\d+)\.(\d+)\.(\d+)', 'Bon Echo'),
  _P(r'(iPhone) OS (\d+)_(\d+)_(\d+)'),
  _P(r'(iPhone) OS (\d+)_(\d+)'),
  _P(r'(Avant)', v1_replacement='1'),
  _P(r'(Nokia)[EN](\d+)'),
  _P(r'(Nokia)(\d+)'),
  _P(r'(Blackberry)(\d+)'),
  _P(r'(BlackBerry)(\d+)',
     family_replacement='Blackberry'),
  _P(r'(OmniWeb)/v(\d+)\.(\d+)'),
  _P(r'(Blazer)/(\d+)\.(\d+)', 'Palm Blazer'),
  _P(r'(Pre)/(\d+)\.(\d+)', 'Palm Pre'),
  _P(r'(Links) \((\d+)\.(\d+)'),
  _P(r'(QtWeb) Internet Browser/(\d+)\.(\d+)'),
  _P(r'(Version)/(\d+)\.(\d+)\.(\d+).*Safari/',
     family_replacement='Safari'),
  _P(r'(Version)/(\d+)\.(\d+).*Safari/',
     family_replacement='Safari'),
  _P(r'(OLPC)/Update(\d+)\.(\d+)'),
  _P(r'(OLPC)/Update\.(\d+)', v1_replacement='0'),
  _P(r'(MSIE) (\d+)\.(\d+)',
     family_replacement='IE'),
)


class UserAgentGroup(db.Model):
  string = db.StringProperty()
  v = db.StringProperty()  # version level

  @staticmethod
  def AddString(version_level, string):
    key_name = UserAgentGroup._MakeKeyName(version_level, string)
    UserAgentGroup.get_or_insert(key_name, v=str(version_level), string=string)

    # Now add string to memcache entry if it exists. Otherwise, skip.
    memcache_key = UserAgentGroup._MakeMemcacheKey(version_level)
    user_agent_strings = memcache.get(key=memcache_key)
    if user_agent_strings and string not in user_agent_strings:
      user_agent_strings.append(str(string))
      user_agent_strings.sort(key=str.lower)
      memcache.set(key=memcache_key, value=user_agent_strings)

  @staticmethod
  def GetStrings(version_level):
    version_level = str(version_level)
    if version_level == 'top':
      user_agent_strings = TOP_USER_AGENT_GROUP_STRINGS[:]
    else:
      memcache_key = UserAgentGroup._MakeMemcacheKey(version_level)
      user_agent_strings = memcache.get(key=memcache_key)
      if not user_agent_strings:
        query = UserAgentGroup.gql('WHERE v = :1', version_level)
        # Needs the string cast to avoid a unicode error on sort with str.lower.
        user_agent_strings = [str(x.string) for x in query.fetch(1000, 0)]
        if len(user_agent_strings) > 900:
          # TODO: Handle more than 1000 user agents strings in a group.
          logging.warn('UserAgentGroup: Group will max out at 1000:'
                       ' version_level=%s, len(user_agent_strings)=%s',
                       version_level, len(user_agent_strings))
        user_agent_strings.sort(key=str.lower)
        memcache.set(key=memcache_key, value=user_agent_strings)
    return user_agent_strings

  @staticmethod
  def ClearMemcache(version_level):
    memcache_key = UserAgentGroup._MakeMemcacheKey(version_level)
    memcache.delete(key=memcache_key, seconds=0)

  @staticmethod
  def _MakeKeyName(version_level, user_agent_string):
    return 'key:%s_%s' % (version_level, user_agent_string)

  @staticmethod
  def _MakeMemcacheKey(version_level):
    return 'user_agent_group_%s' % version_level


class UserAgent(db.Model):
  """User Agent Model."""
  string = db.StringProperty()
  family = db.StringProperty()
  v1 = db.StringProperty()
  v2 = db.StringProperty()
  v3 = db.StringProperty()
  confirmed = db.BooleanProperty(default=False)
  created = db.DateTimeProperty()


  def pretty(self):
    """Invokes pretty print."""
    return UserAgent.pretty_print(self.family, self.v1, self.v2, self.v3)


  def get_string_list(self):
    """Returns a list of a strings suitable a StringListProperty."""
    string_list = []
    string = self.family
    string_list.append(string)
    version_bits = [bit for bit in (self.v1, self.v2, self.v3) if bit]
    for sep, version_bit in zip((' ', '.', '.'), version_bits):
      string = sep.join((string, version_bit))
      string_list.append(string)
    return string_list


  def update_groups(self):
    """Make sure this new user agent is accounted for in the group.

    Add a string for every version level.
    If a level does not have a string, then one from the previous level.
    For example, "Safari 4.3" would add the following:
        level      string
            0  Safari
            1  Safari 4
            2  Safari 4.3
            3  Safari 4.3
    """
    string_list = self.get_string_list()
    max_string_index = len(string_list) - 1
    for v in (0, 1, 2, 3):
      string = string_list[min(v, max_string_index)]
      UserAgentGroup.AddString(v, string)


  @staticmethod
  def factory(string):
    """Factory function."""
    query = db.Query(UserAgent)
    query.filter('string =', string)
    user_agent = query.get()
    if user_agent is None:
      family, v1, v2, v3 = UserAgent.parse(string)
      user_agent = UserAgent(string=string,
                             family=family,
                             v1=v1,
                             v2=v2,
                             v3=v3)
      user_agent.put()

      try:
        taskqueue.Task(method='GET', params={'key': user_agent.key()}
                      ).add(queue_name='user-agent-group')
      except:
        logging.info('Cannot add task: %s:%s' % (sys.exc_type, sys.exc_value))

    return user_agent


  @staticmethod
  def parse(user_agent_string):
    """Parses the user-agent string and returns the bits.

    Args:
      user_agent_string: The full user-agent string.
    """
    for parser in USER_AGENT_PARSERS:
      family, v1, v2, v3 = parser.Parse(user_agent_string)
      if family:
        #logging.info('Used pattern: %s' % parser.pattern)
        return family, v1, v2, v3
    return 'Other', None, None, None

  @staticmethod
  def MatchSpans(user_agent_string):
    """Parses the user-agent string and returns the bits.

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

  @staticmethod
  def parse_to_string_list(pretty_string):
    """Parse a pretty string into string list."""
    string_list = []
    if pretty_string:
      family_end = pretty_string.find(' ')
      if family_end != -1:
        string_list.append(pretty_string[:family_end])
        v1_end = pretty_string.find('.', family_end + 1)
        if v1_end != -1:
          string_list.append(pretty_string[:v1_end])
          v2_end = pretty_string.find('.', v1_end + 1)
          if v2_end == -1:
            v2_end = pretty_string.find(' ', v1_end + 1)
          if v2_end != -1:
            string_list.append(pretty_string[:v2_end])
      string_list.append(pretty_string)
    return string_list
