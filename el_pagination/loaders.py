"""Django EL Pagination object loaders."""

from importlib import import_module

from django.core.exceptions import ImproperlyConfigured


def load_object(path):
    """Return the Python object represented by dotted *path*."""
    i = path.rfind('.')
    module_name, object_name = path[:i], path[i + 1 :]
    # Load module.
    try:
        module = import_module(module_name)
    except ImportError:
        raise ImproperlyConfigured('Module %r not found' % module_name)
    except ValueError:
        raise ImproperlyConfigured('Invalid module %r' % module_name)
    # Load object.
    try:
        return getattr(module, object_name)
    except AttributeError:
        msg = 'Module %r does not define an object named %r'
        raise ImproperlyConfigured(msg % (module_name, object_name))
