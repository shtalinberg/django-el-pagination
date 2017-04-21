Getting started
===============

Requirements
~~~~~~~~~~~~

======  ====================
Python  >= 2.7 (or Python 3)
Django  >= 1.8
jQuery  >= 1.7
======  ====================

Installation
~~~~~~~~~~~~

The Git repository can be cloned with this command::

    git clone https://github.com/shtalinberg/django-el-pagination.git

The ``el_pagination`` package, included in the distribution, should be
placed on the ``PYTHONPATH``.

Otherwise you can just ``easy_install -Z django-el-pagination``
or ``pip install django-el-pagination``.

Settings
~~~~~~~~

Add the request context processor to your *settings.py*, e.g.:

.. code-block:: python

    from django.conf.global_settings import TEMPLATES

    TEMPLATES[0]['OPTIONS']['context_processors'].insert(0, 'django.core.context_processors.request')

or  just adding it to the context_processors manually like so:

.. code-block:: python

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    '...',
                    '...',
                    '...',
                    '...',
                    'django.template.context_processors.request', ## For EL-pagination
                ],
            },
        },
    ]

Add ``'el_pagination'`` to the ``INSTALLED_APPS`` to your *settings.py*.

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

    {% load el_pagination_tags %}

    {% paginate entries %}
    {% for entry in entries %}
        {# your code to show the entry #}
    {% endfor %}
    {% show_pages %}

Done.

This is just a basic example. To continue exploring all the Django Endless
Pagination features, have a look at :doc:`twitter_pagination` or
:doc:`digg_pagination`.
