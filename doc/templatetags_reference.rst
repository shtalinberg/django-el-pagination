Templatetags reference
======================

.. _templatetags-paginate:

paginate
~~~~~~~~

Usage:

.. code-block:: html+django

    {% paginate entries %}

After this call, the *entries* variable in the template context is replaced
by only the entries of the current page.

You can also keep your *entries* original variable (usually a queryset)
and add to the context another name that refers to entries of the current page,
e.g.:

.. code-block:: html+django

    {% paginate entries as page_entries %}

The *as* argument is also useful when a nested context variable is provided
as queryset. In this case, and only in this case, the resulting variable
name is mandatory, e.g.:

.. code-block:: html+django

    {% paginate entries.all as entries %}

The number of paginated entries is taken from settings, but you can
override the default locally, e.g.:

.. code-block:: html+django

    {% paginate 20 entries %}

Of course you can mix it all:

.. code-block:: html+django

    {% paginate 20 entries as paginated_entries %}

By default, the first page is displayed the first time you load the page,
but you can change this, e.g.:

.. code-block:: html+django

    {% paginate entries starting from page 3 %}

When changing the default page, it is also possible to reference the last
page (or the second last page, and so on) by using negative indexes, e.g:

.. code-block:: html+django

    {% paginate entries starting from page -1 %}

This can be also achieved using a template variable that was passed to the
context, e.g.:

.. code-block:: html+django

    {% paginate entries starting from page page_number %}

If the passed page number does not exist, the first page is displayed.
Note that negative indexes are specific to the ``{% paginate %}`` tag: this
feature cannot be used when contents are lazy paginated (see `lazy_paginate`_
below).

If you have multiple paginations in the same page, you can change the
querydict key for the single pagination, e.g.:

.. code-block:: html+django

    {% paginate entries using article_page %}

In this case *article_page* is intended to be a context variable, but you can
hardcode the key using quotes, e.g.:

.. code-block:: html+django

    {% paginate entries using 'articles_at_page' %}

Again, you can mix it all (the order of arguments is important):

.. code-block:: html+django

    {% paginate 20 entries starting from page 3 using page_key as paginated_entries %}

Additionally you can pass a path to be used for the pagination:

.. code-block:: html+django

    {% paginate 20 entries using page_key with pagination_url as paginated_entries %}

This way you can easily create views acting as API endpoints, and point your
Ajax calls to that API. In this case *pagination_url* is considered a
context variable, but it is also possible to hardcode the URL, e.g.:

.. code-block:: html+django

    {% paginate 20 entries with "/mypage/" %}

If you want the first page to contain a different number of items than
subsequent pages, you can separate the two values with a comma, e.g. if
you want 3 items on the first page and 10 on other pages:

.. code-block:: html+django

    {% paginate 3,10 entries %}

You must use this tag before calling the `show_more`_, `get_pages`_ or
`show_pages`_ ones.

.. _templatetags-lazy-paginate:

lazy_paginate
~~~~~~~~~~~~~

Paginate objects without hitting the database with a *select count* query.
Usually pagination requires hitting the database to get the total number of
items to display. Lazy pagination avoids this *select count* query and results
in a faster page load, with a disadvantage: you won't know the total number of
pages in advance.

Use this in the same way as `paginate`_ tag when you are not interested in the
total number of pages.

The ``lazy_paginate`` tag can take all the args of the ``paginate`` one, with
one exception: negative indexes can not be passed to the ``starting from page``
argument.

.. _templatetags-show-more:

show_more
~~~~~~~~~

Show the link to get the next page in a :doc:`twitter_pagination`. Usage:

.. code-block:: html+django

    {% show_more %}

Alternatively you can override the label passed to the default template:

.. code-block:: html+django

    {% show_more "even more" %}

You can override the loading text too:

.. code-block:: html+django

    {% show_more "even more" "working" %}

Must be called after `paginate`_ or `lazy_paginate`_.

.. _templatetags-get-pages:

get_pages
~~~~~~~~~

Usage:

.. code-block:: html+django

    {% get_pages %}

This is mostly used for :doc:`digg_pagination`.

This call inserts in the template context a *pages* variable, as a sequence
of page links. You can use *pages* in different ways:

- just print *pages* and you will get Digg-style pagination displayed:

.. code-block:: html+django

    {{ pages }}

- display pages count:

.. code-block:: html+django

    {{ pages|length }}

- check if the page list contains more than one page:

