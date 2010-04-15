#!/usr/bin/python2.5
#
# Copyright 2008 Google Inc.
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

"""Shared Models Unit Tests."""

__author__ = 'elsigh@google.com (Lindsey Simon)'

import unittest
import logging

from google.appengine.ext import db
from django.test.client import Client
from django import http

import urls
import settings

from base import decorators



class TestDecorators(unittest.TestCase):
  def setUp(self):
    self.client = Client()


  def test_provide_csrf(self):
    params = {
      'return_csrf': 0
    }
    response = self.client.get('/get_csrf', params)
    self.assertEquals(response.content, 'True')


  def test_check_csrf_with_token(self):
    params = {
      'csrf_token': self.client.get('/get_csrf').content
    }
    response = self.client.get('/fake_check_csrf', params)
    self.assertEquals(200, response.status_code)

    # Second time shouldn't work with the same token.
    response = self.client.get('/fake_check_csrf', params)
    self.assertNotEquals(200, response.status_code)


  def test_check_csrf_without_token(self):
    response = self.client.get('/fake_check_csrf')
    self.assertNotEquals(200, response.status_code)
