Changelog
=========

Version 2.0
~~~~~~~~~~~

**New feature**: Python 3 support.

Django Endless Pagination now supports both Python 2 and **Python 3**. Dropped
support for Python 2.5. See :doc:`start` for the new list of requirements.

----

**New feature**: the **JavaScript refactoring**.

This version introduces a re-designed Ajax support for pagination. Ajax can
now be enabled using a brand new jQuery plugin that can be found in
``static/endless_pagination/js/endless-pagination.js``.

Usage:

.. code-block:: html+django

    {% block js %}
        {{ block.super }}
        <script src="http://code.jquery.com/jquery-latest.js"></script>
        <script src="{{ STATIC_URL }}endless_pagination/js/endless-pagination.js"></script>
        <script>$.endlessPaginate();</script>
    {% endblock %}

The last line in the block above enables Ajax requests to retrieve new
pages for each pagination in the page. That's basically the same as the old
approach of loading the file ``endless.js``. The new approach, however,
is more jQuery-idiomatic, increases the flexibility of how objects can be
paginated, implements some :doc:`new features </javascript>` and also contains
some bug fixes.

For backward compatibility, the application still includes the two JavaScript
``endless.js`` and ``endless_on_scroll.js`` files. However, please consider
:ref:`migrating<javascript-migrate>` as soon as possible: the old JavaScript
files are deprecated, are no longer maintained, and don't provide the new
JavaScript features. Also note that the old Javascript files will not work if
jQuery >= 1.9 is used.

New features include ability to **paginate different objects with different
options**, precisely **selecting what to bind**, ability to **register
callbacks**, support for **pagination in chunks** and much more.

Please refer to the :doc:`javascript` for a detailed overview of the new
features and for instructions on :ref:`how to migrate<javascript-migrate>` from
the old JavaScript files to the new one.

----

**New feature**: the :ref:`page_templates<multiple-page-templates>` decorator
also accepts a sequence of ``(template, key)`` pairs, functioning as a dict
mapping templates and keys (still present), e.g.::

    from endless_pagination.decorators import page_templates

    @page_templates((
        ('myapp/entries_page.html', None),
        ('myapp/other_entries_page.html', 'other_entries_page'),
    ))
    def entry_index():
        ...

This also supports serving different paginated objects with the same template.

----

**New feature**: ability to provide nested context variables in the
:ref:`templatetags-paginate` and :ref:`templatetags-lazy-paginate` template
tags, e.g.:

.. code-block:: html+django

    {% paginate entries.all as myentries %}

The code above is basically equivalent to:

.. code-block:: html+django

    {% with entries.all as myentries %}
        {% paginate myentries %}
    {% endwith %}

In this case, and only in this case, the `as` argument is mandatory, and a
*TemplateSyntaxError* will be raised if the variable name is missing.

----

**New feature**: the page list object returned by the
:ref:`templatetags-get-pages` template tag has been improved adding the
following new methods:

