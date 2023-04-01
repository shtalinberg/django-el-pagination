"""Model tests."""



from contextlib import contextmanager

from django.template import Context
from django.test import TestCase
from django.test.client import RequestFactory
from django.utils.encoding import force_str

from el_pagination import models as el_models
from el_pagination import settings, utils
from el_pagination.paginators import DefaultPaginator


@contextmanager
def local_settings(**kwargs):
    """Override local Django Endless Pagination settings.

    This context manager can be used in a way similar to Django own
    ``TestCase.settings()``.
    """
    original_values = []
    for key, value in kwargs.items():
        original_values.append([key, getattr(settings, key)])
        setattr(settings, key, value)
    try:
        yield
    finally:
        for key, value in original_values:
            setattr(settings, key, value)


class LocalSettingsTest(TestCase):

    def setUp(self):
        settings._LOCAL_SETTINGS_TEST = 'original'

    def tearDown(self):
        del settings._LOCAL_SETTINGS_TEST

    def test_settings_changed(self):
        # Check that local settings are changed.
        with local_settings(_LOCAL_SETTINGS_TEST='changed'):
            self.assertEqual('changed', settings._LOCAL_SETTINGS_TEST)

    def test_settings_restored(self):
        # Check that local settings are restored.
        with local_settings(_LOCAL_SETTINGS_TEST='changed'):
            pass
        self.assertEqual('original', settings._LOCAL_SETTINGS_TEST)

    def test_restored_after_exception(self):
        # Check that local settings are restored after an exception.
        with self.assertRaises(RuntimeError):
            with local_settings(_LOCAL_SETTINGS_TEST='changed'):
                raise RuntimeError()
            self.assertEqual('original', settings._LOCAL_SETTINGS_TEST)


def page_list_callable_arrows(number, num_pages):
    """Wrap ``el_pagination.utils.get_page_numbers``.

    Set first / last page arrows to True.
    """
    return utils.get_page_numbers(number, num_pages, arrows=True)


page_list_callable_dummy = lambda number, num_pages: [None]


