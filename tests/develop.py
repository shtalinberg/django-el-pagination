"""Create a development and testing environment using a virtualenv."""
import os
import subprocess
import sys

TESTS = os.path.abspath(os.path.dirname(__file__))
REQUIREMENTS = os.path.join(TESTS, 'requirements.pip')
WITH_VENV = os.path.join(TESTS, 'with_venv.sh')
VENV = os.path.abspath(os.path.join(TESTS, '..', '.venv'))


def call(*args):
    """Simple ``subprocess.call`` wrapper."""
    if subprocess.call(args):  # noqa: S603
        raise SystemExit('Error running {0}.'.format(args))


def pip_install(*args):
    """Install packages using pip inside the venv."""
    call(WITH_VENV, '.venv', 'pip', 'install', *args)


if __name__ == '__main__':
    call(sys.executable, '-m', 'venv', VENV)
    pip_install('-r', REQUIREMENTS)
