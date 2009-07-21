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

from django import http

# Shared stuff
from base import decorators
from base import util
from categories import all_test_sets

# Data structures for reflow testing.
from bin.reflow.run_reflow_timer import TEST_PAGES

from settings import *


CATEGORY = 'reflow'


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
    'tests': all_test_sets.GetTestSet(CATEGORY).tests,
  }
  return util.Render(request, 'templates/about.html', params, CATEGORY)


@decorators.provide_csrf
def Test(request):
  page_title = 'Reflow Tests'
  test_key = request.GET.get('t')
  test_set = all_test_sets.GetTestSet(CATEGORY)
  try:
    test = test_set.GetTest(test_key)
    page_title += ' %s' % test.name
  except KeyError:
    test = None

  params = {
    'page_title': page_title,
    'params': ','.join(test_set.default_params),
    'test': test,
    'server': util.GetServer(request),
    'autorun': request.GET.get('autorun'),
    'continue': request.GET.get('continue'),
    'csrf_token': request.session.get('csrf_token')
  }
  params.update(util.ParamsListToDict(test_set.default_params))

  return util.Render(request, 'templates/acid1.html', params, CATEGORY)


def TestSelectors(request):
  page_title = 'Reflow CSS Selector Tests'
  test_key = request.GET.get('t')
  test_set = all_test_sets.GetTestSet(CATEGORY)
  try:
    test = test_set.GetTest(test_key)
    page_title += ' %s' % test.name
  except KeyError:
    test = None

  default_params=[
    'nested_anchors', 'num_elements=400', 'num_nest=4',
    'css_selector=%23g-content%20*', 'num_css_rules=1000',
    'css_text=border%3A%201px%20solid%20%230C0%3B%20padding%3A%208px%3B']

  params = {
    'page_title': page_title,
    'params': ','.join(default_params),
    'test': test,
    'server': util.GetServer(request),
    'autorun': request.GET.get('autorun'),
    'continue': request.GET.get('continue'),
    'csrf_token': request.session.get('csrf_token')
  }
  params.update(util.ParamsListToDict(default_params))

  return util.Render(request, 'templates/test.html', params, CATEGORY)


def TestGenCss(request):

  default_params=[
    'css_selector=%23g-content%20div%20*', 'num_css_rules=1000',
    'css_text=width%3A%20auto']
  params = request.GET.get('params', default_params)
  css = GenCss(params)
  return http.HttpResponse(css)


def GenCss(params):
  css = []
  params = util.ParamsListToDict(params)
  if params.has_key('css_match_each'):
    for num_css_rule in range(num_css_rules):
      css.append('g-%s { %s }' % (params['num_css_rule'], params['css_text']))
  else:
    for num_css_rule in range(int(params['num_css_rules'])):
      css.append('%s { %s }' % (params['css_selector'], params['css_text']))
  return ' '.join(css)


#@cache_page(60*15)
def StatsChart(request):
  x_axis = request.GET.get('x_axis', 'num_nest')
  test_key = request.GET.get('test')
  test_set = all_test_sets.GetTestSet(CATEGORY)
  try:
    test = test_set.GetTest(test_key)
  except KeyError:
    test = test_set.tests[0]

  url_type = request.GET.get('url_type', 'nested_anchors')
  if url_type == 'nested_divs' or url_type == 'nested_tables':
    x_axis = 'num_nest'

  params = TEST_PAGES[url_type]['params'].copy()
  logging.info('params %s' % params)

  default_params = util.ParamsListToDict(test_set.default_params, unquote=False)

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
    'tests': [x.key for x in test_set.tests],
    'stats_charts': stats_charts,
    'user_agents': stats_charts[0].keys(),
    'param_combos': param_combos,
    'url_type': url_type,
    'test_pages': TEST_PAGES
  }
  return util.Render(request, 'templates/stats_chart.html', params, CATEGORY)


@decorators.provide_csrf
def NestedAnchors(request):
  default_params=[
     'nested_anchors', 'num_elements=400', 'num_nest=0',
     'css_selector=p', 'num_css_rules=1',
     'css_text=float:left;height:100px;width:100px;border:1px solid red;margin-right:5px;']
  css_match_each = request.GET.get('css_match_each', '')
  show_form = int(request.GET.get('show_form', 0))
  params = {
    'csrf_token': request.session.get('csrf_token'),
    'css_match_each': css_match_each,
    'show_form': show_form
  }
  render_params = ['nested_anchors']
  test_set = all_test_sets.GetTestSet(CATEGORY)
  parsed_params = util.ParamsListToDict(default_params)
  for name, val in parsed_params.items():
    if val == '':
      continue
    value = request.GET.get(name, val)
    params[name] = value
    render_params.append('%s=%s' % (name, urllib2.quote(value)))
  params['params'] = ','.join(render_params)

  return util.Render(request, 'templates/nested_anchors.html', params, CATEGORY)


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
  return util.Render(request, 'templates/nested_tables.html', params, CATEGORY)


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
  return util.Render(request, 'templates/nested_divs.html', params, CATEGORY)
