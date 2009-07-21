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


APP_TITLE = 'Browserscope'

# TODO(elsigh): Set the default for production to False
DEBUG = True
BUILD = 'production'
if 'Dev' in os.getenv('SERVER_SOFTWARE'):
  BUILD = 'development'
  DEBUG = True

TEMPLATE_DEBUG = DEBUG

# good gawd, why does this default to True?
APPEND_SLASH = False

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)
MANAGERS = ADMINS

DATABASE_ENGINE = 'appengine'  # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = ''             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'whoiscr@zyluiscrazyidunno'

SESSION_COOKIE_NAME = APP_TITLE

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
#   'django.contrib.csrf.middleware.CsrfMiddleware',
#    'django.contrib.auth.middleware.AuthenticationMiddleware',
#    'django.middleware.doc.XViewMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
#    'django.core.context_processors.i18n',
#    'django.core.context_processors.media',  # 0.97 only.
#    'django.core.context_processors.request',
)

ROOT_URLCONF = 'urls'

ROOT_PATH = os.path.dirname(__file__)
TEMPLATE_DIRS = (
    os.path.join(ROOT_PATH, 'templates'),
    os.path.join(ROOT_PATH, 'categories'),
)

INSTALLED_APPS = (
     'appengine_django',
     'django.contrib.sessions',
     'third_party.gaebar',
#    'django.contrib.admin',
#    'django.contrib.auth',
#    'django.contrib.contenttypes',
#    'django.contrib.sites',
)

#
# Gaebar
#

# We have to add our models dir to the sys.path here because Gaebar has its
# own models dir - doh!
GAEBAR_LOCAL_URL = 'http://localhost:8084'
GAEBAR_SECRET_KEY = 'randomsecreyt'
GAEBAR_SERVERS = {
	#u'Deployment': u'http://bowser.openweb.org',
	u'Staging': u'http://ua-profiler.appspot.com',
	u'Local Test': u'http://localhost:8084',
}
GAEBAR_MODELS = (
  (
    # We can do this here because we've added our models dir to sys.path
    'test_time',
    [u'TestTime']
  ),
  #(
  #  'user_agent',
  #  [u'UserAgent']
  #),
  #(
  #  'google_app_engine_ranklist.ranker',
  #  [u'app', u'ranker', u'ranker_node', u'ranker_score']
  #),
)


# UA PROFILER GLOBALS
CATEGORIES = ['network', 'reflow']
#for category in CATEGORIES:
#  TEMPLATE_DIRS.append(os.path.join(ROOT_PATH, '%s/templates' % category))
STATS_MEMCACHE_TIMEOUT = 0
STATS_MEMCACHE_UA_ROW_NS = 'ua_row'
STATS_SCORE_TRUE = 'yes'
STATS_SCORE_FALSE = 'no'
BAD_BEACON_MSG = 'Nein swine.'
