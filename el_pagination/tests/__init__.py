"""Test model definitions."""

from __future__ import unicode_literals

from django.core.management import call_command


call_command('makemigrations', verbosity=0)
call_command('migrate', verbosity=0)
