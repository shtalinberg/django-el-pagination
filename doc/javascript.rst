JavaScript reference
====================

For each type of pagination it is possible to enable Ajax so that the requested
page is loaded using an asynchronous request to the server. This is especially
important for :doc:`twitter_pagination` and
:ref:`endless pagination on scroll<javascript-pagination-on-scroll>`, but
:doc:`digg_pagination` can also take advantage of this technique.

Activating Ajax support
~~~~~~~~~~~~~~~~~~~~~~~

Ajax support is activated linking jQuery and the ``endless-pagination.js`` file
included in this app. It is then possible to use the *$.endlessPaginate()*
jQuery plugin to enable Ajax pagination, e.g.:

.. code-block:: html+django

    <h2>Entries:</h2>
    <div class="endless_page_template">
        {% include page_template %}
    </div>

    {% block js %}
        {{ block.super }}
        <script src="http://code.jquery.com/jquery-latest.js"></script>
        <script src="{{ STATIC_URL }}endless_pagination/js/endless-pagination.js"></script>
        <script>$.endlessPaginate();</script>
    {% endblock %}

This example assumes that you
:ref:`separated the fragment<twitter-split-template>` containing the single
page (*page_tempate*) from the main template (the code snipper above). More on
this in :doc:`twitter_pagination` and :doc:`digg_pagination`.

The *$.endlessPaginate()* call activates Ajax for each pagination present in
the page.

.. _javascript-pagination-on-scroll:

Pagination on scroll
~~~~~~~~~~~~~~~~~~~~

If you want new items to load when the user scrolls down the browser page,
you can use the **pagination on scroll** feature: just set the
*paginateOnScroll* option of *$.endlessPaginate()* to *true*, e.g.:

.. code-block:: html+django

    <h2>Entries:</h2>
    <div class="endless_page_template">
        {% include page_template %}
    </div>

    {% block js %}
        {{ block.super }}
        <script src="http://code.jquery.com/jquery-latest.js"></script>
        <script src="{{ STATIC_URL }}endless_pagination/js/endless-pagination.js"></script>
        <script>$.endlessPaginate({paginateOnScroll: true});</script>
    {% endblock %}

That's all. See the :doc:`templatetags_reference` page to improve usage of
the included templatetags.

It is possible to set the **bottom margin** used for pagination on scroll
(default is 1 pixel). For example, if you want the pagination on scroll
to be activated when 20 pixels remain to the end of the page:

.. code-block:: html+django

    <h2>Entries:</h2>
    <div class="endless_page_template">
        {% include page_template %}
    </div>

    {% block js %}
        {{ block.super }}
        <script src="http://code.jquery.com/jquery-latest.js"></script>
        <script src="{{ STATIC_URL }}endless_pagination/js/endless-pagination.js"></script>
        <script>
            $.endlessPaginate({
                paginateOnScroll: true,
                paginateOnScrollMargin: 20
            });
        </script>
    {% endblock %}

Attaching callbacks
~~~~~~~~~~~~~~~~~~~

It is possible to customize the behavior of JavaScript pagination by attaching
callbacks to *$.endlessPaginate()*, called when the following events are fired:

- *onClick*: the user clicks on a page link;
- *onCompleted*: the new page is fully loaded and inserted in the DOM.

The context of both callbacks is the clicked link fragment: in other words,
inside the callbacks, *this* will be the HTML fragment representing the clicked
link, e.g.:

.. code-block:: html+django

    <h2>Entries:</h2>
    <div class="endless_page_template">
        {% include page_template %}
    </div>

    {% block js %}
        {{ block.super }}
        <script src="http://code.jquery.com/jquery-latest.js"></script>
        <script src="{{ STATIC_URL }}endless_pagination/js/endless-pagination.js"></script>
        <script>
            $.endlessPaginate({
                onClick: function() {
                    console.log('Label:', $(this).text());
                }
            });
        </script>
    {% endblock %}

Both callbacks also receive a *context* argument containing information about
the requested page:

- *context.url*: the requested URL;
- *context.key*: the querystring key used to retrieve the requested contents.

If the *onClick* callback returns *false*, the pagination process is stopped,
the Ajax request is not performed and the *onCompleted* callback never called.

The *onCompleted* callbacks also receives a second argument: the data returned
by the server. Basically this is the HTML fragment representing the new
requested page.

To wrap it up, here is an example showing the callbacks' signatures:

