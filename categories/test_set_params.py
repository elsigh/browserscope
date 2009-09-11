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

"""Parameters to modify test sets."""

__author__ = 'slamm@google.com (Stephen Lamm)'


import UserDict


class Params(object, UserDict.DictMixin):
  """An immutable, ordered dictionary with a name.

  With Python 2.6, it is recommended to use collections.Mapping instead.
  """

  def __init__(self, name, *args):
    """Initialize Params.

    Args:
      name: a string to identify these params.
      args: a list of ['key_1=value_1', 'key_2=value_2', ...]
    """
    self.name = name
    self._str = None
    pairs = [x.split('=', 1) for x in args]
    self._ordered_keys = [x[0] for x in pairs]
    self._dict = dict(pairs)
    self._str = ','.join(
        x.replace(',', r'\,') for x in [self.name] + list(args))

  @classmethod
  def FromString(cls, params_str):
    temporary_comma = '--tempcomma--'
    params_str.replace(r'\,', temporary_comma)
    name_and_args = params_str.split(',')
    return cls(*[x.replace(temporary_comma, ',') for x in name_and_args])

  def __str__(self):
    return self._str

  def __getitem__(self, key):
    return self._dict[key]

  def keys(self):
    return self._ordered_keys

  def __contains__(self, key):
    return key in self._dict

  def __iter__(self):
    return iter(self._ordered_keys)

  def iteritems(self):
    return iter((x, self._dict[x]) for x in self._ordered_keys)
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

"""Parameters to modify test sets."""

__author__ = 'slamm@google.com (Stephen Lamm)'


import UserDict


class Params(object, UserDict.DictMixin):
  """An immutable, ordered dictionary with a name.

  With Python 2.6, it is recommended to use collections.Mapping instead.
  """

  def __init__(self, name, *args):
    """Initialize Params.

    Args:
      name: a string to identify these params.
      args: a list of ['key_1=value_1', 'key_2=value_2', ...]
    """
    self.name = name
    self._str = None
    pairs = [x.split('=', 1) for x in args]
    self._ordered_keys = [x[0] for x in pairs]
    self._dict = dict(pairs)
    self._str = ','.join(
        x.replace(',', r'\,') for x in [self.name] + list(args))

  @classmethod
  def FromString(cls, params_str):
    temporary_comma = '--tempcomma--'
    params_str.replace(r'\,', temporary_comma)
    name_and_args = params_str.split(',')
    return cls(*[x.replace(temporary_comma, ',') for x in name_and_args])

  def __str__(self):
    return self._str

  def __getitem__(self, key):
    return self._dict[key]

  def keys(self):
    return self._ordered_keys

  def __contains__(self, key):
    return key in self._dict

  def __iter__(self):
    return iter(self._ordered_keys)

  def iteritems(self):
    return iter((x, self._dict[x]) for x in self._ordered_keys)
