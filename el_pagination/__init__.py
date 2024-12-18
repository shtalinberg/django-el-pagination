"""Django pagination tools supporting Ajax, multiple and lazy pagination,
Twitter-style and Digg-style pagination.
"""

VERSION = (4, 1, 2)
__version__ = '.'.join(map(str, VERSION))

def get_version():
    """Return the Django EL Pagination version as a string."""
    return __version__
