Multiple paginations in the same page
=====================================

Sometimes it is necessary to show different types of paginated objects in the
same page. In this case we have to associate a different querystring key
to every pagination.

Normally, the key used is the one specified in
``settings.ENDLESS_PAGINATION_PAGE_LABEL`` (see :doc:`customization`),
but in the case of multiple pagination the application provides a simple way to
override the settings.

If you do not need Ajax, the only file you need to edit is the template.
Here is an example with 2 different paginations (*entries* and *other_entries*)
in the same page, but there is no limit to the number of different paginations
in a page:

.. code-block:: html+django

    {% load endless %}

    {% paginate entries %}
    {% for entry in entries %}
        {# your code to show the entry #}
    {% endfor %}
    {% show_pages %}

    {# "other_entries_page" is the new querystring key #}
    {% paginate other_entries using "other_entries_page" %}
    {% for entry in other_entries %}
        {# your code to show the entry #}
    {% endfor %}
    {% show_pages %}

The ``using`` argument of the :ref:`templatetags-paginate` template tag allows
you to choose the name of the querystring key used to track the page number.
If not specified the system falls back to
``settings.ENDLESS_PAGINATION_PAGE_LABEL``.

In the example above, the url *http://example.com?page=2&other_entries_page=3*
requests the second page of *entries* and the third page of *other_entries*.

The name of the querystring key can also be dinamically passed in the template
context, e.g.:

.. code-block:: html+django

    {# page_variable is not surrounded by quotes #}
    {% paginate other_entries using page_variable %}

You can use any style of pagination: :ref:`templatetags-show-pages`,
:ref:`templatetags-get-pages`, :ref:`templatetags-show-more` etc...
(see :doc:`templatetags_reference`).

Adding Ajax for multiple pagination
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Obviously each pagination needs a template for the page contents. Remember to
box each page in a div with a class called *endless_page_template*, or to
specify the container selector passing an option to *$.endlessPaginate()* as
seen in :ref:`Digg-style pagination and Ajax<digg-ajax>`.

*myapp/entry_index.html*:

.. code-block:: html+django

    <h2>Entries:</h2>
    <div class="endless_page_template">
        {% include "myapp/entries_page.html" %}
    </div>

    <h2>Other entries:</h2>
    <div class="endless_page_template">
        {% include "myapp/other_entries_page.html" %}
    </div>

    {% block js %}
        {{ block.super }}
        <script src="http://code.jquery.com/jquery-latest.js"></script>
        <script src="{{ STATIC_URL }}endless_pagination/js/endless-pagination.js"></script>
        <script>$.endlessPaginate();</script>
    {% endblock %}

See the :doc:`javascript` for further details on how to use the included
jQuery plugin.

*myapp/entries_page.html*:

.. code-block:: html+django

    {% load endless %}

    {% paginate entries %}
    {% for entry in entries %}
        {# your code to show the entry #}
    {% endfor %}
    {% show_pages %}

*myapp/other_entries_page.html*:

.. code-block:: html+django

    {% load endless %}

    {% paginate other_entries using other_entries_page %}
    {% for entry in other_entries %}
        {# your code to show the entry #}
    {% endfor %}
    {% show_pages %}

As seen :ref:`before<twitter-page-template>`, the decorator ``page_template``
simplifies the management of Ajax requests in views. You must, however, map
different paginations to different page templates.

You can chain decorator calls relating a template to the associated
querystring key, e.g.::

    from endless_pagination.decorators import page_template

    @page_template('myapp/entries_page.html')
    @page_template('myapp/other_entries_page.html', key='other_entries_page')
    def entry_index(
            request, template='myapp/entry_index.html', extra_context=None):
        context = {
            'entries': Entry.objects.all(),
            'other_entries': OtherEntry.objects.all(),
        }
        if extra_context is not None:
            context.update(extra_context)
        return render_to_response(
            template, context, context_instance=RequestContext(request))

As seen in previous examples, if you do not specify the *key* kwarg in the
decorator, then the page template is associated to the querystring key
defined in the settings.

.. _multiple-page-templates:

You can use the ``page_templates`` (note the trailing *s*) decorator in
substitution of a decorator chain when you need multiple Ajax paginations.
The previous example can be written as::

    from endless_pagination.decorators import page_templates

    @page_templates({
        'myapp/entries_page.html': None,
        'myapp/other_entries_page.html': 'other_entries_page',
    })
    def entry_index():
        ...

As seen, a dict object is passed to the ``page_templates`` decorator, mapping
templates to querystring keys. Alternatively, you can also pass a sequence
of ``(template, key)`` pairs, e.g.::

    from endless_pagination.decorators import page_templates

    @page_templates((
        ('myapp/entries_page.html', None),
        ('myapp/other_entries_page.html', 'other_entries_page'),
    ))
    def entry_index():
        ...

This also supports serving different paginated objects with the same template.

Manually selecting what to bind
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

What if you need Ajax pagination only for *entries* and not for
*other entries*? You can do this in a straightforward way using jQuery
selectors, e.g.:

.. code-block:: html+django

    {% block js %}
        {{ block.super }}
        <script src="http://code.jquery.com/jquery-latest.js"></script>
        <script src="{{ STATIC_URL }}endless_pagination/js/endless-pagination.js"></script>
        <script>$('#entries').endlessPaginate();</script>
    {% endblock %}

The call to *$('#entries').endlessPaginate()* applies Ajax pagination starting
from the DOM node with id *entries* and to all sub-nodes. This means that
*other entries* are left intact. Of course you can use any selector supported
by jQuery.

Refer to the :doc:`javascript` for an explanation of other features like
calling *$.endlessPaginate()* multiple times in order to customize the behavior
of each pagination in a multiple pagination view.
