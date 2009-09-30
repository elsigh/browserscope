#!/usr/bin/python2.4
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

"""Handlers administrative tasks.

Confirm new user agents.
- Change their browser designation, if needed.
- Delete tests (e.g. spam).
"""

__author__ = 'slamm@google.com (Stephen Lamm)'

import datetime
import logging
import os
import time

from google.appengine.ext import db

import settings
from categories import all_test_sets
from base import decorators
from base import manage_dirty
from base import util
from models.result import ResultParent
from models.result import ResultTime
from models.user_agent import UserAgent
from models.user_agent import UserAgentGroup

from django import http
from django.utils import simplejson
from third_party.gaefy.db import pager


def Render(request, template_file, params):
  """Render network test pages."""

  return util.Render(request, template_file, params)

@decorators.admin_required
def Admin(request):
  """Admin Tools"""

  params = {
    'page_title': 'Admin Tools',
    'application_id': os.environ['APPLICATION_ID'],
    'current_version_id': os.environ['CURRENT_VERSION_ID'],
    'is_development': settings.BUILD == 'development',
    'is_paused': manage_dirty.UpdateDirtyController.IsPaused(),
  }
  return Render(request, 'admin/admin.html', params)

@decorators.check_csrf
def SubmitChanges(request):
  logging.info('^^^^^^^^^^^^^^^^^^^^ SubmitChanges')
  encoded_ua_keys = [key[3:] for key in request.GET if key.startswith('ac_')]
  logging.info('Encoded ua keys: %s' % ', '.join(encoded_ua_keys))
  update_user_agents = []
  for encoded_key in encoded_ua_keys:
    action = request.REQUEST['ac_%s' % encoded_key]
    ua = db.get(db.Key(encoded=encoded_key))
    if action == 'confirm' and not ua.confirmed:
      ua.confirmed = True
      update_user_agents.append(ua)
    if action == 'unconfirm' and ua.confirmed:
      ua.confirmed = False
      update_user_agents.append(ua)
    if action == 'change' and not ua.changed:
      change_to = request.REQUEST['cht_%s' % key]
      if change_to != ua.pretty():
        #UserAgent.parse_to_string_list(change_to)
        #ua.family =
        pass
  logging.info('Update user agents: %s' % ', '.join([ua.string for ua in update_user_agents]))
  db.put(update_user_agents)
  return http.HttpResponse('Time to go to the next page.')


@decorators.admin_required
@decorators.provide_csrf
def ConfirmUa(request):
  """Confirm User-Agents"""

  search_browser = request.REQUEST.get('browser', '')
  search_unconfirmed = request.REQUEST.get('unconfirmed', True)
  search_confirmed = request.REQUEST.get('confirmed', False)
  search_changed = request.REQUEST.get('changed', False)

  if 'search' in request.REQUEST:
    pass
  elif 'submit' in request.REQUEST:
    return SubmitChanges(request)

  user_agents = UserAgent.all().order('string').fetch(1000)
  user_agents = user_agents[:10]

  for ua in user_agents:
    match_spans = UserAgent.MatchSpans(ua.string)
    ua.match_strings = []
    last_pos = 0
    for start, end in match_spans:
      if start > last_pos:
        ua.match_strings.append((False, ua.string[last_pos:start]))
      ua.match_strings.append((True, ua.string[start:end]))
      last_pos = end
    if len(ua.string) > last_pos:
      ua.match_strings.append((False, ua.string[last_pos:]))

  params = {
    'page_title': 'Confirm User-Agents',
    'user_agents': user_agents,
    'search_browser': search_browser,
    'search_unconfirmed': search_unconfirmed,
    'search_confirmed': search_confirmed,
    'search_changed': search_changed,
    'csrf_token': request.session['csrf_token'],
    'use_parse_service': False,
  }
  return Render(request, 'admin/confirm-ua.html', params)


