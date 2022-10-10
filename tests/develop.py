"""Create a development and testing environment using a virtualenv."""
import os
import subprocess
import sys

VENV_NAME = '.venv3'

TESTS = os.path.abspath(os.path.dirname(__file__))
REQUIREMENTS = os.path.join(TESTS, 'requirements.pip')
WITH_VENV = os.path.join(TESTS, 'with_venv.sh')
VENV = os.path.abspath(os.path.join(TESTS, '..', VENV_NAME))


def call(*args):
    """Simple ``subprocess.call`` wrapper."""
    if subprocess.call(args):
        raise SystemExit('Error running {0}.'.format(args))


def pip_install(*args):
    """Install packages using pip inside the virtualenv."""
    call(WITH_VENV, VENV_NAME, 'pip', 'install', *args)


if __name__ == '__main__':
    call('virtualenv', '-p', sys.executable, VENV)
    pip_install('-r', REQUIREMENTS)
