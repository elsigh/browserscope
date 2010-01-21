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

class Mapper(object):
  """For remote_api calls.
  See http://code.google.com/appengine/articles/remote_api.html for examples.
  """
  # Subclasses should replace this with a model class (eg, model.Person).
  KIND = None

  # Subclasses can replace this with a list of (property, value) tuples to filter by.
  FILTERS = []

  def map(self, entity):
    """Updates a single entity.

    Implementers should return a tuple containing two iterables (to_update, to_delete).
    """
    return ([], [])

  def get_query(self):
    """Returns a query over the specified kind, with any appropriate filters applied."""
    q = self.KIND.all()
    for prop, value in self.FILTERS:
      q.filter("%s =" % prop, value)
    q.order("__key__")
    return q

  def run(self, batch_size=100):
    """Executes the map procedure over all matching entities."""
    q = self.get_query()
    entities = q.fetch(batch_size)
    while entities:
      to_put = []
      to_delete = []
      for entity in entities:
        map_updates, map_deletes = self.map(entity)
        to_put.extend(map_updates)
        to_delete.extend(map_deletes)
      if to_put:
        db.put(to_put)
      if to_delete:
        db.delete(to_delete)
      q = self.get_query()
      q.filter("__key__ >", entities[-1].key())
      entities = q.fetch(batch_size)