.. code-block:: html+django

    <h2>Entries:</h2>
    <div class="endless_page_template">
        {% include page_template %}
    </div>

    {% block js %}
        {{ block.super }}
        <script src="http://code.jquery.com/jquery-latest.js"></script>
        <script src="{{ STATIC_URL }}endless_pagination/js/endless-pagination.js"></script>
        <script>
            $.endlessPaginate({
                onClick: function(context) {
                    console.log('Label:', $(this).text());
                    console.log('URL:', context.url);
                    console.log('Querystring key:', context.key);
                    if (forbidden) {  // to be defined...
                        return false;
                    }
                },
                onCompleted: function(context, fragment) {
                    console.log('Label:', $(this).text());
                    console.log('URL:', context.url);
                    console.log('Querystring key:', context.key);
                    console.log('Fragment:', fragment);
                }
            });
        </script>
    {% endblock %}

Manually selecting what to bind
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As seen above, *$.endlessPaginate()* enables Ajax support for each pagination
in the page. But assuming you are using :doc:`multiple_pagination`, e.g.:

.. code-block:: html+django

    <h2>Entries:</h2>
    <div id="entries" class="endless_page_template">
        {% include "myapp/entries_page.html" %}
    </div>

    <h2>Other entries:</h2>
    <div id="other-entries" class="endless_page_template">
        {% include "myapp/other_entries_page.html" %}
    </div>

    {% block js %}
        {{ block.super }}
        <script src="http://code.jquery.com/jquery-latest.js"></script>
        <script src="{{ STATIC_URL }}endless_pagination/js/endless-pagination.js"></script>
        <script>$.endlessPaginate();</script>
    {% endblock %}

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

At this point, you might have already guessed that *$.endlessPaginate()*
is just an alias for *$('body').endlessPaginate()*.

Customize each pagination
~~~~~~~~~~~~~~~~~~~~~~~~~

You can also call *$.endlessPaginate()* multiple times if you want to customize
the behavior of each pagination. E.g. if you need to register a callback for
*entries* but not for *other entries*:

.. code-block:: html+django

    <h2>Entries:</h2>
    <div id="entries" class="endless_page_template">
        {% include "myapp/entries_page.html" %}
    </div>

    <h2>Other entries:</h2>
    <div id="other-entries" class="endless_page_template">
        {% include "myapp/other_entries_page.html" %}
    </div>

    {% block js %}
        {{ block.super }}
        <script src="http://code.jquery.com/jquery-latest.js"></script>
        <script src="{{ STATIC_URL }}endless_pagination/js/endless-pagination.js"></script>
        <script>
            $('#entries').endlessPaginate({
                onCompleted: function(data) {
                    console.log('New entries loaded.');
                }
            });
            $('#other-entries').endlessPaginate();
        </script>
    {% endblock %}

.. _javascript-selectors:

Selectors
~~~~~~~~~

Each time *$.endlessPaginate()* is used, several JavaScript selectors are used
to select DOM nodes. Here is a list of them all:

- containerSelector: '.endless_container'
  (Twitter-style pagination container selector);
- loadingSelector: '.endless_loading' -
  (Twitter-style pagination loading selector);
- moreSelector: 'a.endless_more' -
  (Twitter-style pagination link selector);
- pageSelector: '.endless_page_template'
  (Digg-style pagination page template selector);
- pagesSelector: 'a.endless_page_link'
  (Digg-style pagination link selector).

An example can better explain the meaning of the selectors above. Assume you
have a Digg-style pagination like the following:

.. code-block:: html+django

    <h2>Entries:</h2>
    <div id="entries" class="endless_page_template">
        {% include "myapp/entries_page.html" %}
    </div>

    {% block js %}
        {{ block.super }}
        <script src="http://code.jquery.com/jquery-latest.js"></script>
        <script src="{{ STATIC_URL }}endless_pagination/js/endless-pagination.js"></script>
        <script>
            $('#entries').endlessPaginate();
        </script>
    {% endblock %}

Here the ``#entries`` node is selected and Digg-style pagination is applied.
Digg-style needs to know which DOM node will be updated with new contents,
and in this case it's the same node we selected, because we added the
*endless_page_template* class to that node, and *.endless_page_template*
is the selector used by default. However, the following example is equivalent
and does not involve adding another class to the container:

.. code-block:: html+django

    <h2>Entries:</h2>
    <div id="entries">
        {% include "myapp/entries_page.html" %}
    </div>

    {% block js %}
        {{ block.super }}
        <script src="http://code.jquery.com/jquery-latest.js"></script>
        <script src="{{ STATIC_URL }}endless_pagination/js/endless-pagination.js"></script>
        <script>
            $('#entries').endlessPaginate({
                pageSelector: '#entries'
            });
        </script>
    {% endblock %}

.. _javascript-chunks:

On scroll pagination using chunks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes, when using on scroll pagination, you may want to still display
the *show more* link after each *N* pages. In Django Endless Pagination this is
called *chunk size*. For instance, a chunk size of 5 means that a *show more*
link is displayed after page 5 is loaded, then after page 10, then after page
15 and so on. Activating this functionality is straightforward, just use the
*paginateOnScrollChunkSize* option:

