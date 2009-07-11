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

The site-specific code is all in other files: settings.py, urls.py,
models.py, views.py.  And in fact, only 'settings' is referenced here
directly -- everything else is controlled from there.

'''

import os
import sys
import logging

from appengine_django import InstallAppengineHelperForDjango
from appengine_django import have_django_zip
from appengine_django import django_zip_path
InstallAppengineHelperForDjango()

# Google App Engine imports.
from google.appengine.ext.webapp import util

# Import the part of Django that we use here.
import django.core.handlers.wsgi

def profile_main():
  # Wrap the main function for profiling
  import cProfile, pstats
  prof = cProfile.Profile()
  prof = prof.runctx('main()', globals(), locals())
  print '<pre>'
  stats = pstats.Stats(prof)
  stats.sort_stats('time')  # Or cumulative
  stats.print_stats(80)  # 80 = how many to print
  # The rest is optional.
  # stats.print_callees()
  # stats.print_callers()
  print '</pre>'

def main():
  # Ensure the Django zipfile is in the path if required.
  if have_django_zip and django_zip_path not in sys.path:
    sys.path.insert(1, django_zip_path)

  # Create a Django application for WSGI.
  application = django.core.handlers.wsgi.WSGIHandler()

  # Run the WSGI CGI handler with that application.
  util.run_wsgi_app(application)


if __name__ == '__main__':
  use_profiler = False
  if use_profiler:
    profile_main()
  else:
    main()