.. code-block:: html+django

    {{ pages.paginated }}
    {# the following is equivalent #}
    {{ pages|length > 1 }}

- get a specific page:

.. code-block:: html+django

    {# the current selected page #}
    {{ pages.current }}

    {# the first page #}
    {{ pages.first }}

    {# the last page #}
    {{ pages.last }}

    {# the previous page (or nothing if you are on first page) #}
    {{ pages.previous }}

    {# the next page (or nothing if you are in last page) #}
    {{ pages.next }}

    {# the third page #}
    {{ pages.3 }}
    {# this means page.1 is the same as page.first #}

    {# the 1-based index of the first item on the current page #}
    {{ pages.current_start_index }}

    {# the 1-based index of the last item on the current page #}
    {{ pages.current_end_index }}

    {# the total number of objects, across all pages #}
    {{ pages.total_count }}

    {# the first page represented as an arrow #}
    {{ pages.first_as_arrow }}

    {# the last page represented as an arrow #}
    {{ pages.last_as_arrow }}

- iterate over *pages* to get all pages:

.. code-block:: html+django

    {% for page in pages %}
        {# display page link #}
        {{ page }}

        {# the page url (beginning with "?") #}
        {{ page.url }}

        {# the page path #}
        {{ page.path }}

        {# the page number #}
        {{ page.number }}

        {# a string representing the page (commonly the page number) #}
        {{ page.label }}

        {# check if the page is the current one #}
        {{ page.is_current }}

        {# check if the page is the first one #}
        {{ page.is_first }}

        {# check if the page is the last one #}
        {{ page.is_last }}
    {% endfor %}

You can change the variable name, e.g.:

.. code-block:: html+django

    {% get_pages as page_links %}

This must be called after `paginate`_ or `lazy_paginate`_.

.. _templatetags-show-pages:

show_pages
~~~~~~~~~~

Show page links. Usage:

.. code-block:: html+django

    {% show_pages %}

It is just a shortcut for:

.. code-block:: html+django

    {% get_pages %}
    {{ pages }}

You can set ``ENDLESS_PAGINATION_PAGE_LIST_CALLABLE`` in your *settings.py* to
a callable used to customize the pages that are displayed.
``ENDLESS_PAGINATION_PAGE_LIST_CALLABLE`` can also be a dotted path
representing a callable, e.g.::

    ENDLESS_PAGINATION_PAGE_LIST_CALLABLE = 'path.to.callable'

The callable takes the current page number and the total number of pages,
and must return a sequence of page numbers that will be displayed.

The sequence can contain other values:

- *'previous'*: will display the previous page in that position;
- *'next'*: will display the next page in that position;
- *'first'*: will display the first page as an arrow;
- *'last'*: will display the last page as an arrow;
- *None*: a separator will be displayed in that position.

Here is an example of a custom callable that displays the previous page, then
the first page, then a separator, then the current page, and finally the last
page::

    def get_page_numbers(current_page, num_pages):
        return ('previous', 1, None, current_page, 'last')

If ``ENDLESS_PAGINATION_PAGE_LIST_CALLABLE`` is *None* the internal callable
``endless_pagination.utils.get_page_numbers`` is used, generating a Digg-style
pagination.

An alternative implementation is available:
``endless_pagination.utils.get_elastic_page_numbers``: it adapts its output
to the number of pages, making it arguably more usable when there are many
of them.

This must be called after `paginate`_ or `lazy_paginate`_.

.. _templatetags-show-current-number:

show_current_number
~~~~~~~~~~~~~~~~~~~

Show the current page number, or insert it in the context.

This tag can for example be useful to change the page title according to
the current page number.

To just show current page number:

.. code-block:: html+django

    {% show_current_number %}

If you use multiple paginations in the same page, you can get the page
number for a specific pagination using the querystring key, e.g.:

.. code-block:: html+django

    {% show_current_number using mykey %}

The default page when no querystring is specified is 1. If you changed it
in the `paginate`_ template tag, you have to call  ``show_current_number``
according to your choice, e.g.:

.. code-block:: html+django

    {% show_current_number starting from page 3 %}

This can be also achieved using a template variable you passed to the
context, e.g.:

.. code-block:: html+django

    {% show_current_number starting from page page_number %}

You can of course mix it all (the order of arguments is important):

.. code-block:: html+django

    {% show_current_number starting from page 3 using mykey %}

If you want to insert the current page number in the context, without
actually displaying it in the template, use the *as* argument, i.e.:

.. code-block:: html+django

    {% show_current_number as page_number %}
    {% show_current_number starting from page 3 using mykey as page_number %}
