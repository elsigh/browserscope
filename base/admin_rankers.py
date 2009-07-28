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

"""Handle administrative tasks for rankers (i.e. median trees)."""

__author__ = 'slamm@google.com (Stephen Lamm)'

import logging
import time

from google.appengine.runtime import DeadlineExceededError
from google.appengine.api.labs import taskqueue
from google.appengine.ext import db

from base import decorators
from base import util
from models.result import ResultParent

from third_party.gaefy.db import pager

import django
from django import http
from django.utils import simplejson


def AllRankers(request):
  pass

def AllUserAgents(request):
  pass


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
  bookmark = request.GET.get('bookmark', None)
  total_scanned = int(request.GET.get('total_scanned', 0))
  total_updated = int(request.GET.get('total_updated', 0))
  use_taskqueue = request.GET.get('use_taskqueue', '') == '1'

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
    logging.warn('DeadlineExceededError in UpdateResultParents:'
                 ' total_scanned=%s, total_updated=%s.',
                 total_scanned, total_updated)
    return http.HttpResponse('UpdateResultParent: DeadlineExceededError.',
                             status=403)
  if use_taskqueue:
    if next_bookmark:
      taskqueue.Task(
          method='GET',
          url='/admin/update_result_parents',
          params={
              'bookmark': next_bookmark,
              'total_scanned': total_scanned,
              'total_updated': total_updated,
              'use_taskqueue': 1,
              }).add(queue_name='default')
    else:
      logging.info('Finished UpdateResultParents tasks:'
                   ' total_scanned=%s, total_updated=%s',
                   total_scanned, total_updated)
      return http.HttpResponse(
        simplejson.dumps((next_bookmark, total_scanned, total_updated)))
    return http.HttpResponse('Finished batch. Queued more updates.')
  return http.HttpResponse('Finished batch. No more updates.')
