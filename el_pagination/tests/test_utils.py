"""Utilities tests."""

from __future__ import unicode_literals

from django.test import TestCase
from django.test.client import RequestFactory

from endless_pagination import utils
from endless_pagination.settings import PAGE_LABEL
from endless_pagination.exceptions import PaginationError


class GetDataFromContextTest(TestCase):

    def test_valid_context(self):
        # Ensure the endless data is correctly retrieved from context.
        context = {'endless': 'test-data'}
        self.assertEqual('test-data', utils.get_data_from_context(context))

    def test_invalid_context(self):
        # A ``PaginationError`` is raised if the data cannot be found
        # in the context.
        self.assertRaises(PaginationError, utils.get_data_from_context, {})


class GetPageNumberFromRequestTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_no_querystring_key(self):
        # Ensure the first page is returned if page info cannot be
        # retrieved from the querystring.
        request = self.factory.get('/')
        self.assertEqual(1, utils.get_page_number_from_request(request))

    def test_default_querystring_key(self):
        # Ensure the default page label is used if ``querystring_key``
        # is not provided.
        request = self.factory.get('?{0}=2'.format(PAGE_LABEL))
        self.assertEqual(2, utils.get_page_number_from_request(request))

    def test_default(self):
        # Ensure the default page number is returned if page info cannot be
        # retrieved from the querystring.
        request = self.factory.get('/')
        page_number = utils.get_page_number_from_request(request, default=3)
        self.assertEqual(3, page_number)

    def test_custom_querystring_key(self):
        # Ensure the page returned correctly reflects the ``querystring_key``.
        request = self.factory.get('?mypage=4'.format(PAGE_LABEL))
        page_number = utils.get_page_number_from_request(
            request, querystring_key='mypage')
        self.assertEqual(4, page_number)

    def test_post_data(self):
        # The page number can also be present in POST data.
        request = self.factory.post('/', {PAGE_LABEL: 5})
        self.assertEqual(5, utils.get_page_number_from_request(request))


class GetPageNumbersTest(TestCase):

    def test_defaults(self):
        # Ensure the pages are returned correctly using the default values.
        pages = utils.get_page_numbers(10, 20)
        expected = [
            'previous', 1, 2, 3, None, 8, 9, 10, 11, 12,
            None, 18, 19, 20, 'next']
        self.assertSequenceEqual(expected, pages)

    def test_first_page(self):
        # Ensure the correct pages are returned if the first page is requested.
        pages = utils.get_page_numbers(1, 10)
        expected = [1, 2, 3, None, 8, 9, 10, 'next']
        self.assertSequenceEqual(expected, pages)

    def test_last_page(self):
        # Ensure the correct pages are returned if the last page is requested.
        pages = utils.get_page_numbers(10, 10)
        expected = ['previous', 1, 2, 3, None, 8, 9, 10]
        self.assertSequenceEqual(expected, pages)

    def test_no_extremes(self):
        # Ensure the correct pages are returned with no extremes.
        pages = utils.get_page_numbers(10, 20, extremes=0)
        expected = ['previous', 8, 9, 10, 11, 12, 'next']
        self.assertSequenceEqual(expected, pages)

    def test_no_arounds(self):
        # Ensure the correct pages are returned with no arounds.
        pages = utils.get_page_numbers(10, 20, arounds=0)
        expected = ['previous', 1, 2, 3, None, 10, None, 18, 19, 20, 'next']
        self.assertSequenceEqual(expected, pages)

    def test_no_extremes_arounds(self):
        # Ensure the correct pages are returned with no extremes and arounds.
        pages = utils.get_page_numbers(10, 20, extremes=0, arounds=0)
        expected = ['previous', 10, 'next']
        self.assertSequenceEqual(expected, pages)

    def test_one_page(self):
        # Ensure the correct pages are returned if there is only one page.
        pages = utils.get_page_numbers(1, 1)
        expected = [1]
        self.assertSequenceEqual(expected, pages)

    def test_arrows(self):
        # Ensure the pages are returned correctly adding first / last arrows.
        pages = utils.get_page_numbers(5, 10, arrows=True)
        expected = [
            'first', 'previous', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'next', 'last']
        self.assertSequenceEqual(expected, pages)

    def test_arrows_first_page(self):
        # Ensure the correct pages are returned if the first page is requested
        # adding first / last arrows.
        pages = utils.get_page_numbers(1, 5, arrows=True)
        expected = [1, 2, 3, 4, 5, 'next', 'last']
        self.assertSequenceEqual(expected, pages)

    def test_arrows_last_page(self):
        # Ensure the correct pages are returned if the last page is requested
        # adding first / last arrows.
        pages = utils.get_page_numbers(5, 5, arrows=True)
        expected = ['first', 'previous', 1, 2, 3, 4, 5]
        self.assertSequenceEqual(expected, pages)


