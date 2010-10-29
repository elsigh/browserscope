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

'''Bootstrap for running a Django app under Google App Engine.

Alot of this is copied from Guido's Rietveld app.
'''

import logging
import os
import sys

# Google App Engine imports.
from google.appengine.ext.webapp import util

# Log a message each time this module get loaded.
logging.info('Loading %s, app version = %s',
             __name__, os.getenv('CURRENT_VERSION_ID'))

# Loads the "right" version of django
import appengine_config

import logging
import django.core.handlers.wsgi
import django.core.signals
import django.db
import django.dispatch.dispatcher

# Moving this to main.py to try to prevent weird exceptions in prod.
from django.template import add_to_builtins
add_to_builtins('base.custom_filters')

def log_exception(*args, **kwds):
  """Django signal handler to log an exception."""
  cls, err = sys.exc_info()[:2]
  logging.exception('Exception in request: %s: %s', cls.__name__, err)


# Log all exceptions detected by Django.
django.core.signals.got_request_exception.connect(log_exception)

# Unregister Django's default rollback event handler.
django.core.signals.got_request_exception.disconnect(
    django.db._rollback_on_exception)


def main():
  # Create a Django application for WSGI.
  application = django.core.handlers.wsgi.WSGIHandler()

  # Run the WSGI CGI handler with that application.
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()