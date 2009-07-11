#!/usr/bin/python2.4
#
# Copyright 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the 'License')
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
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

from controllers.reflow import *

class ReflowTest(unittest.TestCase):

  #def setUp(self):
    # Every test needs a client.
    #self.client = Client()

  def test_CustomTestsFunction(self):
    display, score = CustomTestsFunction('testGetOffsetHeight', 0)
    self.assertEqual('0.0', display)
    self.assertEqual(0, score)

    display, score = CustomTestsFunction('testDisplay', 475)
    self.assertEqual('0.5', display)
    self.assertEqual(80, score)

    display, score = CustomTestsFunction('testDisplay', 1203)
    self.assertEqual('1.2', display)
    self.assertEqual(66, score)

if __name__ == '__main__':
  unittest.main()

