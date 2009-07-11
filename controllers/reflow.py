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

"""Handlers for Reflow."""

__author__ = 'elsigh@google.com (Lindsey Simon)'

import datetime
import logging
import re
import urllib2

# Shared stuff
from shared import decorators
from shared import util

# Data structures for reflow testing.
from bin.reflow.run_reflow_timer import TEST_PAGES

from settings import *


CATEGORY = 'reflow'
CATEGORY_NAME = 'Reflow'

HOME_INTRO = ('Reflow in a web browser refers to the process of the render engine calculating the positions and geometry of elements in the document for purpose of drawing, or re-drawing, its visual presentation. Because reflow is a user-blocking operation in the browser, it is useful for developers to understand how to improve reflow times and also to understand the effects of various document properties (DOM nesting, CSS specificity, types of style changes) on reflow. <a href="/reflow/about">Read more about reflow and these tests.</a>')

class ReflowTest(object):
  TESTS_URL_PATH = '/%s/test' % CATEGORY
  def __init__(self, key, label, doc):
    self.key = key
    self.label = label
    self.url = '%s?t=%s' % (self.TESTS_URL_PATH, key)
    self.score_type = 'custom'
    self.doc = doc


TESTS = (
  # key, label, doc
  ReflowTest('testDisplay', 'Display Block',
    '''This test takes an element and sets its
    style.display="none". According to our friends at Mozilla this has
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
  ReflowTest('testVisibility', 'Visiblility None',
    '''Much like the display test above, this test sets an element's
    style.visibility="hidden" and then resets it back to its default,
    which is visible. Visually this has the same effect as setting
    display="none", however this change should be significantly less
    costly for the browser to perform as it should not need be purging
    the element from the render tree and recalculating
    geometries.'''),
  ReflowTest('testNonMatchingClass', 'Non Matching by Class',
    '''This test adds a class name to an element, and more specifically a
    class name which is not present in the document's CSS object
    model.'''),
  ReflowTest('testFourClassReflows', 'Four Reflows by Class',
    '''This test adds a class name to an element that will match a
    previously added CSS declaration added to the CSSOM. This
    declaration is set with four property value pairs which should in
    and of themselves be capable of causing a 1x reflow time. For
    instance, "font-size: 20px; line-height: 10px; padding-left: 10px;
    margin-top: 7px;". This test aims to test whether reflow
    operations occur in a single queue flush or if they are performed
    one at a time when these changes are made via a CSS
    classname. This test is a sort of opposite to the Four Reflows By
    Script.'''),
  ReflowTest('testFourScriptReflows', 'Four Reflows by Script',
    '''Like the Four Reflows By Class test, but instead this test has
    four lines of Javascript, each of which alters the style object
    with a property/value that by itself could cause a 1x reflow
    time.'''),
  ReflowTest('testTwoScriptReflows', 'Two Reflows by Script',
    '''Like the Four Reflows By Script test, except with only two lines
    of Javascript.'''),
  ReflowTest('testPaddingPx', 'Padding px',
    '''This test sets style.padding="FOOpx", aka padding on all sides of
    the box model.'''),
  ReflowTest('testPaddingLeftPx', 'Padding Left px',
    '''This test sets style.paddingLeft="FOOpx", aka padding on only the
    left side of the box.'''),
  ReflowTest('testFontSizeEm', 'Font Size em',
    '''This test changes an element's style.fontSize to an em-based
    value.'''),
  ReflowTest('testWidthPercent', 'Width %',
    '''This test sets an element's style.width="FOO%"'''),
  ReflowTest('testBackground', 'Background Color',
    '''This test sets an element's style.background="#FOO", aka a
    hexadecimal color.'''),
  ReflowTest('testOverflowHidden', 'Overflow Hidden',
    '''This test sets an element's style.overflow="hidden" and then back
    again, timing the cost of an element returning to the default
    overflow which is "visible"'''),
  ReflowTest('testSelectorMatchTime', 'Selector Match Time',
    '''In the world of reflow, one of the possible operations that can
    eat up time occurs when an element gets a new class name and the
    render engine has to look through the CSSOM to see if this element
    now matches some CSS declaration. The goal of this test is to try
    to cause this match operation without causing any change to the
    render tree. The test is much like the Non-Matching Class test,
    except that instead of flushing the render queue before this test,
    we try to simply flush any style computations. The way it works is
    to make a CSS rule that can get activated by virtue of an
    attribute selector but which will never cause reflow because it
    will never match any element in the render tree. For instance
    "body[bogusattr='bogusval'] html {color:pink}". We note that this
    test seems not to work in engines other than Gecko at this
    time.'''),
  ReflowTest('testGetOffsetHeight', 'Do Nothing / OffsetHeight',
    '''This test does nothing other than the request for offsetHeight
    after already having done so. Theoretically, this test is
    something like a control for our test and should have a 0 or very
    low time.'''),
)


