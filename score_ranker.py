#!/usr/bin/python2.5
# Copyright 2009 Google Inc.
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
#
# Author slamm@google.com (Stephen Lamm)

import math


def GetShallowBranchingFactor(min_value, max_value, max_branching_factor=100):
  """Compute the branching factor that gives the most shallow tree.

  Using max_branching_factor would give a tree of minimal depth. However, that
  may waste space. This function computes the branching factor that gives the
  same depth with the least waste.

  Args:
    min_value: an integer
    max_value: an integer
    max_branching_factor: an integer that is the maximum children per node.
  Returns:
    an integer branching factor
  """
  num_scores = max_value - min_value + 1
  num_levels = int(math.ceil(
      math.log(num_scores) / math.log(max_branching_factor)))
  return int(math.ceil(10 ** (math.log(num_scores, 10) / num_levels)))


class Ranker(object):
  def __init__(self, storage, min_value, max_value, branching_factor):
    self.storage = storage
    self.min_value = min_value
    self.branching_factor = branching_factor
    num_scores = max_value - min_value + 1
    num_levels = int(math.ceil(
        math.log(num_scores) / math.log(branching_factor)))
    capacity = branching_factor ** num_levels
    self.level_branch_units = [capacity // branching_factor ** (level + 1)
                               for level in range(num_levels)]

  def Add(self, score):
    self.Update([score])

  def Update(self, scores):
    update_tree = self._BuildUpdateTree(scores, is_add=True)
    self.storage.RunInTransaction(self._SaveUpdates, update_tree)

  def Remove(self, score):
    self.RemoveMultiple([score])

  def RemoveMultiple(self, scores):
    update_tree = self._BuildUpdateTree(scores, is_add=False)
    self.storage.RunInTransaction(self._SaveUpdates, update_tree)

  def FindScore(self, rank):
    return self.FindScoreAndNumScores(rank=rank)[0]

  def FindScoreAndNumScores(self, rank=None, percentile=None):
    """Find by either rank or percentile."""
    def _FindScore(rank):
      node_index = 0
      score = self.min_value
      rank_index = 0
      num_scores = None
      for branch_units in self.level_branch_units:
        child_counts = self.storage.Get(node_index)
        if not child_counts:
          break
        if num_scores is None:
          num_scores = sum(child_counts)
          if rank is None:
            rank = int(num_scores * percentile / 100.0)
        for branch_index, count in enumerate(child_counts):
          if rank_index + count > rank:
            node_index = node_index * self.branching_factor + branch_index + 1
            score += branch_units * branch_index
            break
          rank_index += count
      if num_scores is None:
        num_scores = 0
        score = None
      return score, num_scores
    return self.storage.RunInTransaction(_FindScore, rank)

  def TotalRankedScores(self):
    return sum(self.storage.Get(0) or [])

  def _BuildUpdateTree(self, scores, is_add):
    update_tree = {}
    update_scores = {}
    for score in scores:
      update_scores[score] = update_scores.get(score, 0) + 1
    for score in update_scores:
      for node_index, branch_index in self._FindNodes(score):
        child_counts = update_tree.setdefault(
            node_index, [0] * self.branching_factor)
        if is_add:
          child_counts[branch_index] += update_scores[score]
        else:
          child_counts[branch_index] -= update_scores[score]
    return update_tree

  def _SaveUpdates(self, update_tree):
    existing_tree = self.storage.GetMultiple(update_tree.keys())
    unneeded_node_indexes = []
    # Combine the two trees
    for node_index, child_counts in update_tree.items():
      if node_index in existing_tree:
        updated_counts = [
            x + y for x, y in zip(child_counts, existing_tree[node_index])]
        if sum(updated_counts) > 0:
          update_tree[node_index] = updated_counts
        else:
          del update_tree[node_index]
          unneeded_node_indexes.append(node_index)
    if update_tree:
      self.storage.SetMultiple(update_tree)
    if unneeded_node_indexes:
      self.storage.DeleteMultiple(unneeded_node_indexes)

  def _FindNodes(self, score):
    nodes = []
    node_index = 0
    normalized_score = score - self.min_value
    for branch_units in self.level_branch_units:
      branch_index = normalized_score // branch_units
      nodes.append((node_index, branch_index))

      normalized_score -= branch_units * branch_index
      node_index = node_index * self.branching_factor + branch_index + 1
    return nodes


class StorageBase(object):
  """Expected interfact for Ranker storage implementations."""

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
    raise NotImplemented

  def SetMultiple(self, nodes):
    """Set multiple nodes at once.

    Nodes indexes that do not exist are created.
    Exising nodes are updated.

    Args:
      nodes: {node_index: [child_count_1, ...]}
    """
    raise NotImplemented

  def Get(self, node_index):
    """Get a single node

    Args:
      node_index: an integer (0 is the root node)
    Returns:
      [child_count_1, ...] or None
    """
    raise NotImplemented

  def GetMultiple(self, node_indexes):
    """Get multiple nodes at once.

    Args:
      node_indexes: [node index, ...]  # where node_index is an integer
    Returns:
      {node_index_1: [child_count_1, ...], ...}
    """
    raise NotImplemented

  def DeleteMultiple(self, node_indexes):
    """Delete multiple nodes at once.

    Args:
      node_indexes: [node index, ...]  # where node_index is an integer
    """
    raise NotImplemented
