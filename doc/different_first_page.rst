Different number of items on the first page
===========================================

Sometimes you might want to show on the first page a different number of
items than on subsequent pages (e.g. in a movie detail page you want to show
4 images of the movie as a reminder, making the user click to see the next 20
images). To achieve this, use the :ref:`templatetags-paginate` or
:ref:`templatetags-lazy-paginate` tags with comma separated *first page* and
*per page* arguments, e.g.:

.. code-block:: html+django

    {% load endless %}

    {% lazy_paginate 4,20 entries %}
    {% for entry in entries %}
        {# your code to show the entry #}
    {% endfor %}
    {% show_more %}

This code will display 4 entries on the first page and 20 entries on the other
pages.

Of course the *first page* and *per page* arguments can be passed
as template variables, e.g.:

.. code-block:: html+django

    {% lazy_paginate first_page,per_page entries %}
