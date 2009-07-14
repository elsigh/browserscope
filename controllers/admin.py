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

from django import http


def Render(request, template_file, params):
  """Render network test pages."""

  return util.Render(request, template_file, params)

@decorators.admin_required
def Admin(request):
  """Network Performance Admin Tools"""

  params = {
    'page_title': 'Performance Admin Tools',
  }
  return Render(request, 'admin/admin.html', params)


@decorators.admin_required
def ConfirmUa(request):
  """Network Performance Confirm User-Agents"""

  params = {
    'page_title': 'Performance Confirm User-Agents',
  }
  return Render(request, 'admin/confirm-ua.html', params)


@decorators.admin_required
def Stats(request):
  """Network Performance Stats"""

  params = {
    'page_title': 'Performance Stats',
  }
  return util.Render(request, 'admin/stats.html', params)
