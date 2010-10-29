## This file exists to try to fix django import issues.

# Declare the Django version we need.
from google.appengine.dist import use_library
use_library('django', '1.1')

# Check that Django 1.0 or higher is in fact loaded.
import django
assert django.VERSION[0] >= 1, "This Django version is too old"

# Initialize Django configuration.
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'  # settings.py must exist etc.
from django.conf import settings
settings._target = None
