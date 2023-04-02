"""Customized Django paginators."""

from math import ceil

from django.core.paginator import EmptyPage, Page, PageNotAnInteger, Paginator


class CustomPage(Page):
    """Handle different number of items on the first page."""

    def start_index(self):
        """Return the 1-based index of the first item on this page."""
        paginator = self.paginator
        # Special case, return zero if no items.
        if paginator.count == 0:
            return 0
        elif self.number == 1:
            return 1
        return (self.number - 2) * paginator.per_page + paginator.first_page + 1

    def end_index(self):
        """Return the 1-based index of the last item on this page."""
        paginator = self.paginator
        # Special case for the last page because there can be orphans.
        if self.number == paginator.num_pages:
            return paginator.count
        return (self.number - 1) * paginator.per_page + paginator.first_page


class BasePaginator(Paginator):
    """A base paginator class subclassed by the other real paginators.

    Handle different number of items on the first page.
    """

    def __init__(self, object_list, per_page, **kwargs):
        self._num_pages = None
        if 'first_page' in kwargs:
            self.first_page = kwargs.pop('first_page')
        else:
            self.first_page = per_page
        super().__init__(object_list, per_page, **kwargs)

    def get_current_per_page(self, number):
        return self.first_page if number == 1 else self.per_page


class DefaultPaginator(BasePaginator):
    """The default paginator used by this application."""

    def page(self, number):
        number = self.validate_number(number)
        if number == 1:
            bottom = 0
        else:
            bottom = (number - 2) * self.per_page + self.first_page
        top = bottom + self.get_current_per_page(number)
        if top + self.orphans >= self.count:
            top = self.count
        return CustomPage(self.object_list[bottom:top], number, self)

    def _get_num_pages(self):
        if self._num_pages is None:
            if self.count == 0 and not self.allow_empty_first_page:
                self._num_pages = 0
            else:
                hits = max(0, self.count - self.orphans - self.first_page)
                try:
                    self._num_pages = int(ceil(hits / float(self.per_page))) + 1
                except ZeroDivisionError:
                    self._num_pages = 0  # fallback to a safe value
        return self._num_pages

    num_pages = property(_get_num_pages)


class LazyPaginator(BasePaginator):
    """Implement lazy pagination."""

    def validate_number(self, number):
        try:
            number = int(number)
        except ValueError:
            raise PageNotAnInteger('That page number is not an integer')
        if number < 1:
            raise EmptyPage('That page number is less than 1')
        return number

    def page(self, number):
        number = self.validate_number(number)
        current_per_page = self.get_current_per_page(number)
        if number == 1:
            bottom = 0
        else:
            bottom = (number - 2) * self.per_page + self.first_page
        top = bottom + current_per_page
        # Retrieve more objects to check if there is a next page.
        objects = list(self.object_list[bottom : top + self.orphans + 1])
        objects_count = len(objects)
        if objects_count > (current_per_page + self.orphans):
            # If another page is found, increase the total number of pages.
            self._num_pages = number + 1
            # In any case,  return only objects for this page.
            objects = objects[:current_per_page]
        elif (number != 1) and (objects_count <= self.orphans):
            raise EmptyPage('That page contains no results')
        else:
            # This is the last page.
            self._num_pages = number
        return CustomPage(objects, number, self)

    def _get_count(self):
        raise NotImplementedError

    count = property(_get_count)

    def _get_num_pages(self):
        return self._num_pages

    num_pages = property(_get_num_pages)

    def _get_page_range(self):
        raise NotImplementedError

    page_range = property(_get_page_range)
