#!/usr/bin/python2.4
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

"""
A very simple JSON formatter since the django serializer stuff doesn't serialize
dicts, tuples, or arrays.
"""

__author__ = 'msamuel@google.com (Mike Samuel)'

__all__ = ('to_json',)

import cStringIO
import re

def json_formatter():
  escs = {'"': '\\"', '\\': '\\\\', '\r': '\\r', '\n': '\\n'}
  
  def json_string(s, out):
    out.write('"')
    out.write(re.sub(r'[^\x09\x20\x21\x23-\x5b\x5d-\x7e]',
                     lambda m: (escs.get(m.group(0))
                                or '\\u%04x' % ord(m.group(0)), unicode(s)))
              .encode('UTF-8'))
    out.write('"')

  def json_array(arr, out):
    out.write('[')
    if len(arr):
      json(arr[0], out)
      for el in arr[1:]:
        out.write(',')
        json(el, out)
    out.write(']')

  def json_object(obj, out):
    out.write('{')
    first = True
    for k, v in obj.iteritems():
      if first:
        first = False
      else:
        out.write(',\n')
      json_string(k, out)
      out.write(':')
      json(v, out)
    out.write('}')

  def json_num(n, out):
    out.write(str(n))

  def json_bool(b, out):
    if b:
      out.write('true')
    else:
      out.write('false')

  def json_null(v, out):
    out.write('null')

  handlers = {
    str: json_string,
    unicode: json_string,
    list: json_array,
    tuple: json_array,
    dict: json_object,
    int: json_num,
    long: json_num,
    float: json_num,
    bool: json_bool,
    type: json_null,
    }

  def json(v, out):
    handlers[type(v)](v, out)

  def to_json(v):
    out = cStringIO.StringIO()
    json(v, out)
    return out.getvalue()

  return to_json

to_json = json_formatter()
