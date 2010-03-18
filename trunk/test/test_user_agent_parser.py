#!/usr/bin/python2.5
#
# Copyright 2008 Google Inc.
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

"""User Agent Parser Unit Tests."""

__author__ = 'slamm@google.com (Stephen Lamm)'

import unittest

from models import user_agent_parser


TEST_STRINGS = (
    # ((family, v1, v2, v3), user_agent_string)
    (('Firefox (Shiretoko)', '3', '5', '1pre'),
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.1pre) '
     'Gecko/20090717 Ubuntu/9.04 (jaunty) Shiretoko/3.5.1pre'),
    (('Konqueror', '4', '3', '1'),
     'Mozilla/5.0 (X11; U; Linux; de-DE) AppleWebKit/527  '
     '(KHTML, like Gecko, Safari/419.3) konqueror/4.3.1,gzip(gfe),gzip(gfe)'),
    (('Other', None, None, None),
     'SomethingWeNeverKnewExisted'),
    )

class ParseTest(unittest.TestCase):

  def testStrings(self):
    for (family, v1, v2, v3), user_agent_string in TEST_STRINGS:
      self.assertEqual((family, v1, v2, v3),
                       user_agent_parser.Parse(user_agent_string))
