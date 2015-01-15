#!/usr/bin/python2.4
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

"""Shared decorators."""

__author__ = 'elsigh@google.com (Lindsey Simon)'

import logging
import random

from google.appengine.api import users

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.utils.hashcompat import md5_constructor

from settings import *


def admin_required(func):
  """Tests to make sure the current user is an admin."""
  def _wrapper(request, *args, **kw):
    user = users.get_current_user()
    if user:
      if users.is_current_user_admin():
        return func(request, *args, **kw)
      else:
        return HttpResponse('You need to be an admin. <a href="%s">login</a>.'
                            % users.create_login_url(request.get_full_path()))
    else:
      return HttpResponseRedirect(
          users.create_login_url(request.get_full_path()))
  return _wrapper


# TRUSTED_TESTERS = ['elsigh', 'stevesoudersorg', 'steve.lamm', 'annie.sullivan',
#                    'jeresig', 'kellegous', 'mnotting', 'storey.david',
#                    'test@example.com']
# def trusted_tester_required(func):
#   """Tests to make sure the current user is an admin."""
#   def _wrapper(request, *args, **kw):
#     user = users.get_current_user()
#     logging.info('User: %s' % user.user_id())
#     if user and user in TRUSTED_TESTERS:
#       return func(request, *args, **kw)
#     else:
#       return HttpResponse('You need to be logged in. <a href="%s">login</a>.'
#                           % users.create_login_url(request.get_full_path()))
#   return _wrapper


def dev_appserver_only(func):
  def _wrapper(request, *args, **kw):
    if BUILD == 'production':
      return HttpResponse('Only for dev_appserver eyes.')
    return func(request, *args, **kw)
  return _wrapper


_MAX_CSRF_KEY = 18446744073709551616L
def _make_csrf_key():
  # Use the system (hardware-based) random number generator if it exists.
  if hasattr(random, 'SystemRandom'):
    randrange = random.SystemRandom().randrange
  else:
 	  randrange = random.randrange
  csrf_key = md5_constructor('%s%s' % (randrange(0, _MAX_CSRF_KEY),
                                       SECRET_KEY)
                            ).hexdigest()
  return csrf_key


def provide_csrf(func):
  """Inserts a csrf_token into request.session's list of valid tokens."""
  def _wrapper(request, *args, **kw):
    csrf_token = _make_csrf_key()
    try:
      request.session['csrf_tokens'].append(csrf_token)
    except:
      request.session['csrf_tokens'] = [csrf_token]

    # Expose a single token for session handlers.
    request.session['csrf_token'] = csrf_token

    return func(request, *args, **kw)
  return _wrapper


def check_csrf(func):
  """Checks/removes a csrf_token from request.session's list of valid tokens."""
  def _wrapper(request, *args, **kw):
    valid_csrf_tokens = request.session.get('csrf_tokens')
    request_csrf_token = request.REQUEST.get('csrf_token')

    # Special easter-egg to get around the csrf token.
    # Because most malintents don't really read code.
    if request.GET.get('csrf_override') == 'elsigh':
      return func(request, *args, **kw)

    if request_csrf_token is None:
      return HttpResponseForbidden('CSRF Error - Need csrf_token in request.')
    if request_csrf_token not in valid_csrf_tokens:
      return HttpResponseForbidden('CSRF Error - Invalid csrf_token.')

    request.session['csrf_token'] = None
    request.session['csrf_tokens'].remove(request_csrf_token)

    return func(request, *args, **kw)
  return _wrapper

