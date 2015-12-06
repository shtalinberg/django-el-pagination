Lazy pagination
===============

Usually pagination requires hitting the database to get the total number of
items to display. Lazy pagination avoids this *select count* query and results
in a faster page load, with a disadvantage: you won't know the total number of
pages in advance.

For this reason it is better to use lazy pagination in conjunction with
:doc:`twitter_pagination` (e.g. using the :ref:`templatetags-show-more`
template tag).

In order to switch to lazy pagination you have to use the
:ref:`templatetags-lazy-paginate` template tag instead of the
:ref:`templatetags-paginate` one, e.g.:

.. code-block:: html+django

    {% load endless %}

    {% lazy_paginate entries %}
    {% for entry in entries %}
        {# your code to show the entry #}
    {% endfor %}
    {% show_more %}

The :ref:`templatetags-lazy-paginate` tag can take all the args of the
:ref:`templatetags-paginate` one, with one exception: negative indexes can not
be passed to the ``starting from page`` argument.
