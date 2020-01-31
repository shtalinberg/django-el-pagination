# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import sys

"""Settings file for the Django project used for tests."""


DEBUG = True
ALLOWED_HOSTS = ['*']
# Disable 1.9 arguments '--parallel' and try exclude  “Address already in use” at “setUpClass”
os.environ['DJANGO_TEST_PROCESSES'] = "1"
os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = "localhost:8000-8010,8080,9200-9300"

PROJECT_NAME = 'project'

# Base paths.
ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT = os.path.join(ROOT, PROJECT_NAME)

# Django configuration.
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3'}}

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'el_pagination',
    'nose',
    'django_nose',
    PROJECT_NAME,
)
gettext = lambda s: s

LANGUAGES = (('en', gettext('English')),)
LANGUAGE_CODE = os.getenv('EL_PAGINATION_LANGUAGE_CODE', 'en')
ROOT_URLCONF = PROJECT_NAME + '.urls'
SECRET_KEY = os.getenv('EL_PAGINATION_SECRET_KEY', 'secret')
SITE_ID = 1
STATIC_ROOT = os.path.join(PROJECT, 'static')
STATIC_URL = '/static/'


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                PROJECT_NAME + '.context_processors.navbar',
                PROJECT_NAME + '.context_processors.versions',
            ],
        },

    },
]

MIDDLEWARE = (
    'django.middleware.common.CommonMiddleware',
)

# Testing.
NOSE_ARGS = (
    '--verbosity=1',
    '--stop',
    '-s',  # Don't capture stdout (any stdout output will be printed immediately) [NOSE_NOCAPTURE]
    # '--nomigrations',
    # '--with-coverage',
    # '--cover-branches',
    # '--cover-package=el_pagination',
)
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

try:
    from settings_local import *  # noqa
    INSTALLED_APPS = INSTALLED_APPS + INSTALLED_APPS_LOCAL  # noqa
except ImportError:
    sys.stderr.write('settings_local.py not loaded\n')

TEMPLATES[0]['OPTIONS']['debug'] = DEBUG
