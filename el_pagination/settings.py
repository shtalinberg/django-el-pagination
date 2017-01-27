# """Django Endless Pagination settings file."""

from __future__ import unicode_literals

from django.conf import settings


# How many objects are normally displayed in a page
# (overwriteable by templatetag).
PER_PAGE = getattr(settings, 'EL_PAGINATION_PER_PAGE', 10)
# The querystring key of the page number.
PAGE_LABEL = getattr(settings, 'EL_PAGINATION_PAGE_LABEL', 'page')
# See django *Paginator* definition of orphans.
ORPHANS = getattr(settings, 'EL_PAGINATION_ORPHANS', 0)

# If you use the default *show_more* template, here you can customize
# the content of the loader hidden element.
# Html is safe here, e.g. you can show your pretty animated gif:
#    EL_PAGINATION_LOADING = """
#        <img src="/static/img/loader.gif" alt="loading" />
#    """
LOADING = getattr(
    settings, 'EL_PAGINATION_LOADING', 'loading')

# Labels for previous and next page links.
PREVIOUS_LABEL = getattr(
    settings, 'EL_PAGINATION_PREVIOUS_LABEL', '&lt;')
NEXT_LABEL = getattr(settings, 'EL_PAGINATION_NEXT_LABEL', '&gt;')

# Labels for first and last page links.
FIRST_LABEL = getattr(
    settings, 'EL_PAGINATION_FIRST_LABEL', '&lt;&lt;')
LAST_LABEL = getattr(settings, 'EL_PAGINATION_LAST_LABEL', '&gt;&gt;')

# Set to True if your SEO alchemist wants all the links in Digg-style
# pagination to be ``nofollow``.
ADD_NOFOLLOW = getattr(settings, 'EL_PAGINATION_ADD_NOFOLLOW', False)

# Callable (or dotted path to a callable) returning pages to be displayed.
# If None, a default callable is used (which produces Digg-style pagination).
PAGE_LIST_CALLABLE = getattr(
    settings, 'EL_PAGINATION_PAGE_LIST_CALLABLE', None)

# The default callable returns a sequence of pages producing Digg-style
# pagination, and depending on the settings below.
DEFAULT_CALLABLE_EXTREMES = getattr(
    settings, 'EL_PAGINATION_DEFAULT_CALLABLE_EXTREMES', 3)
DEFAULT_CALLABLE_AROUNDS = getattr(
    settings, 'EL_PAGINATION_DEFAULT_CALLABLE_AROUNDS', 2)
# Whether or not the first and last pages arrows are displayed.
DEFAULT_CALLABLE_ARROWS = getattr(
    settings, 'EL_PAGINATION_DEFAULT_CALLABLE_ARROWS', False)

# Template variable name for *page_template* decorator.
TEMPLATE_VARNAME = getattr(
    settings, 'EL_PAGINATION_TEMPLATE_VARNAME', 'template')

# If page out of range, throw a 404 exception
PAGE_OUT_OF_RANGE_404 = getattr(
    settings, 'EL_PAGINATION_PAGE_OUT_OF_RANGE_404', False)
