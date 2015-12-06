Getting the current page number
===============================

In the template
~~~~~~~~~~~~~~~

You can get and display the current page number in the template using
the :ref:`templatetags-show-current-number` template tag, e.g.:

.. code-block:: html+django

    {% show_current_number %}

This call will display the current page number, but you can also
insert the value in the context as a template variable:

.. code-block:: html+django


    {% show_current_number as page_number %}
    {{ page_number }}

See the :ref:`templatetags-show-current-number` refrence for more information
on accepted arguments.

In the view
~~~~~~~~~~~

If you need to get the current page number in the view, you can use an utility
function called ``get_page_number_from_request``, e.g.::

    from endless_pagination import utils

    page = utils.get_page_number_from_request(request)

If you are using :doc:`multiple pagination<multiple_pagination>`, or you have
changed the default querystring for pagination, you can pass the querystring
key as an optional argument::

    page = utils.get_page_number_from_request(request, querystring_key=mykey)

If the page number is not present in the request, by default *1* is returned.
You can change this behaviour using::

    page = utils.get_page_number_from_request(request, default=3)

