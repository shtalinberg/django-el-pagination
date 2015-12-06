"""Loader tests."""

from __future__ import unicode_literals
from contextlib import contextmanager

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from el_pagination import loaders


test_object = 'test object'


class ImproperlyConfiguredTestMixin(object):
    """Include an ImproperlyConfigured assertion."""

    @contextmanager
    def assertImproperlyConfigured(self, message):
        """Assert the code in the context manager block raises an error.

        The error must be ImproperlyConfigured, and the error message must
        include the given *message*.
        """
        try:
            yield
        except ImproperlyConfigured as err:
            self.assertIn(message, str(err).lower())
        else:
            self.fail('ImproperlyConfigured not raised')


class AssertImproperlyConfiguredTest(ImproperlyConfiguredTestMixin, TestCase):

    def test_assertion(self):
        # Ensure the assertion does not fail if ImproperlyConfigured is raised
        # with the given error message.
        with self.assertImproperlyConfigured('error'):
            raise ImproperlyConfigured('Example error text')

    def test_case_insensitive(self):
        # Ensure the error message test is case insensitive.
        with self.assertImproperlyConfigured('error'):
            raise ImproperlyConfigured('Example ERROR text')

    def test_assertion_fails_different_message(self):
        # Ensure the assertion fails if ImproperlyConfigured is raised with
        # a different message.
        with self.assertRaises(AssertionError):
            with self.assertImproperlyConfigured('failure'):
                raise ImproperlyConfigured('Example error text')

    def test_assertion_fails_no_exception(self):
        # Ensure the assertion fails if ImproperlyConfigured is not raised.
        with self.assertRaises(AssertionError) as cm:
            with self.assertImproperlyConfigured('error'):
                pass
        self.assertEqual('ImproperlyConfigured not raised', str(cm.exception))

    def test_assertion_fails_different_exception(self):
        # Ensure other exceptions are not swallowed.
        with self.assertRaises(TypeError):
            with self.assertImproperlyConfigured('error'):
                raise TypeError


class LoadObjectTest(ImproperlyConfiguredTestMixin, TestCase):

    def setUp(self):
        self.module = self.__class__.__module__

    def test_valid_path(self):
        # Ensure the object is correctly loaded if the provided path is valid.
        path = '.'.join((self.module, 'test_object'))
        self.assertIs(test_object, loaders.load_object(path))

    def test_module_not_found(self):
        # An error is raised if the module cannot be found.
        with self.assertImproperlyConfigured('not found'):
            loaders.load_object('__invalid__.module')

    def test_invalid_module(self):
        # An error is raised if the provided path is not a valid dotted string.
        with self.assertImproperlyConfigured('invalid'):
            loaders.load_object('')

    def test_object_not_found(self):
        # An error is raised if the object cannot be found in the module.
        path = '.'.join((self.module, '__does_not_exist__'))
        with self.assertImproperlyConfigured('object'):
            loaders.load_object(path)
