#!/usr/bin/python2.5
#
# Copyright 2010 Google Inc.
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

"""Test helpers. See test/test_gaeunit.py for actual tests."""

import logging

from google.appengine.ext import db

import django
from django import http


class TaskTrace(db.Model):
  KEY_NAME = 'task_trace'

  method = db.StringProperty()
  encoding = db.StringProperty()
  param = db.StringProperty()


def TaskHandler(request):
  param = None
  if request.method == 'GET':
    param = request.GET.get('the_get_param')
  elif request.method == 'POST':
    param = request.POST.get('the_post_param')
  task_trace = TaskTrace(key_name=TaskTrace.KEY_NAME)
  task_trace.method = request.method
  task_trace.encoding = request.encoding
  task_trace.param = param
  task_trace.put()
  return http.HttpResponse('Saved Task Details')
