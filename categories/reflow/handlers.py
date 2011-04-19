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
from categories import test_set_params

# Data structures for reflow testing.
#from bin.reflow.run_reflow_timer import TEST_PAGES

from settings import *


CATEGORY = 'reflow'


def ConstructTestPageParamCombinations(params, url_type):
  """A list of category,param=val,param2=val2, etc..:
  [u'nested_anchors', u'num_elements=1000', u'num_nest=10',
   u'css_selector=%23g-content%20div', u'num_css_rules=0',
   u'css_text=border%3A%201px%20solid%20%230C0%3B%20padding%3A%208px%3B']
  """
  if url_type == 'nested_anchors':
    param_combos = [[[[[
        test_set_params.Params(url_type,
                               'num_elements=%s' % num_elements,
                               'num_nest=%s' % num_nest,
                               'css_selector=%s' % css_selector,
                               'num_css_rules=%s' % num_css_rules,
                               'css_text=%s' % css_text)
        for num_elements in params['num_elements']]
        for num_nest in params['num_nest']]
        for css_selector in params['css_selector']]
        for num_css_rules in params['num_css_rules']]
        for css_text in params['css_text']]
  elif url_type == 'nested_divs' or url_type == 'nested_tables':
    params_combos = [test_set_params.Params(url_type, 'num_nest=%s' % num_nest)
                     for num_nest in params['num_nest']]
  else:
    param_combos = []
  return param_combos


def OldHome(request):
  return http.HttpResponseRedirect('/reflow/about')

def About(request):
  """About page."""
  params = {
    'page_title': 'What are the Reflow Tests?',
    'server': util.GetServer(request),
    'tests': all_test_sets.GetTestSet(CATEGORY).tests,
  }
  return util.Render(request, 'templates/about.html', params, CATEGORY)


@decorators.provide_csrf
def TestAcid1(request):
  page_title = 'Reflow Tests'
  test_key = request.GET.get('t')
  test_set = all_test_sets.GetTestSet(CATEGORY)
  try:
    test = test_set.GetTest(test_key)
  except KeyError:
    test = None

  params = {
    'page_title': page_title,
    'params': test_set_params.Params('acid1', 'num_elements=300'),
    'test': test,
    'server': util.GetServer(request),
    'autorun': request.GET.get('autorun'),
    'continue': request.GET.get('continue'),
    'csrf_token': request.session.get('csrf_token')
  }
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

  default_params=test_set_params.Params(
    'nested_anchors', 'num_elements=400', 'num_nest=4',
    'css_selector=#g-content *', 'num_css_rules=1000',
    'css_text=border: 1px solid #0C0; padding: 8px;')

  params = {
    'page_title': page_title,
    'params': default_params,
    'test': test,
    'server': util.GetServer(request),
    'autorun': request.GET.get('autorun'),
    'continue': request.GET.get('continue'),
    'csrf_token': request.session.get('csrf_token')
  }
  return util.Render(request, 'templates/test.html', params, CATEGORY)


def TestGenCss(request):
  params = test_set_params.Params(
    'gencss', 'css_selector=#g-content div *', 'num_css_rules=1000',
    'css_text=width: auto')
  params_str = request.GET.get('params')
  if params_str:
    params = test_set_params.FromString(params_str)
  css = GenCss(params)
  return http.HttpResponse(css)


def GenCss(params):
  if 'css_match_each' in params:
    css = ['g-%s { %s }' % (params['num_css_rule'], params['css_text'])
           for num_css_rule in range(num_css_rules)]
  else:
    css = ['%s { %s }' % (params['css_selector'], params['css_text'])
           for num_css_rule in range(int(params['num_css_rules']))]
  return ' '.join(css)


@decorators.provide_csrf
def NestedAnchors(request):
  default_params = test_set_params.Params(
     'nested_anchors', 'num_elements=400', 'num_nest=4',
     'css_selector=p', 'num_css_rules=1000',
     'css_text=border:1px solid green;padding: 5px')
  css_match_each = request.GET.get('css_match_each', '')
  show_form = int(request.GET.get('show_form', 0))
  params = {
    'csrf_token': request.session.get('csrf_token'),
    'css_match_each': css_match_each,
    'show_form': show_form,
    'params': default_params,
  }
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
