Generic views
=============

This application provides a customized class-based view, similar to
*django.views.generic.ListView*, that allows Ajax pagination of a
list of objects (usually a queryset).

AjaxListView reference
~~~~~~~~~~~~~~~~~~~~~~

.. py:module:: el_pagination.views

.. py:class:: AjaxListView(django.views.generic.ListView)

    A class based view, similar to *django.views.generic.ListView*,
    that allows Ajax pagination of a list of objects.

    You can use this class based view in place of *ListView* in order to
    recreate the behaviour of the *page_template* decorator.

    For instance, assume you have this code (taken from Django docs)::

        from django.conf.urls import url
        from django.views.generic import ListView
        from books.models import Publisher

        urlpatterns = [
            url(r'^publishers/$', ListView.as_view(model=Publisher)),
        ]


    You want to Ajax paginate publishers, so, as seen, you need to switch
    the template if the request is Ajax and put the page template
    into the context as a variable named *page_template*.

    This is straightforward, you only need to replace the view class, e.g.::

        from django.conf.urls import *
        from books.models import Publisher

        from el_pagination.views import AjaxListView

        urlpatterns = [
            url(r'^publishers/$', AjaxListView.as_view(model=Publisher)),
        ]


    .. py:attribute:: key

        the querystring key used for the current pagination
        (default: *settings.EL_PAGINATION_PAGE_LABEL*)

    .. py:attribute:: page_template

        the template used for the paginated objects

    .. py:attribute:: page_template_suffix

        the template suffix used for autogenerated page_template name
        (when not given, default='_page')


    .. py:method:: get_context_data(self, **kwargs)

        Adds the *page_template* variable in the context.

        If the *page_template* is not given as a kwarg of the *as_view*
        method then it is invented using app label, model name
        (obviously if the list is a queryset), *self.template_name_suffix*
        and *self.page_template_suffix*.

        For instance, if the list is a queryset of *blog.Entry*,
        the template will be *myapp/publisher_list_page.html*.

    .. py:method:: get_template_names(self)

        Switch the templates for Ajax requests.

    .. py:method:: get_page_template(self, **kwargs)

        Only called if *page_template* is not given as a kwarg of
        *self.as_view*.


Generic view example
~~~~~~~~~~~~~~~~~~~~
If the developer wants pagination of publishers, in *views.py* we have code class-based::

    from django.views.generic import ListView

    class EntryListView(ListView)
        model = Publisher
        template_name = "myapp/publisher_list.html"
        context_object_name = "publisher_list"

or function-based::

    def entry_index(request, template='myapp/publisher_list.html'):
        context = {
            'publisher_list': Entry.objects.all(),
        }
        return render(request, template, context)

In *myapp/publisher_list.html*:

.. code-block:: html+django

	<h2>Entries:</h2>
	{% for entry in publisher_list %}
	    {# your code to show the entry #}
	{% endfor %}

This is just a basic example. To continue exploring more AjaxListView examples,
have a look at :doc:`twitter_pagination`

