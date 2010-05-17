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

import re
import logging
import sys

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
    'Bolt|Jasmine|Midori|Maxthon|Lynx|Arora|IBrowse|Dillo|Camino|Shiira|Fennec|'
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
  _P(r'(MozillaDeveloperPreview)/(\d+)\.(\d+)([ab]\d+[a-z]*)?'),
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
  _P(r'(Opera)/.+Opera Mobi.+Version/(\d+)\.(\d+)',
      family_replacement='Opera Mobile'),
  _P(r'(Opera)/9.80.*Version\/(\d+)\.(\d+)(?:\.(\d+))?'),

  # Palm WebOS looks a lot like Safari.
  _P('(webOS)/(\d+)\.(\d+)', 'Palm webOS'),

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
  _P(r'\(iPad;.+(Version)/(\d+)\.(\d+)(?:\.(\d+))?.*Safari/',
     family_replacement='iPad'),
  _P(r'(Version)/(\d+)\.(\d+)(?:\.(\d+))?.*Safari/',
     family_replacement='Safari'),
  _P(r'(OLPC)/Update(\d+)\.(\d+)'),
  _P(r'(OLPC)/Update()\.(\d+)', v1_replacement='0'),
  _P(r'(SamsungSGHi560)', family_replacement='Samsung SGHi560'),
  _P(r'^(SonyEricssonK800i)', family_replacement='Sony Ericsson K800i'),
  _P(r'(Teleca Q7)'),
  _P(r'(MSIE) (\d+)\.(\d+)', family_replacement='IE'),
)
# select family, v1, v2, v3 from user_agent where v3 regexp '[a-zA-Z]' group by family, v1, v2, v3;


def GetFilters(user_agent_string, js_user_agent_string=None,
          js_document_mode=None):
  """Return the optional arguments that should be saved and used to query.

  js_user_agent_string is always returned if it is present. We really only need
  it for Chrome Frame. However, I added it in the generally case to find other
  cases when it is different. When the recording of js_user_agent_string was
  added, we created new records for all new user agents.

  Since we only added js_document_mode for the IE 9 preview case, it did not
  cause new user agent records the way js_user_agent_string did.

  Args:
    user_agent_string: The full user-agent string.
    js_user_agent_string: JavaScript ua string from client-side
    js_document_mode: JavaScript document.documentMode ('9' for IE 9 preview)
  Returns:
    {js_user_agent_string: '[...]', js_document_mode: '[...]'}
  """
  filters = {}
  if js_user_agent_string is not None:
    filters['js_user_agent_string'] = js_user_agent_string
  if js_document_mode == '9':
    # Detect the IE 9 case
    filters['js_document_mode'] = '9'
  return filters


def Parse(user_agent_string, js_user_agent_string=None,
          js_document_mode=None):
  """Parses the user-agent string and returns the bits.

  Args:
    user_agent_string: The full user-agent string.
    js_user_agent_string: JavaScript ua string from client-side
    js_document_mode: JavaScript document.documentMode ('9' for IE 9 preview)
  Returns:
    [family, v1, v2, v3]
    e.g. ['Chrome', '4', '0', '203']
  """
  for parser in USER_AGENT_PARSERS:
    family, v1, v2, v3 = parser.Parse(user_agent_string)
    if family:
      break
  # Override for Chrome Frame IFF Chrome is enabled.
  if (js_user_agent_string and js_user_agent_string.find('Chrome/') > -1 and
      user_agent_string.find('chromeframe') > -1):
    family = 'Chrome Frame (%s %s)' % (family, v1)
    cf_family, v1, v2, v3 = Parse(js_user_agent_string)
  if (js_document_mode == '9' and family == 'IE' and v1 == '8'):
    family, v1 = 'IE Platform Preview', '9'
  return family or 'Other', v1, v2, v3