@decorators.admin_required
def Stats(request):
  """Stats"""

  params = {
    'page_title': 'Stats',
  }
  return util.Render(request, 'admin/stats.html', params)


@decorators.admin_required
def GetUserAgentGroupStrings(request):
  version_level = request.GET.get('v', 'top')
  UserAgentGroup.ClearMemcache(version_level)
  ua_strings = UserAgentGroup.GetStrings(version_level)
  return http.HttpResponse('<br>'.join(ua_strings))

@decorators.admin_required
def WTF(request):
  key = request.GET.get('key')
  dbkey = db.Key(key)
  if not key:
    return http.HttpResponse('No key')
  ua = UserAgent.get(dbkey)
  logging.info('ua: %s' % user_agent)
  if ua:
    ua.update_groups()
    logging.info('DONE WTF!!')
    return http.HttpResponse('Done with UserAgent key=%s' % key)
  else:
    return http.HttpResponse('No user_agent with this key.')

def DataDump(request):
  bookmark = request.GET.get('bookmark')
  created = request.GET.get('created')
  if created:
    created = datetime.datetime.strptime(created, '%Y-%m-%d %H:%M:%S')
  if bookmark and created:
    return http.HttpResponseBadRequest(
        'Both "bookark" and "created" set. Should only set one or neither.')
  fetch_limit = int(request.GET.get('fetch_limit', 100))
  time_limit = int(request.GET.get('time_limit', 3))
  start_time = datetime.datetime.now()
  model = request.GET.get('model') # 'ResultParent', 'UserAgent'

  if model == 'ResultParent':
    query = pager.PagerQuery(ResultParent, keys_only=True)
  elif model == 'UserAgent':
    query = pager.PagerQuery(UserAgent)
  else:
    return http.HttpResponseBadRequest(
        'model must be one of "ResultParent", "UserAgent".')
  if created:
    query.filter('created >=', created)
  query.order('created')
  prev_bookmark, results, next_bookmark = query.fetch(fetch_limit, bookmark)

  if model == 'ResultParent':
    data = []
    result_time_query = ResultTime.gql('WHERE ANCESTOR IS :1')
    last_result_parent_key = None
    for result_parent_key in results:
      if (last_result_parent_key and
          (datetime.datetime.now() - start_time).seconds > time_limit):
        # There is more to process, but we have run out of time.
        next_bookmark = query.get_bookmark(last_result_parent_key)
        break
      last_result_parent_key = result_parent_key
      p = ResultParent.get(result_parent_key)
      data.append({
          'model_class': 'ResultParent',
          'result_parent_key': str(result_parent_key),
          'user_agent_key': str(p.user_agent.key()),
          'ip': p.ip,
          'user_id': p.user and p.user.user_id() or None,
          'created': p.created and p.created.isoformat() or None,
          'params_str': p.params_str,
          'loader_id': hasattr(p, 'loader_id') and p.loader_id or None,
          })
      result_time_query.bind(result_parent_key)
      for result_time in result_time_query.fetch(1000):
        data.append({
            'model_class': 'ResultTime',
            'result_time_key': str(result_time.key()),
            'result_parent_key': str(result_parent_key),
            'test': result_time.test,
            'score': result_time.score,
            })
  elif model == 'UserAgent':
    data = [{
        'user_agent_key': str(ua.key()),
        'string': ua.string,
        'family': ua.family,
        'v1': ua.v1,
        'v2': ua.v2,
        'v3': ua.v3,
        'confirmed': ua.confirmed,
        'created': ua.created and ua.created.isoformat() or None,
        'js_user_agent_string': (hasattr(ua, 'js_user_agent_string') and
                                 ua.js_user_agent_string or None),
        } for ua in results]
  response_params = {
      'bookmark': next_bookmark,
      'fetch_limit': fetch_limit,
      'time_limit': time_limit,
      'data': data,
      'model': model,
      }
  return http.HttpResponse(content=simplejson.dumps(response_params),
                           content_type='application/json')
