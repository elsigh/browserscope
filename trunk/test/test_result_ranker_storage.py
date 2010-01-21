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

"""Result ranker storage Unit Tests."""

__author__ = 'slamm@google.com (Stephen Lamm)'

import unittest
import logging

from google.appengine.api import datastore_types

from models import result_ranker_storage


class ResultRankerStorageTest(unittest.TestCase):
  def testRunInTransactionPassesValueThrough(self):
    parent_key = datastore_types.Key.from_path(
        "result_ranker_storage_test_parent", "trans_pass")
    storage = result_ranker_storage.ScoreDatastore(parent_key)
    storage.SetMultiple({0: [0, 77, 3, 4]})
    self.assertEqual([0, 77, 3, 4], storage.RunInTransaction(storage.Get, 0))

  def testGetReturnsNoneWhenEmpty(self):
    parent_key = datastore_types.Key.from_path(
        "result_ranker_storage_test_parent", "empty_none")
    storage = result_ranker_storage.ScoreDatastore(parent_key)
    self.assertEqual(None, storage.Get(0))

  def testSetAndGet(self):
    parent_key = datastore_types.Key.from_path(
        "result_ranker_storage_test_parent", "set_and_get")
    storage = result_ranker_storage.ScoreDatastore(parent_key)
    storage.SetMultiple({0: [4, 6, 7]})
    self.assertEqual([4, 6, 7], storage.Get(0))

  def testSetMultipleAndGetMultiple(self):
    parent_key = datastore_types.Key.from_path(
        "result_ranker_storage_test_parent", "set_multiple_and_get")
    storage = result_ranker_storage.ScoreDatastore(parent_key)
    scores = {0: [4, 6, 7], 1: [3, 5, 8]}
    storage.SetMultiple(scores)
    self.assertEqual([4, 6, 7], storage.Get(0))
    self.assertEqual([3, 5, 8], storage.Get(1))
    self.assertEqual(scores, storage.GetMultiple([1, 0]))

  def testDeleteMultiple(self):
    parent_key = datastore_types.Key.from_path(
        "result_ranker_storage_test_parent", "delete_multiple")
    storage = result_ranker_storage.ScoreDatastore(parent_key)
    scores = {0: [4, 6, 7], 1: [3, 5, 8], 2: [2, 9, 10]}
    storage.SetMultiple(scores)
    storage.DeleteMultiple([0, 2])
    self.assertEqual({1: [3, 5, 8]}, storage.GetMultiple([0, 1, 2]))

  def testDeleteAll(self):
    parent_key = datastore_types.Key.from_path(
        "result_ranker_storage_test_parent", "delete_all")
    storage = result_ranker_storage.ScoreDatastore(parent_key)
    scores = {0: [11, 12], 1: [22, 23], 2: [33, 34]}
    storage.SetMultiple(scores)
    storage.DeleteAll()
    self.assertEqual({}, storage.GetMultiple([0, 1, 2]))
