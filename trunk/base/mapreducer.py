#!/usr/bin/python2.5
#
# Copyright 2009 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Mapreduce handlers and functions."""

__author__ = 'elsigh@google.com (Lindsey Simon)'


from base import shardedcounter
from mapreduce import operation as op
from google.appengine.ext import db


def ResultParentCountSet(entity):
  shardedcounter.increment(entity.category)


def TestCountSet(entity):
  entity.beacon_count = int(
      shardedcounter.get_count(entity.get_memcache_keyname()))
  yield op.db.Put(entity)


def ResultParentUaDeNorm(entity):
  try:
    ua = entity.user_agent
  except db.ReferencePropertyResolveError:
    yield op.db.Delete(entity)
  if (not entity.category or not entity.user_agent or
      (entity.category == 'reflow' and entity.params_str)):
    yield op.db.Delete(entity)
  else:
    entity.user_agent_string_list = entity.user_agent.get_string_list()
    for attr in ['user_agent_family', 'user_agent_v1', 'user_agent_v2',
                 'user_agent_v3']:
      if hasattr(entity, attr):
        delattr(entity, attr)
    yield op.db.Put(entity)

