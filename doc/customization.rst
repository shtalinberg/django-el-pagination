Customization
=============

Settings
~~~~~~~~

You can customize the application using ``settings.py``.

================================================= =========== ==============================================
Name                                              Default     Description
================================================= =========== ==============================================
``ENDLESS_PAGINATION_PER_PAGE``                   10          How many objects are normally displayed
                                                              in a page (overwriteable by templatetag).
------------------------------------------------- ----------- ----------------------------------------------
``ENDLESS_PAGINATION_PAGE_LABEL``                 'page'      The querystring key of the page number
                                                              (e.g. ``http://example.com?page=2``).
------------------------------------------------- ----------- ----------------------------------------------
``ENDLESS_PAGINATION_ORPHANS``                    0           See Django *Paginator* definition of orphans.
------------------------------------------------- ----------- ----------------------------------------------
``ENDLESS_PAGINATION_LOADING``                    'loading'   If you use the default ``show_more`` template,
                                                              here you can customize the content of the
                                                              loader hidden element. HTML is safe here,
                                                              e.g. you can show your pretty animated GIF
                                                              ``ENDLESS_PAGINATION_LOADING = """<img src="/static/img/loader.gif" alt="loading" />"""``.
------------------------------------------------- ----------- ----------------------------------------------
``ENDLESS_PAGINATION_PREVIOUS_LABEL``             '<'         Default label for the *previous* page link.
------------------------------------------------- ----------- ----------------------------------------------
``ENDLESS_PAGINATION_NEXT_LABEL``                 '>'         Default label for the *next* page link.
------------------------------------------------- ----------- ----------------------------------------------
``ENDLESS_PAGINATION_FIRST_LABEL``                '<<'        Default label for the *first* page link.
------------------------------------------------- ----------- ----------------------------------------------
``ENDLESS_PAGINATION_LAST_LABEL``                 '>>'        Default label for the *last* page link.
------------------------------------------------- ----------- ----------------------------------------------
``ENDLESS_PAGINATION_ADD_NOFOLLOW``               *False*     Set to *True* if your SEO alchemist
                                                              wants search engines not to follow
                                                              pagination links.
------------------------------------------------- ----------- ----------------------------------------------
``ENDLESS_PAGINATION_PAGE_LIST_CALLABLE``         *None*      Callable (or dotted path to a callable) that
                                                              returns pages to be displayed.
                                                              If *None*, a default callable is used;
                                                              that produces :doc:`digg_pagination`.
                                                              The applicationt provides also a callable
                                                              producing elastic pagination:
                                                              ``endless_pagination.utils.get_elastic_page_numbers``.
                                                              It adapts its output to the number of pages,
                                                              making it arguably more usable when there are
                                                              many of them.
                                                              See :doc:`templatetags_reference` for
                                                              information about writing custom callables.
------------------------------------------------- ----------- ----------------------------------------------
``ENDLESS_PAGINATION_DEFAULT_CALLABLE_EXTREMES``  3           Deafult number of *extremes* displayed when
                                                              :doc:`digg_pagination` is used with the
                                                              default callable.
------------------------------------------------- ----------- ----------------------------------------------
``ENDLESS_PAGINATION_DEFAULT_CALLABLE_AROUNDS``   2           Deafult number of *arounds* displayed when
                                                              :doc:`digg_pagination` is used with the
                                                              default callable.
------------------------------------------------- ----------- ----------------------------------------------
``ENDLESS_PAGINATION_DEFAULT_CALLABLE_ARROWS``    *False*     Whether or not the first and last pages arrows
                                                              are displayed when :doc:`digg_pagination` is
                                                              used with the default callable.
------------------------------------------------- ----------- ----------------------------------------------
``ENDLESS_PAGINATION_TEMPLATE_VARNAME``           'template'  Template variable name used by the
                                                              ``page_template`` decorator. You can change
                                                              this value if you are going to decorate
                                                              generic views using a different variable name
                                                              for the template (e.g. ``template_name``).
================================================= =========== ==============================================

Templates and CSS
~~~~~~~~~~~~~~~~~

You can override the default template for ``show_more`` templatetag following
some rules:

- *more* link is shown only if the variable ``querystring`` is not False;
- the container (most external html element) class is *endless_container*;
- the *more* link and the loader hidden element live inside the container;
- the *more* link class is *endless_more*;
- the *more* link rel attribute is ``{{ querystring_key }}``;
- the loader hidden element class is *endless_loading*.
