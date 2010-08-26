#!/usr/bin/python2.5

import csv
import logging
import re

import django
from django import http


class PartParser(object):
  """User Agent substring parser."""

  PATTERN_STRING_TEMPLATE = r'(%s)/(\S+)'
  ENDING_RE = r'(?:\s+|\s*$)'

  def __init__(self, pattern_string=None, pattern=None, priority=0, **kwds):
    if pattern is None:
      pattern = self.PATTERN_STRING_TEMPLATE % pattern_string
    if self.ENDING_RE:
      pattern += self.ENDING_RE
    self.pattern_re = re.compile(pattern)
    self.kwds = kwds
    self.priority = priority

  def Parse(self, parts, string):
    end = None
    match = self.pattern_re.match(string)
    if match:
      for key, value in self.kwds.items():
        if not isinstance(value, bool) and isinstance(value, int):
          value = match.group(value)
        if value:
          parts.setdefault(key, [])
          parts[key].append((self.priority, value))
      end = match.end()
      #logging.warn('end:%s,rest:%s', end, string[end:])
    return end


class ProductParser(PartParser):
  """Product part parser."""

  GROUPS = ('product', 'product_version')

  def __init__(self, pattern_string=None, pattern=None, **kwds):
    for index, key in enumerate(self.GROUPS):
      if key not in kwds:
        kwds[key] = index + 1
    PartParser.__init__(self, pattern_string, pattern, **kwds)


class RendererParser(ProductParser):
  """Renderer part parser."""

  GROUPS = ('renderer', 'renderer_version')


class CommentParser(PartParser):
  """Comment part parser."""

  PATTERN_STRING_TEMPLATE = r'%s'
  ENDING_RE = '(?:;\s+|\s*(?=[\(\)]))'


PRODUCT_PARSERS = (
    ProductParser('Mozilla', product=None, product_version=None),
    ProductParser('Safari', product_version=None, priority=-5),
    ProductParser('Firefox', priority=-3),
    ProductParser('Chrome'),
    ProductParser('Camino'),
    ProductParser(pattern=r'(Opera)[ /](\S+)'),
    ProductParser('SeaMonkey'),
    ProductParser('Minefield', product='Firefox', product_codename='Minefield'),
    ProductParser('Shiretoko', product='Firefox', product_codename='Shiretoko'),
    ProductParser('Lunascape'),
    ProductParser('Version', product=None, priority=10),
    ProductParser('Iceweasel'),
    ProductParser('NetNewsWire'),
    ProductParser('K-Meleon'),
    ProductParser('Arora'),
    ProductParser(pattern=r'(BlackBerry\d+)/(\S+)', product='RIM', platform=1, product_version=2),
    RendererParser('Gecko', renderer_version=None, renderer_date=2),
    RendererParser('AppleWebKit'),
    RendererParser('KHTML'),
    RendererParser('WebKit'),
    RendererParser('Trident'),
    RendererParser('Presto'),
    PartParser('Ubuntu', os=1, os_version=2),
    PartParser('Mobile', iphone_build_number=2),
    PartParser(pattern=r'(\S+)', unknown_product=1),
    # iCab for iCab 3 and before?
    )