def CustomTestsFunction(test, median):
  """Returns a tuple with display text for the cell as well as a 1-100 value.
  i.e. ('1X', 95)
  Args:
    test: A string representing the test.key
    median: The test median.
  Returns:
    A tuple of display, score
  """
  if not median:
    return('0.0', 0)

  time = round(float(median) / 1000.0, 1)
  #logging.info('CustomTestsFunction w/ %s, %s' % (test, median))

  abc = [1, 2, 3, 4]

  if test is 'testDisplay':
    abc = [.3, .5, 1, 1.5]
  elif test is 'testVisibility':
    abc = [.4, .7, 1.1, 1.6]
  elif test is 'testNonMatchingClass':
    abc = [.6, 1, 2, 3]
  elif test is 'testFourClassReflows':
    abc = [.6, 1, 2, 3]
  elif test is 'testFourScriptReflows':
    abc = [.6, 1, 2, 3]
  elif test is 'testTwoScriptReflows':
    abc = [.6, 1, 2, 3]
  elif test is 'testPaddingPx':
    abc = [.6, 1, 2, 3]
  elif test is 'testPaddingLeftPx':
    abc = [.6, 1, 1.5, 2]
  elif test is 'testFontSizeEm':
    abc = [.6, 1, 2, 3]
  elif test is 'testWidthPercent':
    abc = [.6, 1, 2, 3]
  elif test is 'testBackground':
    abc = [.6, 1, 2, 3]
  elif test is 'testOverflowHidden':
    abc = [.6, 1, 2, 3]
  elif test is 'testSelectorMatchTime':
    abc = [.6, 1, 1.5, 2]
  elif test is 'testGetOffsetHeight':
    abc = [0, .1, .2, .3]

  score = _GetScore(time, abc)
  #logging.info('TEST!! %s, %s, %s' % (test, time, score))

  return (str(time), score)


def _GetScore(time, abc):
  """Computes an A,B,C,DF like score out of 100 where abc represents
  cutoffs for 90,80,70,60 etc..."""
  if time <= abc[0]:
    base = 90
    bounds = [0, abc[0]]
  elif abc[0] < time <= abc[1]:
    base = 80
    bounds = [abc[0], abc[1]]
  elif abc[1] < time <= abc[2]:
    base = 70
    bounds = [abc[1], abc[2]]
  elif abc[2] < time <= abc[3]:
    base = 60
    bounds = [abc[2], abc[3]]
  else:
    bounds = None

  # Get their score out of 100, whereby bounds gives scores for
  # A, B, C, D
  # where time of 0 through bounds[0] is the spread for 100 through 90, etc.
  if bounds:
    delta = bounds[1] - bounds[0]
    unit = 1 / delta
    diff = (bounds[1] - time) * unit * 10
    score = int(round(base + diff))
  else:
    score = 10
  return score


DEFAULT_PARAMS = ['nested_anchors', 'num_elements=400', 'num_nest=4',
                  'css_selector=%23g-content%20*', 'num_css_rules=1000',
                  'css_text=border%3A%201px%20solid%20%230C0%3B%20padding%3A%208px%3B']


def ConstructTestPageParamCombinations(params, url_type):
  """A list of category,param=val,param2=val2, etc..:
  [u'nested_anchors', u'num_elements=1000', u'num_nest=10',
   u'css_selector=%23g-content%20div', u'num_css_rules=0',
   u'css_text=border%3A%201px%20solid%20%230C0%3B%20padding%3A%208px%3B']
  """
  param_combos = []
  if url_type == 'nested_anchors':
    for num_elements in params['num_elements']:
      for num_nest in params['num_nest']:
        for css_selector in params['css_selector']:
          for num_css_rules in params['num_css_rules']:
            for css_text in params['css_text']:
              params_array = [url_type,
                              'num_elements=%s' % num_elements,
                              'num_nest=%s' % num_nest,
                              'css_selector=%s' % css_selector,
                              'num_css_rules=%s' % num_css_rules,
                              'css_text=%s' % css_text]
              param_combos.append(params_array)

    # def fun(params, params_array):
    #   for i in range(0, len(params) - 1):
    #     for param in params[i]:
    #       params_array[i] = '%s=%s' % (param, params[param][i])


    # for i in range(0, len(params) - 1):
    #   param_combos = fun(params, params_array={})

    # for dict[params.keys()[0]] in params[0]:
    #   for params.keys()[1] in params[1]:
    #     for params.keys()[2] in params[2]:
    #       for params.keys()[3] in params[3]:
    #         for params.keys()[4] in params[4]:
    #           params_array = ['reflow',
    #                           '%s=%s' % (params.keys()[0], num_elements),
    #                           'num_nest=%s' % num_nest,
    #                           'css_selector=%s' % css_selector,
    #                           'num_css_rules=%s' % num_css_rules,
    #                           'css_text=%s' % css_text]
    #           params.append(params_array)


  elif url_type == 'nested_divs' or url_type == 'nested_tables':
    for num_nest in params['num_nest']:
      params_array = [url_type, 'num_nest=%s' % num_nest]
      param_combos.append(params_array)
  return param_combos


