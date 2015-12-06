Getting started
===============

Requirements
~~~~~~~~~~~~

======  ====================
Python  >= 2.6 (or Python 3)
Django  >= 1.3
jQuery  >= 1.7
======  ====================

Installation
~~~~~~~~~~~~

The Git repository can be cloned with this command::

    git clone https://github.com/frankban/django-endless-pagination.git

If you like Mercurial, you can clone the application with this command::

    hg clone https://bitbucket.org/frankban/django-endless-pagination

The ``endless_pagination`` package, included in the distribution, should be
placed on the ``PYTHONPATH``.

Otherwise you can just ``easy_install -Z django-endless-pagination``
or ``pip install django-endless-pagination``.

Settings
~~~~~~~~

Add the request context processor to your *settings.py*, e.g.::

    from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
    TEMPLATE_CONTEXT_PROCESSORS += (
        'django.core.context_processors.request',
    )

Add ``'endless_pagination'`` to the ``INSTALLED_APPS`` to your *settings.py*.

See the :doc:`customization` section for other settings.

Quickstart
~~~~~~~~~~

Given a template like this:

.. code-block:: html+django

    {% for entry in entries %}
        {# your code to show the entry #}
    {% endfor %}

you can use Digg-style pagination to display objects just by adding:

.. code-block:: html+django

    {% load endless %}

    {% paginate entries %}
    {% for entry in entries %}
        {# your code to show the entry #}
    {% endfor %}
    {% show_pages %}

Done.

This is just a basic example. To continue exploring all the Django Endless
Pagination features, have a look at :doc:`twitter_pagination` or
:doc:`digg_pagination`.
