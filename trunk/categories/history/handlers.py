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

"""Handlers for History Tests.

Example beacon request:
  http://localhost:8080/beacon?category=History&results=latency=123,hostconn=6,
     maxconn=29,parscript=0,parsheet=1,parcssjs=0,cacheexp=1,cacheredir=0,
     cacheresredir=0,prefetch=1,gzip=1,du=1
"""

__author__ = 'kyle.scholz@gmail.com (Kyle Scholz)'

import re

from categories import all_test_sets
from base import decorators
from base import util

from django import http
from django import shortcuts
	
CATEGORY = 'History'

TEST_PAGE = '/%s/frameset' % CATEGORY
