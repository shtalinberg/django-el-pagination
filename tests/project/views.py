"""Test project views."""

from __future__ import unicode_literals

from django.shortcuts import render


LOREM = """Lorem ipsum dolor sit amet, consectetur adipisicing elit,
    sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
    nisi ut aliquip ex ea commodo consequat.
"""


def _make(title, number):
    """Make a *number* of items."""
    return [
        {'title': '{0} {1}'.format(title, i + 1), 'contents': LOREM}
        for i in range(number)
    ]


def generic(request, extra_context=None, template=None, number=50):
    context = {
        'objects': _make('Object', number),
        'items': _make('Item', number),
        'entries': _make('Entry', number),
        'articles': _make('Article', number),
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)