COMMENT_PARSERS = (
    # name, pattern
    CommentParser(pattern=r'(Android)\ (\d[\d.]+)', platform=1, product=1, product_version=2, priority=15),
    CommentParser(pattern=r"""(?x)(
        Windows
        | Macintosh
        | X11
        | FreeBSD
        | iPod
        | iPhone\ Simulator
        | Linux
        )""", platform=1),
    CommentParser('iPhone', platform='iPhone', product='iPhone'),
    CommentParser('Win3.11', os='Windows 3.11'),
    CommentParser('WinNT3.51', os='Windows NT 3.51'),
    CommentParser('WinNT4.0', os='Windows NT 4.0'),
    CommentParser('Windows NT 4.0', os='Windows NT 4.0'),
    CommentParser('Windows NT 5.01', os='Windows 2000, Service Pack 1 (SP1)'),
    CommentParser('Windows NT 5.0', os='Windows 2000'),
    CommentParser('Windows NT 5.1', os='Windows XP'),
    CommentParser('Windows NT 5.2', os='Windows Server 2003; Windows XP x64 Edition'),
    CommentParser('Windows NT 6.0', os='Windows Vista'),
    CommentParser('Windows NT 6.1', os='Windows 7; Windows Server 2008 R2'),
    CommentParser('Windows 98; Win 9x 4.90', os='Windows Millennium Edition (Windows Me)'),
    CommentParser('Windows 98', os='Windows 98'),
    CommentParser('Win98', os='Windows 98'),
    CommentParser('Windows 95', os='Windows 95'),
    CommentParser('Win95', os='Windows 95'),
    CommentParser('Win 9x 4.90', os='Windows ME'),
    CommentParser('Windows CE', os='Windows CE'),
    CommentParser('WindowsCE', os='Windows CE'),
    CommentParser(pattern=r"""(?x)(
        | (?:Intel|PPC)\ Mac\ OS\ X(?:\ (?:\d[\d_.]+|Mach-O))?
        | CPU\ (?:iPhone\ OS\ \d[\d_]+\ )?like\ Mac\ OS\ X
        | Linux\ (?:i686(?:\ \(x86_64\))?|x86_64|armv[67]l)
        | FreeBSD\ (?:i386|7)
        | OpenBSD\ (?:i386|amd64)
        | SunOS\ i86pc
        )""", os=1),
    CommentParser('N', security='No security'),
    CommentParser('U', security='Strong security'),
    CommentParser('I', security='Weak security'),
    CommentParser('US_en', language='en-US'),
    CommentParser(pattern=r"""(?x)(
        [a-z][a-z](?:[-_][a-zA-Z]{2,3})?
        | ja-JP-mac
        | en-US-Hixie
        )""", language=1),
    CommentParser(pattern=r'^rv:([^;\s]+)', renderer_version=1),
    CommentParser('dream', platform='HTC G1'),
    CommentParser('generic', platform='Android SDK emulator'),
    CommentParser('compatible', is_compatible=True),
    CommentParser(pattern=r'^(\.NET CLR \d[.\d]+)', platform=1),
    CommentParser(pattern=r'^MSIE ([.\d]+)', product='IE', product_version=1, priority=-3),
    CommentParser('WOW64', platform='32-bit application running on 64-bit processor'), # IE only?
    CommentParser('Win64; x64', cpu='64-bit processor (AMD)'),
    CommentParser('Win64; IA54', cpu='64-bit processor (Intel)'),
    CommentParser('Tablet PC', platform='Tablet services are installed'),
    CommentParser('SV1', security='IE 6 with enhanced security features'),
    CommentParser('Avant Browser', product='Avant', product_version='1', priority=5),  # version is bogus; should this be IE instead?
    ProductParser('ANTGalio'),
    CommentParser(pattern='([^;\(\)]+)', unknown_comment=1),
    )

MSIE_RE = re.compile(r"""(?x)
    ^Mozilla/4\.0\ \(
        compatible;\ MSIE\
        (?P<version>[^;]+)
        ;\ (?P<os>[^;]+)
        (?:;\ ([^;]+))?
        (?:;[^;]*)*
        \)
    (?:\ (?P<override_product>[^/\s]+)[/\s]
         (?P<override_version>v?\d+[\.\w]*))?
    """)


class UserAgent(object):
  def __init__(self, string):
    self.string = string
    self.parts = {}

  def TopPart(self, part_key):
    value = None
    if part_key in self.parts:
      value = sorted(self.parts[part_key], reverse=True)[0][1]
    return value

  def Parse(self):
    pos = 0
    comment_level = 0
    while pos < len(self.string):
      if self.string[pos] == ' ':
        pos += 1
        continue
      if self.string[pos] == '(':
        pos += 1
        comment_level += 1
        continue
      if self.string[pos] == ')':
        pos += 1
        comment_level -= 1
        continue
      if comment_level == 0:
        parsers = PRODUCT_PARSERS
      else:
        parsers = COMMENT_PARSERS
      #logging.warn("%s: '%s'", comment_level, self.string[pos:])
      for comment_parser in parsers:
        parts = self.parts
        if comment_level > 1:
          parts = self.parts.setdefault('nested_comment', {})
        end = comment_parser.Parse(parts, self.string[pos:])
        if end:
          #logging.warn('Matched: %s', pos)
          pos += end
          break
      else:
        break
    self.matched = self.string[:pos]
    self.unmatched = self.string[pos:]

def ParseTest(request):
  ua_file = open('test/ua.csv')
  #ua_file = open('test/ua_sample.csv')
  data = list(csv.DictReader(
      ua_file, fieldnames=["pbrowser","browser","v1","v2","v3","useragent"]))
  content = []
  for row in data:
    browser = row['pbrowser']
    ua = UserAgent(row['useragent'])
    ua.Parse()

    browser_parts = []
    product = ua.TopPart('product')
    if product:
      browser_parts.append(product)
    codename = ua.TopPart('product_codename')
    if codename:
      browser_parts.append('(%s)' % codename)
    version = ua.TopPart('product_version')
    if version:
      browser_parts.append(version)
    browser_new = ' '.join(browser_parts)
    if not browser_new.startswith(browser):
      content.append('<b>%s</b> ' % browser)
      content.append('%s<font color=red>%s</font><br>'
                     % (ua.matched, ua.unmatched))
      content.append('<b>%s</b> ' % browser_new)
      content.append(' %s<p>' % str(ua.parts))
  return http.HttpResponse(''.join(content))
