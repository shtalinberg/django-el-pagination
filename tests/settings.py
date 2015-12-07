"""Settings file for the Django project used for tests."""

import os

from django import VERSION
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS


PROJECT_NAME = 'project'

# Base paths.
ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT = os.path.join(ROOT, PROJECT_NAME)

# Django configuration.
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3'}}
DEBUG = TEMPLATE_DEBUG = True
INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'el_pagination',
    PROJECT_NAME,
)
LANGUAGE_CODE = os.getenv('EL_PAGINATION_LANGUAGE_CODE', 'en-us')
ROOT_URLCONF = PROJECT_NAME + '.urls'
SECRET_KEY = os.getenv('EL_PAGINATION_SECRET_KEY', 'secret')
SITE_ID = 1
STATIC_ROOT = os.path.join(PROJECT, 'static')
STATIC_URL = '/static/'
TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
    PROJECT_NAME + '.context_processors.navbar',
    PROJECT_NAME + '.context_processors.versions',
)


if VERSION >= (1, 8):
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(PROJECT, 'templates'),],
            'APP_DIRS': True,
            'OPTIONS': {
                # ... some options here ...
            },
        },
    ]
else:
    TEMPLATE_DIRS = os.path.join(PROJECT, 'templates')

# Testing.
NOSE_ARGS = (
    '--verbosity=2',
    '--with-coverage',
    '--cover-package=el_pagination',
)
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