.. code-block:: html+django

    {% block js %}
        {{ block.super }}
        <script src="http://code.jquery.com/jquery-latest.js"></script>
        <script src="{{ STATIC_URL }}endless_pagination/js/endless-pagination.js"></script>
        <script>
            $.endlessPaginate({
                paginateOnScroll: true,
                paginateOnScrollChunkSize: 5
            });
        </script>
    {% endblock %}

.. _javascript-migrate:

Migrate from version 1.1 to 2.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Django Endless Pagination v2.0 introduces changes in how Ajax pagination
is handled by JavaScript. These changes are discussed in this document and in
the :doc:`changelog`.

The JavaScript code now lives in a file named ``endless-pagination.js``.
For backward compatibility, the application still includes the two JavaScript
files ``endless.js`` and ``endless_on_scroll.js``. However, please consider
migrating as soon as possible: the old JavaScript files are deprecated, are
no longer maintained, and don't provide the new JavaScript features.

Instructions on how to migrate from the old version to the new one follow.

Basic migration
---------------

Before:

.. code-block:: html+django

    <h2>Entries:</h2>
    {% include page_template %}

    {% block js %}
        {{ block.super }}
        <script src="http://code.jquery.com/jquery-latest.js"></script>
        <script src="{{ STATIC_URL }}endless_pagination/js/endless.js"></script>
    {% endblock %}

Now:

.. code-block:: html+django

    <h2>Entries:</h2>
    {% include page_template %}

    {% block js %}
        {{ block.super }}
        <script src="http://code.jquery.com/jquery-latest.js"></script>
        <script src="{{ STATIC_URL }}endless_pagination/js/endless-pagination.js"></script>
        <script>$.endlessPaginate();</script>
    {% endblock %}

Pagination on scroll
--------------------

Before:

.. code-block:: html+django

    <h2>Entries:</h2>
    {% include page_template %}

    {% block js %}
        {{ block.super }}
        <script src="http://code.jquery.com/jquery-latest.js"></script>
        <script src="{{ STATIC_URL }}endless_pagination/js/endless.js"></script>
        <script src="{{ STATIC_URL }}endless_pagination/js/endless_on_scroll.js"></script>
    {% endblock %}

Now:

.. code-block:: html+django

    <h2>Entries:</h2>
    {% include page_template %}

    {% block js %}
        {{ block.super }}
        <script src="http://code.jquery.com/jquery-latest.js"></script>
        <script src="{{ STATIC_URL }}endless_pagination/js/endless-pagination.js"></script>
        <script>
            $.endlessPaginate({paginateOnScroll: true});
        </script>
    {% endblock %}

Pagination on scroll with customized bottom margin
--------------------------------------------------

Before:

.. code-block:: html+django

    <h2>Entries:</h2>
    {% include page_template %}

    {% block js %}
        {{ block.super }}
        <script src="http://code.jquery.com/jquery-latest.js"></script>
        <script src="{{ STATIC_URL }}endless_pagination/js/endless.js"></script>
        <script src="{{ STATIC_URL }}endless_pagination/js/endless_on_scroll.js"></script>
        <script>
            var endless_on_scroll_margin = 20;
        </script>
    {% endblock %}

Now:

.. code-block:: html+django

    <h2>Entries:</h2>
    {% include page_template %}

    {% block js %}
        {{ block.super }}
        <script src="http://code.jquery.com/jquery-latest.js"></script>
        <script src="{{ STATIC_URL }}endless_pagination/js/endless-pagination.js"></script>
        <script>
            $.endlessPaginate({
                paginateOnScroll: true,
                paginateOnScrollMargin: 20
            });
        </script>
    {% endblock %}


Avoid enabling Ajax on one or more paginations
----------------------------------------------

Before:

.. code-block:: html+django

    <h2>Other entries:</h2>
    <div class="endless_page_template endless_page_skip">
        {% include "myapp/other_entries_page.html" %}
    </div>

    {% block js %}
        {{ block.super }}
        <script src="http://code.jquery.com/jquery-latest.js"></script>
        <script src="{{ STATIC_URL }}endless_pagination/js/endless.js"></script>
    {% endblock %}

Now:

.. code-block:: html+django

    <h2>Other entries:</h2>
    <div class="endless_page_template endless_page_skip">
        {% include "myapp/other_entries_page.html" %}
    </div>

    {% block js %}
        {{ block.super }}
        <script src="http://code.jquery.com/jquery-latest.js"></script>
        <script src="{{ STATIC_URL }}endless_pagination/js/endless-pagination.js"></script>
        <script>$('not:(.endless_page_skip)').endlessPaginate();</script>
    {% endblock %}

In this last example, activating Ajax just where you want might be preferred
over excluding nodes.
