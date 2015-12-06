Contributing
============

Here are the steps needed to set up a development and testing environment.

Creating a development environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The development environment is created in a virtualenv. The environment
creation requires the *make* and *virtualenv* programs to be installed.

To install *make* under Debian/Ubuntu::

    $ sudo apt-get install build-essential

Under Mac OS/X, *make* is available as part of XCode.

To install virtualenv::

    $ sudo pip install virtualenv

At this point, from the root of this branch, run the command::

    $ make

This command will create a ``.venv`` directory in the branch root, ignored
by DVCSes, containing the development virtual environment with all the
dependencies.

Testing the application
~~~~~~~~~~~~~~~~~~~~~~~

Run the tests::

    $ make test

The command above also runs all the available integration tests. They use
Selenium and require Firefox to be installed. To avoid executing integration
tests, define the environment variable SKIP_SELENIUM, e.g.::

    $ make test SKIP_SELENIUM=1

Integration tests are excluded by default when using Python 3. The test suite
requires Python >= 2.6.1.

Run the tests and lint/pep8 checks::

    $ make check

Again, to exclude integration tests::

    $ make check SKIP_SELENIUM=1

Debugging
~~~~~~~~~

Run the Django shell (Python interpreter)::

    $ make shell

Run the Django development server for manual testing::

    $ make server

After executing the command above, it is possible to navigate the testing
project going to <http://localhost:8000>.

See all the available make targets, including info on how to create a Python 3
development environment::

    $ make help

Thanks for contributing, and have fun!
