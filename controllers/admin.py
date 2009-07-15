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

import time

from controllers import all_test_sets
from controllers.shared import decorators
from controllers.shared import util

from models import user_agent

from django import http


def Render(request, template_file, params):
  """Render network test pages."""

  return util.Render(request, template_file, params)

@decorators.provide_csrf
@decorators.admin_required
def Admin(request):
  """Admin Tools"""

  params = {
    'page_title': 'Admin Tools',
  }
  return Render(request, 'admin/admin.html', params)


@decorators.admin_required
def ConfirmUa(request):
  """Confirm User-Agents"""

  search_browser = request.GET.get('browser', '')
  search_user_agent = request.GET.get('useragent', '')
  search_unconfirmed = request.GET.get('unconfirmed', True)
  search_confirmed = request.GET.get('confirmed', False)
  search_changed = request.GET.get('changed', False)

  user_agents = user_agent.UserAgent.all().order('string').fetch(1000)

  # family, v1, v2, v3 = user_agent.UserAgent.parse(string)

  params = {
    'page_title': 'Confirm User-Agents',
    'user_agents': user_agents[:15],
    'search_browser': search_browser,
    'search_user_agent': search_user_agent,
    'search_unconfirmed': search_unconfirmed,
    'search_confirmed': search_confirmed,
    'search_changed': search_changed,
  }
  return Render(request, 'admin/confirm-ua.html', params)


@decorators.admin_required
def Stats(request):
  """Stats"""

  params = {
    'page_title': 'Stats',
  }
  return util.Render(request, 'admin/stats.html', params)
