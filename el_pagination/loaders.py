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
    except ImportError as exc:
        raise ImproperlyConfigured(f'Module {module_name} not found') from exc
    except ValueError as exc:
        raise ImproperlyConfigured(f'Invalid module {module_name}') from exc
    # Load object.
    try:
        return getattr(module, object_name)
    except AttributeError as exc:
        msg = 'Module %r does not define an object named %r'
        raise ImproperlyConfigured(msg % (module_name, object_name)) from exc
