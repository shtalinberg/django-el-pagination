"""Django pagination tools supporting Ajax, multiple and lazy pagination,
Twitter-style and Digg-style pagination.
"""

from __future__ import unicode_literals


VERSION = (2, 1, 1)


def get_version():
    """Return the Django EL Pagination version as a string."""
    return '.'.join(map(str, VERSION))
