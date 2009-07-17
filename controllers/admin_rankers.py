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
from django.utils import simplejson

def Render(request, template_file, params):
  """Render network test pages."""

  return util.Render(request, template_file, params)


def RebuildRankers(request):
  """Rebuild rankers."""

  params = {
    'page_title': 'Rebuild Rankers',
  }
  return Render(request, 'admin/rebuild_rankers.html', params)


def UpdateResultParents(request):
  is_client_tool = False
  if request.method == 'POST':
    # Request is from client tool (e.g. bin/db_update.py)
    is_client_tool = True
    try:
      bookmark, total_scanned, total_updated = simplejson.loads(
          request.raw_post_data)
    except ValueError:
      bookmark = None
  else:
    bookmark = request.GET.get('bookmark', None)
    total_scanned = request.GET.get('total_scanned', 0)
    total_updated = request.GET.get('total_updated', 0)
  query = pager.PagerQuery(ResultParent)
  try:
    prev_bookmark, results, next_bookmark = query.fetch(100, bookmark)
    total_scanned += len(results)
    changed_results = []
    for result in results:
      if result.user_agent_list:
        result.user_agent_pretty = result.user_agent_list[-1]
        result.user_agent_list = []
        changed_results.append(result)
    if changed_results:
      db.put(changed_results)
      total_updated += len(changed_results)
  except DeadlineExceededError:
    return http.HttpResponse('UpdateResultParent: DeadlineExceededError.',
                             status=403)
  if is_client_tool:
    return http.HttpResponse(
        simplejson.dumps((next_bookmark, total_scanned, total_updated)))
  elif next_bookmark:
    taskqueue.Task(
        method='GET',
        url='/admin/update_result_parents',
        params={
            'bookmark': next_bookmark,
            'total_scanned': total_scanned,
            'total_updated': total_updated,
            }).add()
    return http.HttpResponse('Finished batch. Queued more updates.')
  return http.HttpResponse('Finished batch. No more updates.')
