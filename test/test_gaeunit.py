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

"""Unit Test Unit Tests. See gaeunit_test.py for helpers."""

__author__ = 'slamm@google.com (Stephen Lamm)'

import unittest
import logging

from google.appengine.ext import db
from google.appengine.api.labs import taskqueue

from gaeunit_test import TaskTrace

class TestTaskQueue(unittest.TestCase):
  """Make sure the mocked taskqueue executes tasks.

  Tasks should execute immediately.
  """
  URL = '/admin/test_task_queue'

  def testGet(self):
    params = {'the_get_param': 'fooey'}
    taskqueue.Task(method='GET', url=self.URL, params=params).add()
    task_trace = TaskTrace.get_by_key_name(TaskTrace.KEY_NAME)
    self.assertNotEqual(None, task_trace)
    self.assertEqual('GET', task_trace.method)

  def testPost(self):
    params = {'the_post_param': 'fooey'}
    taskqueue.Task(method='POST', url=self.URL, params=params).add()
    task_trace = TaskTrace.get_by_key_name(TaskTrace.KEY_NAME)
    self.assertNotEqual(None, task_trace)
    self.assertEqual('POST', task_trace.method)
