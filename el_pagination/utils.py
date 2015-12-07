"""Django EL Pagination utility functions."""

from __future__ import unicode_literals
import sys

from el_pagination import exceptions
from el_pagination.settings import (
    DEFAULT_CALLABLE_AROUNDS,
    DEFAULT_CALLABLE_ARROWS,
    DEFAULT_CALLABLE_EXTREMES,
    PAGE_LABEL,
)


# Handle the Python 2 to 3 migration.
if sys.version_info[0] >= 3:
    PYTHON3 = True
    text = str
else:
    PYTHON3 = False
    # Avoid lint errors under Python 3.
    text = unicode  # NOQA


def get_data_from_context(context):
    """Get the django paginator data object from the given *context*.

    The context is a dict-like object. If the context key ``endless``
    is not found, a *PaginationError* is raised.
    """
    try:
        return context['endless']
    except KeyError:
        raise exceptions.PaginationError(
            'Cannot find endless data in context.')


def get_page_number_from_request(
        request, querystring_key=PAGE_LABEL, default=1):
    """Retrieve the current page number from *GET* or *POST* data.

    If the page does not exists in *request*, or is not a number,
    then *default* number is returned.
    """
    try:
        return int(request.GET.get(querystring_key,
            request.POST.get(querystring_key)))
    except (KeyError, TypeError, ValueError):
        return default


def get_page_numbers(
        current_page, num_pages, extremes=DEFAULT_CALLABLE_EXTREMES,
        arounds=DEFAULT_CALLABLE_AROUNDS, arrows=DEFAULT_CALLABLE_ARROWS):
    """Default callable for page listing.

    Produce a Digg-style pagination.
    """
    page_range = range(1, num_pages + 1)
    pages = []
    if current_page != 1:
        if arrows:
            pages.append('first')
        pages.append('previous')

    # Get first and last pages (extremes).
    first = page_range[:extremes]
    pages.extend(first)
    last = page_range[-extremes:]

    # Get the current pages (arounds).
    current_start = current_page - 1 - arounds
    if current_start < 0:
        current_start = 0
    current_end = current_page + arounds
    if current_end > num_pages:
        current_end = num_pages
    current = page_range[current_start:current_end]

    # Mix first with current pages.
    to_add = current
    if extremes:
        diff = current[0] - first[-1]
        if diff > 1:
            pages.append(None)
        elif diff < 1:
            to_add = current[abs(diff) + 1:]
    pages.extend(to_add)

    # Mix current with last pages.
    if extremes:
        diff = last[0] - current[-1]
        to_add = last
        if diff > 1:
            pages.append(None)
        elif diff < 1:
            to_add = last[abs(diff) + 1:]
        pages.extend(to_add)

    if current_page != num_pages:
        pages.append('next')
        if arrows:
            pages.append('last')
    return pages


def _iter_factors(starting_factor=1):
    """Generator yielding something like 1, 3, 10, 30, 100, 300 etc.

    The series starts from starting_factor.
    """
    while True:
        yield starting_factor
        yield starting_factor * 3
        starting_factor *= 10


def _make_elastic_range(begin, end):
    """Generate an S-curved range of pages.

    Start from both left and right, adding exponentially growing indexes,
    until the two trends collide.
    """
    # Limit growth for huge numbers of pages.
    starting_factor = max(1, (end - begin) // 100)
    factor = _iter_factors(starting_factor)
    left_half, right_half = [], []
    left_val, right_val = begin, end
    right_val = end
    while left_val < right_val:
        left_half.append(left_val)
        right_half.append(right_val)
        next_factor = next(factor)
        left_val = begin + next_factor
        right_val = end - next_factor
    # If the trends happen to meet exactly at one point, retain it.
    if left_val == right_val:
        left_half.append(left_val)
    right_half.reverse()
    return left_half + right_half


def get_elastic_page_numbers(current_page, num_pages):
    """Alternative callable for page listing.

    Produce an adaptive pagination, useful for big numbers of pages, by
    splitting the num_pages ranges in two parts at current_page. Each part
    will have its own S-curve.
    """
    if num_pages <= 10:
        return list(range(1, num_pages + 1))
    if current_page == 1:
        pages = [1]
    else:
        pages = ['first', 'previous']
        pages.extend(_make_elastic_range(1, current_page))
    if current_page != num_pages:
        pages.extend(_make_elastic_range(current_page, num_pages)[1:])
        pages.extend(['next', 'last'])
    return pages


def get_querystring_for_page(
        request, page_number, querystring_key, default_number=1):
    """Return a querystring pointing to *page_number*."""
    querydict = request.GET.copy()
    querydict[querystring_key] = page_number
    # For the default page number (usually 1) the querystring is not required.
    if page_number == default_number:
        del querydict[querystring_key]
    if 'querystring_key' in querydict:
        del querydict['querystring_key']
    if querydict:
        return '?' + querydict.urlencode()
    return ''


def normalize_page_number(page_number, page_range):
    """Handle a negative *page_number*.

    Return a positive page number contained in *page_range*.
    If the negative index is out of range, return the page number 1.
    """
    try:
        return page_range[page_number]
    except IndexError:
        return page_range[0]


class UnicodeMixin(object):
    """Mixin class to handle defining the proper unicode and string methods."""

    if PYTHON3:
        def __str__(self):
            return self.__unicode__()
