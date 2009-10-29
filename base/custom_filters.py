# Copyright 2009 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
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
#

__author__ = 'elsigh@google.com (Lindsey Simon)'

import logging
import os
import datetime
from datetime import timedelta
import re
import urllib2

from django import template
register = template.Library()

import settings

@register.filter
def by_key(array, key):
  try:
    value = array[key]
  except IndexError:
    value = ''
  except TypeError:
    value = ''
  except KeyError:
    value = ''
  return value


@register.filter
def is_in(value, array):
  return value in array


@register.filter
def less_than(value1, value2):
  logging.info('%s less than %s = %s' % (value1, value2, value1 < value2))
  return value1 < value2


@register.filter
def greater_than(value1, value2):
  logging.info('%s greater than %s = %s' % (value1, value2, value1 > value2))
  return value1 > value2


@register.filter
def urlquote(url):
  return urllib2.quote(url)


@register.filter
def urlunquote(url):
  return urllib2.unquote(url)


@register.filter
def resource_path(resource, category=None):
  if category:
    path = '/%s/static/%s' % (category, resource)
  else:
    path = '/static/%s' % resource

  # Add on a version bit so we can use far future expires.
  # In dev mode add random bits to prevent annoying, cough, browsers from
  # caching stuff in frames.
  version = get_resource_version()

  path += '?v=%s' % version

  return path


def get_resource_version():
  if settings.BUILD == 'development':
    version = str(datetime.datetime.now())
  else:
    version = os.environ['CURRENT_VERSION_ID']
  return version


@register.filter
def as_range(end_range):
  end_range = int(end_range)
  return range(1, end_range + 1)


@register.filter
def utc_to_pst(utc_dt):
  return utc_dt - timedelta(hours=7)
