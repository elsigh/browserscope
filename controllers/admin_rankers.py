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

"""Handle administrative tasks for rankers (i.e. median trees)."""

__author__ = 'slamm@google.com (Stephen Lamm)'

import logging
import time

from google.appengine.runtime import DeadlineExceededError
from google.appengine.api.labs import taskqueue
from google.appengine.ext import db

from controllers.shared import decorators
from controllers.shared import util
from gaefy.db import pager
from models.result import ResultParent


import django
from django import http

def Render(request, template_file, params):
  """Render network test pages."""

  return util.Render(request, template_file, params)


@decorators.admin_required
def RebuildRankers(request):
  """Rebuild rankers."""

  params = {
    'page_title': 'Rebuild Rankers',
  }
  return Render(request, 'admin/rebuild_rankers.html', params)


@decorators.admin_required
def UpdateResultParents(request):
  bookmark = request.GET.get('bookmark', None)
  total = request.GET.get('total', 0)

  query = pager.PagerQuery(ResultParent)
  try:
    prev_bookmark, results, next_bookmark = query.fetch(1000, bookmark)
    changed_results = []
    for result in results:
      if result.user_agent_list:
        result.user_agent_pretty = result.user_agent_list[-1]
        result.user_agent_list = []
        changed_results.append(result)
    if changed_results:
      logging.info('Update ResultParent user_agent_list -> user_agent_pretty: count = %s', len(changed_results))
      db.put(changed_results)
  except DeadlineExceededError:
    logging.warn('Update ResultParent user_agent_list -> user_agent_pretty: DeadlineExceededError')
    # retry with fewer?
    return http.HttpResponse('UpdateResultParent: timed-out.', status=403)
  if next_bookmark:
    taskqueue.Task(method='GET', url='/admin/update_result_parent',
                   params={'bookmark': next_bookmark,
                           'total': total}).add(update-dirty)
  else:
    logging.info('Update ResultParent user_agent_list -> user_agent_pretty: total processed: %s', total)
  return http.HttpResponse('UpdateResultParent: chunk complete.')
