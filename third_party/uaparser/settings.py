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

# Django settings for google-app-engine-django project.

import os
import logging
import sys
from google.appengine.api import users


APP_TITLE = 'UA Parser'
APPEND_SLASH = False
ADMINS = (('Drew Stephens', 'drew@dinomite.net'),
          ('Lindsey Simon', 'elsigh@gmail.com'),
          ('Stephen Lamm', 'steve.lamm@gmail.com'))
MANAGERS = ADMINS
SERVER_EMAIL = 'elsigh@gmail.com'
TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
SECRET_KEY = 'uaparserisnawtverysekkrit'
SESSION_COOKIE_NAME = APP_TITLE
TEMPLATE_LOADERS = (
  'django.template.loaders.filesystem.load_template_source',
  'django.template.loaders.app_directories.load_template_source'
)
MIDDLEWARE_CLASSES = (
  'django.middleware.common.CommonMiddleware',
)
TEMPLATE_CONTEXT_PROCESSORS = (
  'django.core.context_processors.debug'
)
ROOT_URLCONF = 'urls'
ROOT_PATH = os.path.dirname(__file__)
TEMPLATE_DIRS = (
  os.path.join(ROOT_PATH, 'templates'),
)
INSTALLED_APPS = (
)

# We toggle DEBUG and TEMPLATE_DEBUG based on APP ENGINE's reported env.
DEBUG = False
BUILD = 'production'
SERVER_SOFTWARE = os.getenv('SERVER_SOFTWARE')
if (users.is_current_user_admin() or
    (SERVER_SOFTWARE is not None and 'Dev' in SERVER_SOFTWARE)):
  BUILD = 'development'
  DEBUG = True
TEMPLATE_DEBUG = DEBUG
