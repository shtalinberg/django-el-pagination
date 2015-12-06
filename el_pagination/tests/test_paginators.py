"""Paginator tests."""

from __future__ import unicode_literals

from django.test import TestCase

from el_pagination import paginators


class PaginatorTestMixin(object):
    """Base test mixin for paginators.

    Subclasses (actual test cases) must define the ``paginator_class`` name.
    """

    def setUp(self):
        self.items = list(range(30))
        self.per_page = 7
        self.paginator = self.paginator_class(
            self.items, self.per_page, orphans=2)

    def test_object_list(self):
        # Ensure the paginator correctly returns objects for each page.
        first_page = self.paginator.first_page
        expected = self.items[first_page:first_page + self.per_page]
        object_list = self.paginator.page(2).object_list
        self.assertSequenceEqual(expected, object_list)

    def test_orphans(self):
        # Ensure orphans are included in the last page.
        object_list = self.paginator.page(4).object_list
        self.assertSequenceEqual(self.items[-9:], object_list)

    def test_no_orphans(self):
        # Ensure exceeding orphans generate a new page.
        paginator = self.paginator_class(range(11), 8, orphans=2)
        object_list = paginator.page(2).object_list
        self.assertEqual(3, len(object_list))

    def test_empty_page(self):
        # En error if raised if the requested page does not exist.
        with self.assertRaises(paginators.EmptyPage):
            self.paginator.page(5)

    def test_invalid_page(self):
        # En error is raised if the requested page is not valid.
        with self.assertRaises(paginators.PageNotAnInteger):
            self.paginator.page('__not_valid__')
        with self.assertRaises(paginators.EmptyPage):
            self.paginator.page(0)


class DifferentFirstPagePaginatorTestMixin(PaginatorTestMixin):
    """Base test mixin for paginators.

    This time the paginator defined in ``setUp`` has different number of
    items on the first page.
    Subclasses (actual test cases) must define the ``paginator_class`` name.
    """

    def setUp(self):
        self.items = list(range(26))
        self.per_page = 7
        self.paginator = self.paginator_class(
            self.items, self.per_page, first_page=3, orphans=2)

    def test_no_orphans(self):
        # Ensure exceeding orphans generate a new page.
        paginator = self.paginator_class(range(11), 5, first_page=3, orphans=2)
        object_list = paginator.page(3).object_list
        self.assertEqual(3, len(object_list))


class DefaultPaginatorTest(PaginatorTestMixin, TestCase):

    paginator_class = paginators.DefaultPaginator

    def test_indexes(self):
        # Ensure start and end indexes are correct.
        page = self.paginator.page(2)
        self.assertEqual(self.per_page + 1, page.start_index())
        self.assertEqual(self.per_page * 2, page.end_index())

    def test_items_count(self):
        # Ensure the paginator reflects the number of items.
        self.assertEqual(len(self.items), self.paginator.count)

    def test_num_pages(self):
        # Ensure the number of pages is correctly calculated.
        self.assertEqual(4, self.paginator.num_pages)

    def test_page_range(self):
        # Ensure the page range is correctly calculated.
        self.assertSequenceEqual([1, 2, 3, 4], self.paginator.page_range)

    def test_no_items(self):
        # Ensure the right values are returned if the page contains no items.
        paginator = self.paginator_class([], 10)
        page = paginator.page(1)
        self.assertEqual(0, paginator.count)
        self.assertEqual(0, page.start_index())

    def test_single_page_indexes(self):
        # Ensure the returned indexes are correct for a single page pagination.
        paginator = self.paginator_class(range(6), 5, orphans=2)
        page = paginator.page(1)
        self.assertEqual(1, page.start_index())
        self.assertEqual(6, page.end_index())


class LazyPaginatorTest(PaginatorTestMixin, TestCase):

    paginator_class = paginators.LazyPaginator

    def test_items_count(self):
        # The lazy paginator does not implement items count.
        with self.assertRaises(NotImplementedError):
            self.paginator.count

    def test_num_pages(self):
        # The number of pages depends on the current page.
        self.paginator.page(2)
        self.assertEqual(3, self.paginator.num_pages)

    def test_page_range(self):
        # The lazy paginator does not implement page range.
        with self.assertRaises(NotImplementedError):
            self.paginator.page_range


class DifferentFirstPageDefaultPaginatorTest(
        DifferentFirstPagePaginatorTestMixin, TestCase):

    paginator_class = paginators.DefaultPaginator


class DifferentFirstPageLazyPaginatorTest(
        DifferentFirstPagePaginatorTestMixin, TestCase):

    paginator_class = paginators.LazyPaginator