.. code-block:: html+django

    {# whether the page list contains more than one page #}
    {{ pages.paginated }}

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

In the *arrow* representation, the page label defaults to ``<<`` for the first
page and to ``>>`` for the last one. As a consequence, the labels of the
previous and next pages are now single brackets, respectively ``<`` and ``>``.
First and last pages' labels can be customized using
``settings.ENDLESS_PAGINATION_FIRST_LABEL`` and
``settings.ENDLESS_PAGINATION_LAST_LABEL``: see :doc:`customization`.

----

**New feature**: The sequence returned by the callable
``settings.ENDLESS_PAGINATION_PAGE_LIST_CALLABLE`` can now contain two new
values:

- *'first'*: will display the first page as an arrow;
- *'last'*: will display the last page as an arrow.

The :ref:`templatetags-show-pages` template tag documentation describes how to
customize Digg-style pagination defining your own page list callable.

When using the default Digg-style pagination (i.e. when
``settings.ENDLESS_PAGINATION_PAGE_LIST_CALLABLE`` is set to *None*), it is
possible to enable first / last page arrows by setting the new flag
``settings.ENDLESS_PAGINATION_DEFAULT_CALLABLE_ARROWS`` to *True*.

----

**New feature**: ``settings.ENDLESS_PAGINATION_PAGE_LIST_CALLABLE`` can now be
either a callable or a **dotted path** to a callable, e.g.::

    ENDLESS_PAGINATION_PAGE_LIST_CALLABLE = 'path.to.callable'

In addition to the default, ``endless_pagination.utils.get_page_numbers``, an
alternative implementation is now available:
``endless_pagination.utils.get_elastic_page_numbers``. It adapts its output
to the number of pages, making it arguably more usable when there are many
of them. To enable it, add the following line to your ``settings.py``::

    ENDLESS_PAGINATION_PAGE_LIST_CALLABLE = (
        'endless_pagination.utils.get_elastic_page_numbers')

----

**New feature**: ability to create a development and testing environment
(see :doc:`contributing`).

----

**New feature**: in addition to the ability to provide a customized pagination
URL as a context variable, the :ref:`templatetags-paginate` and
:ref:`templatetags-lazy-paginate` tags now support hardcoded pagination URL
endpoints, e.g.:

.. code-block:: html+django

    {% paginate 20 entries with "/mypage/" %}

----

**New feature**: ability to specify negative indexes as values for the
``starting from page`` argument of the :ref:`templatetags-paginate` template
tag.

When changing the default page, it is now possible to reference the last page
(or the second last page, and so on) by using negative indexes, e.g:

.. code-block:: html+django

    {% paginate entries starting from page -1 %}

See :doc:`templatetags_reference`.

----

**Documentation**: general clean up.

----

**Documentation**: added a :doc:`contributing` page. Have a look!

----

**Documentation**: included a comprehensive :doc:`javascript`.

----

**Fix**: ``endless_pagination.views.AjaxListView`` no longer subclasses
``django.views.generic.list.ListView``. Instead, the base objects and
mixins composing the final view are now defined by this app.

This change eliminates the ambiguity of having two separate pagination
machineries in place: the Django Endless Pagination one and the built-in
Django ``ListView`` one.

----

**Fix**: the *using* argument of :ref:`templatetags-paginate` and
:ref:`templatetags-lazy-paginate` template tags now correctly handles
querystring keys containing dashes, e.g.:

.. code-block:: html+django

    {% lazy_paginate entries using "entries-page" %}

----

**Fix**: replaced namespace ``endless_pagination.paginator`` with
``endless_pagination.paginators``: the module contains more than one
paginator classes.

----

**Fix**: in some corner cases, loading ``endless_pagination.models`` raised
an *ImproperlyConfigured* error while trying to pre-load the templates.

----

**Fix**: replaced doctests with proper unittests. Improved the code coverage
as a consequence. Also introduced integration tests exercising JavaScript,
based on Selenium.

----

**Fix**: overall code lint and clean up.


Version 1.1
~~~~~~~~~~~

**New feature**: now it is possible to set the bottom margin used for
pagination on scroll (default is 1 pixel).

For example, if you want the pagination on scroll to be activated when
20 pixels remain until the end of the page:

.. code-block:: html+django

    <script src="http://code.jquery.com/jquery-latest.js"></script>
    <script src="{{ STATIC_URL }}endless_pagination/js/endless.js"></script>
    <script src="{{ STATIC_URL }}endless_pagination/js/endless_on_scroll.js"></script>

    {# add the lines below #}
    <script type="text/javascript" charset="utf-8">
        var endless_on_scroll_margin = 20;
    </script>

----

**New feature**: added ability to avoid Ajax requests when multiple pagination
is used.

A template for multiple pagination with Ajax support may look like this
(see :doc:`multiple_pagination`):

.. code-block:: html+django

    {% block js %}
        {{ block.super }}
        <script src="http://code.jquery.com/jquery-latest.js"></script>
        <script src="{{ STATIC_URL }}endless_pagination/js/endless.js"></script>
    {% endblock %}

    <h2>Entries:</h2>
    <div class="endless_page_template">
        {% include "myapp/entries_page.html" %}
    </div>

    <h2>Other entries:</h2>
    <div class="endless_page_template">
        {% include "myapp/other_entries_page.html" %}
    </div>

But what if you need Ajax pagination for *entries* but not for *other entries*?
You will only have to add a class named ``endless_page_skip`` to the
page container element, e.g.:

.. code-block:: html+django

    <h2>Other entries:</h2>
    <div class="endless_page_template endless_page_skip">
        {% include "myapp/other_entries_page.html" %}
    </div>

----

**New feature**: implemented a class-based generic view allowing
Ajax pagination of a list of objects (usually a queryset).

Intended as a substitution of *django.views.generic.ListView*, it recreates
the behaviour of the *page_template* decorator.

For a complete explanation, see :doc:`generic_views`.

----

**Fix**: the ``page_template`` and ``page_templates`` decorators no longer
hide the original view name and docstring (*update_wrapper*).

----

**Fix**: pagination on scroll now works on Firefox >= 4.

----

**Fix**: tests are now compatible with Django 1.3.
