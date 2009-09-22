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

import logging
import os
import time

from google.appengine.ext import db

import settings
from categories import all_test_sets
from base import decorators
from base import manage_dirty
from base import util
from models import user_agent

from django import http


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

  user_agents = user_agent.UserAgent.all().order('string').fetch(1000)
  user_agents = user_agents[:10]

  for ua in user_agents:
    match_spans = user_agent.UserAgent.MatchSpans(ua.string)
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
  user_agent.UserAgentGroup.ClearMemcache(version_level)
  ua_strings = user_agent.UserAgentGroup.GetStrings(version_level)
  return http.HttpResponse('<br>'.join(ua_strings))

@decorators.admin_required
def WTF(request):
  key = request.GET.get('key')
  dbkey = db.Key(key)
  if not key:
    return http.HttpResponse('No key')
  ua = user_agent.UserAgent.get(dbkey)
  logging.info('ua: %s' % user_agent)
  if ua:
    ua.update_groups()
    logging.info('DONE WTF!!')
    return http.HttpResponse('Done with UserAgent key=%s' % key)
  else:
    return http.HttpResponse('No user_agent with this key.')
