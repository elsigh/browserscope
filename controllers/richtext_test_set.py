#!/usr/bin/python2.4
#
# Copyright 2009 Google Inc.
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

"""Reflow Test Definitions."""

__author__ = 'elsigh@google.com (Lindsey Simon)'


from controllers import test_set_base


_CATEGORY = 'richtext'


class RichtextTest(object):
  TESTS_URL_PATH = '/%s/test' % _CATEGORY
  def __init__(self, key, name, doc):
    self.key = key
    self.name = name
    self.url = '%s?t=%s' % (self.TESTS_URL_PATH, key)
    self.score_type = 'custom'
    self.doc = doc
    self.min_value, self.max_value = 0, 60000



_TESTS = (
  # key, name, doc
  RichtextTest('testDisplay', 'Display Block',
    '''This test takes an element and sets its
    style.display="none". According to the folks at Mozilla this has
    the effect of taking an element out of the browser's "render tree" -
    the in-memory representation of all of results of
    geometry/positioning calculations for that particular
    element. Setting an element to display="none" has the additional
    effect of removing all of an elements children from the render tree
    as well. Next, the test resets the element's style.display="", which
    sets the element's display back to its original value. Our thinking
    was that this operation ought to approximate the cost of reflowing
    an element on a particular page since the browser would have to
    recalculate all the positions and sizes for every child within the
    element as well as make any changes to the overall document that
    this change would cause to parents and ancestors. This was
    originally the only test that the Reflow Timer performed, but as you
    can see from the results, we discovered that not all render engines
    work like Gecko's and so we began adding more tests.'''),
)


TEST_SET = test_set_base.TestSet(
    category=_CATEGORY,
    category_name='Richtext',
    tests=_TESTS,
    subnav={
      'Test': '/%s/test' % _CATEGORY,
      'About': '/%s/about' % _CATEGORY
    },
    home_intro=''
)
