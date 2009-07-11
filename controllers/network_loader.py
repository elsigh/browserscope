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

"""Bulk load network performance tests.

Used to load tests from the pre-GAE UA profiler.

The client is bin/network_uploader.py.
"""

__author__ = 'slamm@google.com (Stephen Lamm)'

import datetime
import logging
import traceback

from django import http
from django.utils import simplejson

from controllers import network
from models.result import *
from models.user_agent import UserAgent

from shared import decorators

from google.appengine.ext import db
from google.appengine.runtime import DeadlineExceededError


def LastLoaderId():
  query = db.GqlQuery('SELECT * FROM ResultParent ORDER BY loader_id DESC')
  results = query.fetch(1)
  if not results:
    return 0
  return results[0].loader_id


@decorators.admin_required
def ResultLoader(request):
  try:
    last_loader_id = LastLoaderId()
    results = [result for result in simplejson.loads(request.raw_post_data)
               if result[0] > last_loader_id]
    logging.info('last_loader_id=%d, num results to add=%d',
                 last_loader_id, len(results))
    for result in results:
      logging.debug("result: %s", result)
      loader_id, ip, user_agent_string, created_timestamp, test_scores = result
      created = datetime.datetime.utcfromtimestamp(created_timestamp)
      ResultParent.AddResult(network.CATEGORY, ip, user_agent_string,
                             test_scores, loader_id=loader_id, created=created)
      last_loader_id = loader_id
  except Exception:
    logging.info('exception: %s', traceback.format_exc())
    return http.HttpResponse('exception: %s' % str(e), mimetype='text/plain')
  return http.HttpResponse(str(last_loader_id), mimetype='text/plain')