class PageListTest(TestCase):

    def setUp(self):
        self.paginator = DefaultPaginator(range(30), 7, orphans=2)
        self.current_number = 2
        self.page_label = 'page'
        self.factory = RequestFactory()
        self.request = self.factory.get(
            self.get_path_for_page(self.current_number))
        self.pages = el_models.PageList(
            self.request, self.paginator.page(self.current_number),
            self.page_label, context=Context())

    def get_url_for_page(self, number):
        """Return a url for the given page ``number``."""
        return '?{0}={1}'.format(self.page_label, number)

    def get_path_for_page(self, number):
        """Return a path for the given page ``number``."""
        return '/' + self.get_url_for_page(number)

    def check_page(
            self, page, number, is_first, is_last, is_current, label=None):
        """Perform several assertions on the given page attrs."""
        if label is None:
            label = force_str(page.number)
        self.assertEqual(label, page.label)
        self.assertEqual(number, page.number)
        self.assertEqual(is_first, page.is_first)
        self.assertEqual(is_last, page.is_last)
        self.assertEqual(is_current, page.is_current)

    def check_page_list_callable(self, callable_or_path):
        """Check the provided *page_list_callable* is actually used."""
        with local_settings(PAGE_LIST_CALLABLE=callable_or_path):
            rendered = force_str(self.pages.get_rendered()).strip()
        expected = '<span class="endless_separator">...</span>'
        self.assertEqual(expected, rendered)

    def test_length(self):
        # Ensure the length of the page list equals the number of pages.
        self.assertEqual(self.paginator.num_pages, len(self.pages))

    def test_paginated(self):
        # Ensure the *paginated* method returns True if the page list contains
        # more than one page, False otherwise.
        page = DefaultPaginator(range(10), 10).page(1)
        pages = el_models.PageList(self.request, page, self.page_label,
                                   context=Context())
        self.assertFalse(pages.paginated())
        self.assertTrue(self.pages.paginated())

    def test_first_page(self):
        # Ensure the attrs of the first page are correctly defined.
        page = self.pages.first()
        self.assertEqual('/', page.path)
        self.assertEqual('', page.url)
        self.check_page(page, 1, True, False, False)

    def test_last_page(self):
        # Ensure the attrs of the last page are correctly defined.
        page = self.pages.last()
        self.check_page(page, len(self.pages), False, True, False)

    def test_first_page_as_arrow(self):
        # Ensure the attrs of the first page are correctly defined when the
        # page is represented as an arrow.
        page = self.pages.first_as_arrow()
        self.assertEqual('/', page.path)
        self.assertEqual('', page.url)
        self.check_page(
            page, 1, True, False, False, label=settings.FIRST_LABEL)

    def test_last_page_as_arrow(self):
        # Ensure the attrs of the last page are correctly defined when the
        # page is represented as an arrow.
        page = self.pages.last_as_arrow()
        self.check_page(
            page, len(self.pages), False, True, False,
            label=settings.LAST_LABEL)

    def test_current_page(self):
        # Ensure the attrs of the current page are correctly defined.
        page = self.pages.current()
        self.check_page(page, self.current_number, False, False, True)

    def test_path(self):
        # Ensure the path of each page is correctly generated.
        for num, page in enumerate(list(self.pages)[1:]):
            expected = self.get_path_for_page(num + 2)
            self.assertEqual(expected, page.path)

    def test_url(self):
        # Ensure the path of each page is correctly generated.
        for num, page in enumerate(list(self.pages)[1:]):
            expected = self.get_url_for_page(num + 2)
            self.assertEqual(expected, page.url)

    def test_current_indexes(self):
        # Ensure the 1-based indexes of the first and last items on the current
        # page are correctly returned.
        self.assertEqual(8, self.pages.current_start_index())
        self.assertEqual(14, self.pages.current_end_index())

    def test_total_count(self):
        # Ensure the total number of objects is correctly returned.
        self.assertEqual(30, self.pages.total_count())

    def test_page_render(self):
        # Ensure the page is correctly rendered.
        page = self.pages.first()
        rendered_page = force_str(page.render_link())
        self.assertIn('href="/"', rendered_page)
        self.assertIn(page.label, rendered_page)

    def test_current_page_render(self):
        # Ensure the page is correctly rendered.
        page = self.pages.current()
        rendered_page = force_str(page.render_link())
        self.assertNotIn('href', rendered_page)
        self.assertIn(page.label, rendered_page)

    def test_page_list_render(self):
        # Ensure the page list is correctly rendered.
        rendered = force_str(self.pages.get_rendered())
        self.assertEqual(5, rendered.count('<a href'))
        self.assertIn(settings.PREVIOUS_LABEL, rendered)
        self.assertIn(settings.NEXT_LABEL, rendered)

    def test_page_list_render_using_arrows(self):
        # Ensure the page list is correctly rendered when using first / last
        # page arrows.
        page_list_callable = (
            'el_pagination.tests.test_models.page_list_callable_arrows')
        with local_settings(PAGE_LIST_CALLABLE=page_list_callable):
            rendered = force_str(self.pages.get_rendered())
        self.assertEqual(7, rendered.count('<a href'))
        self.assertIn(settings.FIRST_LABEL, rendered)
        self.assertIn(settings.LAST_LABEL, rendered)

    def test_page_list_render_just_one_page(self):
        # Ensure nothing is rendered if the page list contains only one page.
        page = DefaultPaginator(range(10), 10).page(1)
        pages = el_models.PageList(self.request, page, self.page_label,
                                   context=Context())
        self.assertEqual('', force_str(pages))

    def test_different_default_number(self):
        # Ensure the page path is generated based on the default number.
        pages = el_models.PageList(
            self.request, self.paginator.page(2), self.page_label,
            default_number=2, context=Context())
        self.assertEqual('/', pages.current().path)
        self.assertEqual(self.get_path_for_page(1), pages.first().path)

    def test_index_error(self):
        # Ensure an error if raised if a non existent page is requested.
        with self.assertRaises(IndexError):
            self.pages[len(self.pages) + 1]

    def test_previous(self):
        # Ensure the correct previous page is returned.
        previous_page = self.pages.previous()
        self.assertEqual(self.current_number - 1, previous_page.number)

    def test_previous_attrs(self):
        # Ensure the attrs of the next page are correctly defined.
        with local_settings(USE_NEXT_PREVIOUS_LINKS=True):
            previous_page = self.pages.previous()
        self.assertEqual(True, previous_page.is_previous)
        self.check_page(
            previous_page, self.current_number - 1, True, False, False, label=settings.PREVIOUS_LABEL)

    def test_next(self):
        # Ensure the correct next page is returned.
        next_page = self.pages.next()
        self.assertEqual(self.current_number + 1, next_page.number)

    def test_next_attrs(self):
        # Ensure the attrs of the next page are correctly defined.
        with local_settings(USE_NEXT_PREVIOUS_LINKS=True):
            next_page = self.pages.next()
        self.assertEqual(True, next_page.is_next)
        self.check_page(
            next_page, self.current_number + 1, False, False, False, label=settings.NEXT_LABEL)

    def test_no_previous(self):
        # An empty string is returned if the previous page cannot be found.
        pages = el_models.PageList(
            self.request, self.paginator.page(1), self.page_label,
            context=Context())
        self.assertEqual('', pages.previous())

    def test_no_next(self):
        # An empty string is returned if the next page cannot be found.
        num_pages = self.paginator.num_pages
        pages = el_models.PageList(
            self.request, self.paginator.page(num_pages), self.page_label,
            context=Context())
        self.assertEqual('', pages.next())

    def test_customized_page_list_callable(self):
        # The page list is rendered based on ``settings.PAGE_LIST_CALLABLE``.
        self.check_page_list_callable(page_list_callable_dummy)

    def test_customized_page_list_dotted_path(self):
        # The option ``settings.PAGE_LIST_CALLABLE`` can be provided as a
        # dotted path, e.g.: 'path.to.my.callable'.
        self.check_page_list_callable(
            'el_pagination.tests.test_models.page_list_callable_dummy')

    def test_whitespace_in_path(self):
        # Ensure white spaces in paths are correctly handled.
        path = '/a path/containing spaces/'
        request = self.factory.get(path)
        next = el_models.PageList(
            request, self.paginator.page(self.current_number),
            self.page_label, context=Context()).next()
        self.assertEqual(path.replace(' ', '%20') + next.url, next.path)

    def test_lookup(self):
        # Ensure the page list correctly handles lookups.
        pages = self.pages
        self.assertEqual(pages.first().number, pages[1].number)

    def test_invalid_lookup(self):
        # A TypeError is raised if the lookup is not valid.
        with self.assertRaises(TypeError):
            self.pages['invalid']
