#!/usr/bin/python2.7
#
# Copyright 2009 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Views."""

__author__ = 'elsigh@google.com (Lindsey Simon)'

import logging
import os
import re
import sys
import time
import yaml

from google.appengine.api import memcache
from google.appengine.api import users

import django
from django import http
from django import shortcuts
from django.template import loader, Context
from django.utils import simplejson

from django.template import add_to_builtins
add_to_builtins('tags.custom_filters')

import decorators
import user_agent_parser
import settings


def Render(request, template, params={}):
  """Wrapper function to render templates with global and category vars."""
  params['app_title'] = settings.APP_TITLE
  params['version_id'] = os.environ['CURRENT_VERSION_ID']
  params['build'] = settings.BUILD
  params['epoch'] = int(time.time())
  params['request_path'] = request.get_full_path()
  params['request_path_lastbit'] = re.sub('^.+\/([^\/]+$)', '\\1', request.path)
  params['current_ua_string'] = request.META['HTTP_USER_AGENT']
  params['current_ua'] = user_agent_parser.PrettyUserAgent(params['current_ua_string'])
  params['chromeframe_enabled'] = request.COOKIES.get(
      'browserscope-chromeframe-enabled', '0')
  params['app_categories'] = []
  params['is_admin'] = users.is_current_user_admin()

  current_user = users.get_current_user()
  if current_user:
    params['user_id'] = current_user.user_id()
  else:
    params['user_id'] = None
  params['user'] = current_user

  params['sign_in'] = users.create_login_url(request.get_full_path())
  params['sign_out'] = users.create_logout_url('/')

  return shortcuts.render_to_response(template, params)


def WebParser(request):
  output = request.REQUEST.get('o', 'html')

  parsed = {}
  ua_string = request.REQUEST.get('ua')
  js_user_agent_string = request.REQUEST.get('js_ua')
  js_user_agent_family = request.REQUEST.get('js_user_agent_family')
  js_user_agent_v1 = request.REQUEST.get('js_user_agent_v1')
  js_user_agent_v2 = request.REQUEST.get('js_user_agent_v2')
  js_user_agent_v3 = request.REQUEST.get('js_user_agent_v3')
  logging.info('js_ua "%s"' % js_user_agent_string)
  logging.info('js_user_agent_family "%s"' % js_user_agent_family)
  logging.info('js_user_agent_v1 %s' % js_user_agent_v1)
  logging.info('js_user_agent_v2 %s' % js_user_agent_v2)
  logging.info('js_user_agent_v3 %s' % js_user_agent_v3)
  logging.info('output "%s"' % request.POST if request.method == "POST" else "no post")

  if ua_string:
    ua_parsed = user_agent_parser.ParseUserAgent(ua_string,
        js_user_agent_string=js_user_agent_string,
        js_user_agent_family=js_user_agent_family,
        js_user_agent_v1=js_user_agent_v1,
        js_user_agent_v2=js_user_agent_v2,
        js_user_agent_v3=js_user_agent_v3)
    
    os_parsed = user_agent_parser.ParseOS(ua_string)
    
    parsed['string'] = ua_string
    parsed['prettyUA'] = user_agent_parser.PrettyUserAgent(**ua_parsed)
    parsed['prettyOS'] = user_agent_parser.PrettyOS(**os_parsed)
    parsed.update(os_parsed)
    parsed.update(ua_parsed)

  else:
    ua_string = request.META.get('HTTP_USER_AGENT')


  params = {
    'ua': ua_string,
    'ua_parsed': parsed,
    'js_ua': js_user_agent_string,
    'js_user_agent_family': js_user_agent_family,
    'js_user_agent_v1': js_user_agent_v1,
    'js_user_agent_v2': js_user_agent_v2,
    'js_user_agent_v3': js_user_agent_v3
  }

  # HTML form
  if output == 'html':
    return Render(request, 'user_agent.html', params)
  # JS snippet
  elif output == 'js':
    params = {'mimetype': 'text/javascript'}
    return Render(request, 'user_agent.js', params)
  else:
    raise NotImplementedError

def GetYaml():
  root_dir = os.path.abspath(os.path.dirname(__file__))
  yaml_file = open(root_dir + '/resources/user_agent_parser.yaml')
  yaml_obj = yaml.load(yaml_file)
  yaml_file.close()
  return yaml_obj

def Yaml(request):
  yaml_obj = GetYaml()
  return http.HttpResponse(yaml.dump(yaml_obj))


def Json(request):
  yaml_obj = GetYaml()
  indent = int(request.GET.get('indent', '0'))
  return http.HttpResponse(simplejson.dumps(yaml_obj, indent=indent))


def Feed(request):
  yaml_obj = GetYaml()
  params = {'yaml': yaml_obj['user_agent_parsers']}
  return Render(request, 'atom.xml', params)


def JsOverrideFn(request):
  path = os.path.join(os.path.split(__file__)[0],
                     'resources/user_agent_overrides.js')
  f = open(path, 'r')
  try:
    data = f.read()
  finally:
    f.close()

  return http.HttpResponse(data, 'text/javascript')




