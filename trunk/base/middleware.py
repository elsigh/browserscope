# Copyright 2010 Google Inc.
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

__author__ = 'slamm@google.com (Stephen Lamm)'

import logging
import traceback

from google.appengine.api import users
from base import util


class ExceptionMiddleware(object):
  """Log full trackbacks for exceptions."""

  def process_exception(self, request, exception):
    error = traceback.format_exc()
    logging.error('Traceback: %s', error)
    if users.is_current_user_admin():
      return util.Render(request, '500.html', params={'traceback': error})
    else:
      return None