def About(request):
  """About page."""
  params = {
    'page_title': 'Reflow Timer - About',
    'server': util.GetServer(request),
    'tests': TESTS,
  }
  return util.Render(request, 'reflow/about.html', params, CATEGORY)


@decorators.provide_csrf
def Test(request):
  page_title = 'Reflow Tests'
  test_key = request.GET.get('t')
  test = None
  if test_key:
    for candidate_test in TESTS:
      if candidate_test.key == test_key:
        test = candidate_test
        page_title += ' %s' % test.label
        break

  params = {
    'page_title': page_title,
    'params': ','.join(DEFAULT_PARAMS),
    'test': test,
    'server': util.GetServer(request),
    'autorun': request.GET.get('autorun'),
    'continue': request.GET.get('continue'),
    'csrf_token': request.session.get('csrf_token')
  }
  params.update(util.ParamsListToDict(DEFAULT_PARAMS))

  return util.Render(request, 'reflow/test.html', params, CATEGORY)


#@cache_page(60*15)
def StatsChart(request):
  x_axis = request.GET.get('x_axis', 'num_nest')
  test_key = request.GET.get('test')
  test = None
  if test_key:
    for candidate_test in TESTS:
      if candidate_test.key == test_key:
        test = candidate_test
        break
  else:
    test = TESTS[0]

  url_type = request.GET.get('url_type', 'nested_anchors')
  if url_type == 'nested_divs' or url_type == 'nested_tables':
    x_axis = 'num_nest'

  params = TEST_PAGES[url_type]['params'].copy()
  logging.info('params %s' % params)

  default_params = util.ParamsListToDict(DEFAULT_PARAMS, unquote=False)

  # seed a params array with less than all the values to construct a graph.
  if url_type == 'nested_anchors':
    for key, val in params.items():
      if val == '':
        continue
      # Uses the last value in our array as the default for the non-X axis
      # unless passed in the url.
      if key != x_axis:
        #param_val = request.GET.get(key, val[len(val) - 1])
        param_val = request.GET.get(key, default_params[key])
        params[key] = [param_val]

  param_combos = ConstructTestPageParamCombinations(params, url_type)
  #logging.info('param_combos: %s' % param_combos)

  stats_charts = []
  for param_combo in param_combos:
    #logging.info('Going to get stats for %s' % location)
    these_params = util.GetStats(request, CATEGORY, output='data',
                                 params=param_combo, opt_tests=[test],
                                 use_memcache=False)
    stats = these_params['stats']
    #logging.info('Stats came back: %s' % stats)
    stats_charts.append(stats)

  params = {
    'x_axis': x_axis,
    'y_axis': 'Reflow Time (ms)',
    'x_labels': params[x_axis],
    'test': test.key,
    'tests': [x.key for x in TESTS],
    'stats_charts': stats_charts,
    'user_agents': stats_charts[0].keys(),
    'param_combos': param_combos,
    'url_type': url_type,
    'test_pages': TEST_PAGES
  }
  return util.Render(request, 'reflow/stats_chart.html', params, CATEGORY)


@decorators.provide_csrf
def NestedAnchors(request):
  css_match_each = request.GET.get('css_match_each', '')
  show_form = int(request.GET.get('show_form', 0))
  params = {
    'csrf_token': request.session.get('csrf_token'),
    'css_match_each': css_match_each,
    'show_form': show_form,
  }
  render_params = ['nested_anchors']
  parsed_params = util.ParamsListToDict(DEFAULT_PARAMS)
  for name, val in parsed_params.items():
    if val == '':
      continue
    value = request.GET.get(name, val)
    params[name] = value
    render_params.append('%s=%s' % (name, urllib2.quote(value)))
  params['params'] = ','.join(render_params)

  return util.Render(request, 'reflow/nested_anchors.html', params, CATEGORY)


@decorators.provide_csrf
def NestedTables(request):
  num_nest = request.GET.get('num_nest', 4)
  render_params = ['nested_tables', 'num_nest=%s' % num_nest]
  params = {
    'csrf_token': request.session.get('csrf_token'),
    'table_layout': request.GET.get('table-layout', 'fixed'),
    'num_nest': num_nest,
    'params': render_params,
    'templates': ['50-50', '33-67', '67-33', '25-75', '75-25']
  }
  return util.Render(request, 'reflow/nested_tables.html', params, CATEGORY)


@decorators.provide_csrf
def NestedDivs(request):
  num_nest = request.GET.get('num_nest', 4)
  render_params = ['nested_divs', 'num_nest=%s' % num_nest]
  params = {
    'csrf_token': request.session.get('csrf_token'),
    'num_nest': num_nest,
    'params': render_params,
    'templates': ['50-50', '33-67', '67-33', '25-75', '75-25']
  }
  return util.Render(request, 'reflow/nested_divs.html', params, CATEGORY)