class IterFactorsTest(TestCase):

    def _run_tests(self, test_data):
        for starting_factor, num_factors, expected in test_data:
            factor = utils._iter_factors(starting_factor)
            factors = [next(factor) for idx in range(num_factors)]
            self.assertEqual(expected, factors)

    def test__iter_factors(self):
        # Ensure the correct values are progressively generated.
        test_data = (
            (1, 10, [1, 3, 10, 30, 100, 300, 1000, 3000, 10000, 30000]),
            (5, 10, [5, 15, 50, 150, 500, 1500, 5000, 15000, 50000, 150000]),
            (10, 10, [
                10, 30, 100, 300, 1000, 3000, 10000, 30000, 100000, 300000]),
        )
        self._run_tests(test_data)


class MakeElasticRangeTest(TestCase):

    def _run_tests(self, test_data):
        for begin, end, expected in test_data:
            elastic_range = utils._make_elastic_range(begin, end)
            self.assertEqual(expected, elastic_range)

    def test___make_elastic_range_units(self):
        # Ensure an S-curved range of pages is correctly generated for units.
        test_data = (
            (1, 1, [1]),
            (1, 2, [1, 2]),
            (2, 2, [2]),
            (1, 3, [1, 2, 3]),
            (2, 3, [2, 3]),
            (3, 3, [3]),
            (1, 4, [1, 2, 3, 4]),
            (2, 4, [2, 3, 4]),
            (3, 4, [3, 4]),
            (4, 4, [4]),
            (1, 5, [1, 2, 4, 5]),
            (2, 5, [2, 3, 4, 5]),
            (3, 5, [3, 4, 5]),
            (4, 5, [4, 5]),
            (5, 5, [5]),
            (1, 6, [1, 2, 5, 6]),
            (2, 6, [2, 3, 5, 6]),
            (3, 6, [3, 4, 5, 6]),
            (4, 6, [4, 5, 6]),
            (5, 6, [5, 6]),
            (6, 6, [6]),
            (1, 7, [1, 2, 4, 6, 7]),
            (2, 7, [2, 3, 6, 7]),
            (3, 7, [3, 4, 6, 7]),
            (4, 7, [4, 5, 6, 7]),
            (5, 7, [5, 6, 7]),
            (6, 7, [6, 7]),
            (7, 7, [7]),
            (1, 8, [1, 2, 4, 5, 7, 8]),
            (2, 8, [2, 3, 5, 7, 8]),
            (3, 8, [3, 4, 7, 8]),
            (4, 8, [4, 5, 7, 8]),
            (5, 8, [5, 6, 7, 8]),
            (6, 8, [6, 7, 8]),
            (7, 8, [7, 8]),
            (8, 8, [8]),
            (1, 9, [1, 2, 4, 6, 8, 9]),
            (2, 9, [2, 3, 5, 6, 8, 9]),
            (3, 9, [3, 4, 6, 8, 9]),
            (4, 9, [4, 5, 8, 9]),
            (5, 9, [5, 6, 8, 9]),
            (6, 9, [6, 7, 8, 9]),
            (7, 9, [7, 8, 9]),
            (8, 9, [8, 9]),
            (9, 9, [9]),
            (1, 10, [1, 2, 4, 7, 9, 10]),
            (2, 10, [2, 3, 5, 7, 9, 10]),
            (3, 10, [3, 4, 6, 7, 9, 10]),
            (4, 10, [4, 5, 7, 9, 10]),
            (5, 10, [5, 6, 9, 10]),
            (6, 10, [6, 7, 9, 10]),
            (7, 10, [7, 8, 9, 10]),
            (8, 10, [8, 9, 10]),
            (9, 10, [9, 10]),
            (10, 10, [10]),
        )
        self._run_tests(test_data)

    def test___make_elastic_range_tens(self):
        # Ensure an S-curved range of pages is correctly generated for tens.
        test_data = (
            (1, 20, [1, 2, 4, 17, 19, 20]),
            (5, 20, [5, 6, 8, 17, 19, 20]),
            (10, 20, [10, 11, 13, 17, 19, 20]),
            (11, 20, [11, 12, 14, 17, 19, 20]),
            (1, 50, [1, 2, 4, 11, 40, 47, 49, 50]),
            (10, 50, [10, 11, 13, 20, 40, 47, 49, 50]),
            (25, 50, [25, 26, 28, 35, 40, 47, 49, 50]),
            (1, 100, [1, 2, 4, 11, 31, 70, 90, 97, 99, 100]),
            (25, 100, [25, 26, 28, 35, 55, 70, 90, 97, 99, 100]),
            (50, 100, [50, 51, 53, 60, 90, 97, 99, 100]),
            (75, 100, [75, 76, 78, 85, 90, 97, 99, 100]),
        )
        self._run_tests(test_data)

    def test___make_elastic_range_more(self):
        # An S-curved range of pages is correctly generated for larger numbers.
        test_data = (
            (1, 500, [1, 5, 13, 41, 121, 380, 460, 488, 496, 500]),
            (1, 1000, [1, 10, 28, 91, 271, 730, 910, 973, 991, 1000]),
            (1, 10000, [
                1, 100, 298, 991, 2971, 7030, 9010, 9703, 9901, 10000]),
            (1, 100000, [
                1, 1000, 2998, 9991, 29971, 70030, 90010, 97003, 99001,
                100000]),
            (1, 1000000, [
                1, 10000, 29998, 99991, 299971, 700030, 900010, 970003,
                990001, 1000000]),
        )
        self._run_tests(test_data)


