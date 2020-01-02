from django.db import models


def make_model_instances(number):
    """Make a ``number`` of test model instances and return a queryset."""
    for _ in range(number):
        TestModel.objects.create()
    return TestModel.objects.all().order_by('pk')


class TestModel(models.Model):
    """A model used in tests."""

    class Meta:
        app_label = 'el_pagination'

    def __str__(self):
        return 'TestModel: {0}'.format(self.id)
