"""Test model definitions."""

from __future__ import unicode_literals

from django.core.management import call_command
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


def make_model_instances(number):
    """Make a ``number`` of test model instances and return a queryset."""
    for _ in range(number):
        TestModel.objects.create()
    return TestModel.objects.all()


@python_2_unicode_compatible
class TestModel(models.Model):
    """A model used in tests."""

    class Meta:
        app_label = 'el_pagination'


    def __str__(self):
        return 'TestModel: {0}'.format(self.id)


@python_2_unicode_compatible
class TestTagModel(models.Model):
    """A model used in tests."""

    class Meta:
        app_label = 'el_pagination'


    def __str__(self):
        return 'TestTagModel: {0}'.format(self.id)


call_command('makemigrations', verbosity=0)
call_command('migrate', verbosity=0)