class GetElasticPageNumbersTest(TestCase):

    def _run_tests(self, test_data):
        for current_page, num_pages, expected in test_data:
            pages = utils.get_elastic_page_numbers(current_page, num_pages)
            self.assertSequenceEqual(expected, pages)

    def test_get_elastic_page_numbers_units(self):
        # Ensure the callable returns the expected values for units.
        test_data = (
            (1, 1, [1]),
            (1, 2, [1, 2]),
            (2, 2, [1, 2]),
            (1, 3, [1, 2, 3]),
            (3, 3, [1, 2, 3]),
            (1, 4, [1, 2, 3, 4]),
            (4, 4, [1, 2, 3, 4]),
            (1, 5, [1, 2, 3, 4, 5]),
            (5, 5, [1, 2, 3, 4, 5]),
            (1, 6, [1, 2, 3, 4, 5, 6]),
            (6, 6, [1, 2, 3, 4, 5, 6]),
            (1, 7, [1, 2, 3, 4, 5, 6, 7]),
            (7, 7, [1, 2, 3, 4, 5, 6, 7]),
            (1, 8, [1, 2, 3, 4, 5, 6, 7, 8]),
            (8, 8, [1, 2, 3, 4, 5, 6, 7, 8]),
            (1, 9, [1, 2, 3, 4, 5, 6, 7, 8, 9]),
            (9, 9, [1, 2, 3, 4, 5, 6, 7, 8, 9]),
            (1, 10, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
            (6, 10, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
            (10, 10, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        )
        self._run_tests(test_data)

    def test_get_elastic_page_numbers_tens(self):
        # Ensure the callable returns the expected values for tens.
        test_data = (
            (1, 11, [
                1, 2, 4, 8, 10, 11, 'next', 'last']),
            (2, 11, [
                'first', 'previous', 1, 2, 3, 5, 8, 10, 11, 'next', 'last']),
            (3, 11, [
                'first', 'previous', 1, 2, 3, 4, 6, 8, 10, 11, 'next',
                'last']),
            (4, 11, [
                'first', 'previous', 1, 2, 3, 4, 5, 7, 8, 10, 11, 'next',
                'last']),
            (5, 11, [
                'first', 'previous', 1, 2, 4, 5, 6, 8, 10, 11, 'next',
                'last']),
            (6, 11, [
                'first', 'previous', 1, 2, 5, 6, 7, 10, 11, 'next', 'last']),
            (7, 11, [
                'first', 'previous', 1, 2, 4, 6, 7, 8, 10, 11, 'next',
                'last']),
            (8, 11, [
                'first', 'previous', 1, 2, 4, 5, 7, 8, 9, 10, 11, 'next',
                'last']),
            (9, 11, [
                'first', 'previous', 1, 2, 4, 6, 8, 9, 10, 11, 'next',
                'last']),
            (10, 11, [
                'first', 'previous', 1, 2, 4, 7, 9, 10, 11, 'next', 'last']),
            (11, 11, ['first', 'previous', 1, 2, 4, 8, 10, 11]),
            (1, 12, [1, 2, 4, 9, 11, 12, 'next', 'last']),
            (2, 12, [
                'first', 'previous', 1, 2, 3, 5, 9, 11, 12, 'next', 'last']),
            (6, 12, [
                'first', 'previous', 1, 2, 5, 6, 7, 9, 11, 12, 'next',
                'last']),
            (7, 12, [
                'first', 'previous', 1, 2, 4, 6, 7, 8, 11, 12, 'next',
                'last']),
            (11, 12, [
                'first', 'previous', 1, 2, 4, 8, 10, 11, 12, 'next', 'last']),
            (12, 12, ['first', 'previous', 1, 2, 4, 9, 11, 12]),
            (1, 15, [1, 2, 4, 12, 14, 15, 'next', 'last']),
            (5, 15, [
                'first', 'previous', 1, 2, 4, 5, 6, 8, 12, 14, 15, 'next',
                'last']),
            (10, 15, [
                'first', 'previous', 1, 2, 4, 7, 9, 10, 11, 14, 15, 'next',
                'last']),
            (15, 15, ['first', 'previous', 1, 2, 4, 12, 14, 15]),
            (1, 100, [1, 2, 4, 11, 31, 70, 90, 97, 99, 100, 'next', 'last']),
            (25, 100, [
                'first', 'previous', 1, 2, 4, 11, 15, 22, 24, 25, 26, 28, 35,
                55, 70, 90, 97, 99, 100, 'next', 'last']),
            (75, 100, [
                'first', 'previous', 1, 2, 4, 11, 31, 45, 65, 72, 74, 75, 76,
                78, 85, 90, 97, 99, 100, 'next', 'last']),
            (100, 100, [
                'first', 'previous', 1, 2, 4, 11, 31, 70, 90, 97, 99, 100]),
        )
        self._run_tests(test_data)

    def test_get_elastic_page_numbers_more(self):
        # Ensure the callable returns the expected values for larger numbers.
        test_data = (
            (1, 500, [
                1, 5, 13, 41, 121, 380, 460, 488, 496, 500, 'next', 'last']),
            (150, 500, [
                'first', 'previous', 1, 2, 4, 11, 31, 120, 140, 147, 149, 150,
                153, 159, 180, 240, 410, 470, 491, 497, 500, 'next', 'last']),
            (350, 500, [
                'first', 'previous', 1, 4, 10, 31, 91, 260, 320, 341, 347, 350,
                351, 353, 360, 380, 470, 490, 497, 499, 500, 'next', 'last']),
            (500, 500, [
                'first', 'previous', 1, 5, 13, 41, 121, 380, 460, 488, 496,
                500]),
            (100, 1000, [
                'first', 'previous', 1, 2, 4, 11, 31, 70, 90, 97, 99, 100, 109,
                127, 190, 370, 730, 910, 973, 991, 1000, 'next', 'last']),
            (1000, 10000, [
                'first', 'previous', 1, 10, 28, 91, 271, 730, 910, 973, 991,
                1000, 1090, 1270, 1900, 3700, 7300, 9100, 9730, 9910, 10000,
                'next', 'last']),
            (10000, 100000, [
                'first', 'previous', 1, 100, 298, 991, 2971, 7030, 9010, 9703,
                9901, 10000, 10900, 12700, 19000, 37000, 73000, 91000, 97300,
                99100, 100000, 'next', 'last']),
            (100000, 1000000, [
                'first', 'previous', 1, 1000, 2998, 9991, 29971, 70030, 90010,
                97003, 99001, 100000, 109000, 127000, 190000, 370000, 730000,
                910000, 973000, 991000, 1000000, 'next', 'last']),
        )
        self._run_tests(test_data)


class GetQuerystringForPageTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_querystring(self):
        # Ensure the querystring is correctly generated from request.
        request = self.factory.get('/')
        querystring = utils.get_querystring_for_page(request, 2, 'mypage')
        self.assertEqual('?mypage=2', querystring)

    def test_default_page(self):
        # Ensure the querystring is empty for the default page.
        request = self.factory.get('/')
        querystring = utils.get_querystring_for_page(
            request, 3, 'mypage', default_number=3)
        self.assertEqual('', querystring)

    def test_composition(self):
        # Ensure existing querystring is correctly preserved.
        request = self.factory.get('/?mypage=1&foo=bar')
        querystring = utils.get_querystring_for_page(request, 4, 'mypage')
        self.assertIn('mypage=4', querystring)
        self.assertIn('foo=bar', querystring)

    def test_querystring_key(self):
        # The querystring key is deleted from the querystring if present.
        request = self.factory.get('/?querystring_key=mykey')
        querystring = utils.get_querystring_for_page(request, 5, 'mypage')
        self.assertEqual('?mypage=5', querystring)


class NormalizePageNumberTest(TestCase):

    page_range = [1, 2, 3, 4]

    def test_in_range(self):
        # Ensure the correct page number is returned when the requested
        # negative index is in range.
        page_numbers = [-1, -2, -3, -4]
        expected_results = reversed(self.page_range)
        for page_number, expected in zip(page_numbers, expected_results):
            result = utils.normalize_page_number(page_number, self.page_range)
            self.assertEqual(expected, result)

    def test_out_of_range(self):
        # Ensure the page number 1 returned when the requested negative index
        # is out of range.
        result = utils.normalize_page_number(-5, self.page_range)
        self.assertEqual(self.page_range[0], result)
