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

__author__ = 'slamm@google.com (Stephen Lamm)'

from google.appengine.api import datastore
from google.appengine.api import datastore_errors
from google.appengine.api import datastore_types

import score_ranker

class ScoreDatastore(score_ranker.StorageBase):
  def __init__(self, parent_key):
    """Initialize the ScoreDatastore.

    Args:
      parent_key: the parent key of all the node entities.
    """
    self.parent_key = parent_key

  def RunInTransaction(self, func, *args, **kwds):
    """Run the pass function in a transaction.

    Blocks other changes to the storage.

    Args:
      func: a function reference
      args: the positional arguments list
      kwds: the keyword arguments dict
    Raises:
      score_ranker.TransactionFailedError if transaction failed
    """
    return datastore.RunInTransaction(func, *args, **kwds)

  def SetMultiple(self, nodes):
    """Set multiple nodes at once.

    Nodes indexes that do not exist are created.
    Exising nodes are updated.

    Args:
      nodes: {node_index: [child_count_1, ...], ...}
    """
    datastore.Put([self._CreateRankerNodeEntity(node)
                   for node in nodes.items()])

  def Get(self, node_index):
    """Get a single node

    Args:
      node_index: an integer (0 is the root node)
    Returns:
      [child_count_1, ...] or None
    """
    try:
      node_entity = datastore.Get(self._RankerNodeKey(node_index))
    except datastore_errors.EntityNotFoundError:
      return None
    return node_entity["child_counts"]


  def GetMultiple(self, node_indexes):
    """Get multiple nodes at once.

    Args:
      node_indexes: [node index, ...]  # where node_index is an integer
    Returns:
      {node_index_1: [child_count_1, ...], ...}
    """
    node_entities = datastore.Get([self._RankerNodeKey(node_index)
                                   for node_index in node_indexes])
    return dict((node_index, node["child_counts"])
                for node_index, node in zip(node_indexes, node_entities)
                if node)

  def DeleteMultiple(self, node_indexes):
    """Delete multiple nodes at once.

    Args:
      node_indexes: [node index, ...]  # where node_index is an integer
    """
    db_nodes = datastore.Delete([self._RankerNodeKey(node_index)
                                 for node_index in set(node_indexes)])

  def DeleteAll(self):
    query = datastore.Query('ranker_node', keys_only=True)
    query.Ancestor(self.parent_key)
    datastore.Delete(list(query.Run()))

  def _RankerNodeKey(self, node_index):
    """Creates a (named) key for the node with a given id.

    The key will have the ranker as a parent element to guarantee
    uniqueness (in the presence of multiple rankers) and to put all
    nodes in a single entity group.

    Args:
      node_index: The node's id as an integer.

    Returns:
      A (named) key for the node with the id 'node_index'.
    """
    return datastore_types.Key.from_path(
        "ranker_node", "node_%s" % node_index, parent=self.parent_key)

  def _CreateRankerNodeEntity(self, node):
    node_index, child_counts = node
    node_entity = datastore.Entity(
        "ranker_node", parent=self.parent_key,
        name=self._RankerNodeKey(node_index).name())
    node_entity["child_counts"] = child_counts
    return node_entity
