"""Ephemeral models used to represent a page and a list of pages."""

from __future__ import unicode_literals

from django.template import (
    loader,
    Context,
)
from django.utils.encoding import iri_to_uri

from el_pagination import (
    loaders,
    settings,
    utils,
)


# Page templates cache.
_template_cache = {}


class ELPage(utils.UnicodeMixin):
    """A page link representation.

    Interesting attributes:

        - *self.number*: the page number;
        - *self.label*: the label of the link
          (usually the page number as string);
        - *self.url*: the url of the page (strting with "?");
        - *self.path*: the path of the page;
        - *self.is_current*: return True if page is the current page displayed;
        - *self.is_first*: return True if page is the first page;
        - *self.is_last*:  return True if page is the last page.
    """

    def __init__(
            self, request, number, current_number, total_number,
            querystring_key, label=None, default_number=1, override_path=None,
            context=None):
        self._request = request
        self.number = number
        self.label = utils.text(number) if label is None else label
        self.querystring_key = querystring_key
        self.context = context or {}
        self.context['request'] = request

        self.is_current = number == current_number
        self.is_first = number == 1
        self.is_last = number == total_number

        self.url = utils.get_querystring_for_page(
            request, number, self.querystring_key,
            default_number=default_number)
        path = iri_to_uri(override_path or request.path)
        self.path = '{0}{1}'.format(path, self.url)

    def __unicode__(self):
        """Render the page as a link."""
        extra_context = {
            'add_nofollow': settings.ADD_NOFOLLOW,
            'page': self,
            'querystring_key': self.querystring_key,
        }
        if self.is_current:
            template_name = 'el_pagination/current_link.html'
        else:
            template_name = 'el_pagination/page_link.html'
        template = _template_cache.setdefault(
            template_name, loader.get_template(template_name))
        with self.context.push(**extra_context):
            return template.render(self.context.flatten())


class PageList(utils.UnicodeMixin):
    """A sequence of endless pages."""

    def __init__(
            self, request, page, querystring_key, context,
            default_number=None, override_path=None):
        self._request = request
        self._page = page
        self.context = context
        self.context['request'] = request
        if default_number is None:
            self._default_number = 1
        else:
            self._default_number = int(default_number)
        self._querystring_key = querystring_key
        self._override_path = override_path

    def _endless_page(self, number, label=None):
        """Factory function that returns a *ELPage* instance.

        This method works just like a partial constructor.
        """
        return ELPage(
            self._request,
            number,
            self._page.number,
            len(self),
            self._querystring_key,
            label=label,
            default_number=self._default_number,
            override_path=self._override_path,
            context=self.context
        )

    def __getitem__(self, value):
        # The type conversion is required here because in templates Django
        # performs a dictionary lookup before the attribute lokups
        # (when a dot is encountered).
        try:
            value = int(value)
        except (TypeError, ValueError):
            # A TypeError says to django to continue with an attribute lookup.
            raise TypeError
        if 1 <= value <= len(self):
            return self._endless_page(value)
        raise IndexError('page list index out of range')

    def __len__(self):
        """The length of the sequence is the total number of pages."""
        return self._page.paginator.num_pages

    def __iter__(self):
        """Iterate over all the endless pages (from first to last)."""
        for i in range(len(self)):
            yield self[i + 1]

    def __unicode__(self):
        """Return a rendered Digg-style pagination (by default).

        The callable *settings.PAGE_LIST_CALLABLE* can be used to customize
        how the pages are displayed. The callable takes the current page number
        and the total number of pages, and must return a sequence of page
        numbers that will be displayed. The sequence can contain other values:

            - *'previous'*: will display the previous page in that position;
            - *'next'*: will display the next page in that position;
            - *'first'*: will display the first page as an arrow;
            - *'last'*: will display the last page as an arrow;
            - *None*: a separator will be displayed in that position.

        Here is an example of custom calable that displays the previous page,
        then the first page, then a separator, then the current page, and
        finally the last page::

            def get_page_numbers(current_page, num_pages):
                return ('previous', 1, None, current_page, 'last')

        If *settings.PAGE_LIST_CALLABLE* is None an internal callable is used,
        generating a Digg-style pagination. The value of
        *settings.PAGE_LIST_CALLABLE* can also be a dotted path to a callable.
        """
        if len(self) > 1:
            callable_or_path = settings.PAGE_LIST_CALLABLE
            if callable_or_path:
                if callable(callable_or_path):
                    pages_callable = callable_or_path
                else:
                    pages_callable = loaders.load_object(callable_or_path)
            else:
                pages_callable = utils.get_page_numbers
            pages = []
            for item in pages_callable(self._page.number, len(self)):
                if item is None:
                    pages.append(None)
                elif item == 'previous':
                    pages.append(self.previous())
                elif item == 'next':
                    pages.append(self.next())
                elif item == 'first':
                    pages.append(self.first_as_arrow())
                elif item == 'last':
                    pages.append(self.last_as_arrow())
                else:
                    pages.append(self[item])
            template = loader.get_template('el_pagination/show_pages.html')
            with self.context.push(pages=pages):
                return template.render(self.context.flatten())
        return ''

    def current(self):
        """Return the current page."""
        return self._endless_page(self._page.number)

    def current_start_index(self):
        """Return the 1-based index of the first item on the current page."""
        return self._page.start_index()

    def current_end_index(self):
        """Return the 1-based index of the last item on the current page."""
        return self._page.end_index()

    def total_count(self):
        """Return the total number of objects, across all pages."""
        return self._page.paginator.count

    def first(self, label=None):
        """Return the first page."""
        return self._endless_page(1, label=label)

    def last(self, label=None):
        """Return the last page."""
        return self._endless_page(len(self), label=label)

    def first_as_arrow(self):
        """Return the first page as an arrow.

        The page label (arrow) is defined in ``settings.FIRST_LABEL``.
        """
        return self.first(label=settings.FIRST_LABEL)

    def last_as_arrow(self):
        """Return the last page as an arrow.

        The page label (arrow) is defined in ``settings.LAST_LABEL``.
        """
        return self.last(label=settings.LAST_LABEL)

    def previous(self):
        """Return the previous page.

        The page label is defined in ``settings.PREVIOUS_LABEL``.
        Return an empty string if current page is the first.
        """
        if self._page.has_previous():
            return self._endless_page(
                self._page.previous_page_number(),
                label=settings.PREVIOUS_LABEL)
        return ''

    def next(self):
        """Return the next page.

        The page label is defined in ``settings.NEXT_LABEL``.
        Return an empty string if current page is the last.
        """
        if self._page.has_next():
            return self._endless_page(
                self._page.next_page_number(),
                label=settings.NEXT_LABEL)
        return ''

    def paginated(self):
        """Return True if this page list contains more than one page."""
        return len(self) > 1

    def per_page_number(self):
        """Return the numbers of objects are normally display in per page."""
        return self._page.paginator.per_page
