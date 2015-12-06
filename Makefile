# Django Endless Pagination Makefile.

# Define these variables based on the system Python versions.
PYTHON2 = python
PYTHON3 = python3

VENV2 = .venv
VENV3 = .venv3

LINTER = flake8 --show-source endless_pagination/ tests/
MANAGE = python ./tests/manage.py

ifdef PY3
	PYTHON = $(PYTHON3)
	VENV = $(VENV3)
else
	PYTHON = $(PYTHON2)
	VENV = $(VENV2)
endif

DOC_INDEX = doc/_build/html/index.html
VENV_ACTIVATE = $(VENV)/bin/activate
WITH_VENV = ./tests/with_venv.sh $(VENV)

all: develop

$(DOC_INDEX): $(wildcard doc/*.rst)
	@$(WITH_VENV) make -C doc html

doc: develop $(DOC_INDEX)

clean:
	$(PYTHON) setup.py clean
	rm -rfv .coverage build/ dist/ doc/_build MANIFEST
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d -delete

cleanall: clean
	rm -rfv $(VENV2) $(VENV3)

check: test lint

$(VENV_ACTIVATE): tests/develop.py tests/requirements.pip
	@$(PYTHON) tests/develop.py
	@touch $(VENV_ACTIVATE)

develop: $(VENV_ACTIVATE)

help:
	@echo -e 'Django Endless Pagination - list of make targets:\n'
	@echo 'make - Set up development and testing environment'
	@echo 'make test - Run tests'
	@echo 'make lint - Run linter and pep8'
	@echo 'make check - Run tests, linter and pep8'
	@echo 'make doc - Build Sphinx documentation'
	@echo 'make opendoc - Build Sphinx documentation and open it in browser'
	@echo 'make source - Create source package'
	@echo 'make install - Install on local system'
	@echo 'make shell - Enter Django interactive interpreter'
	@echo 'make server - Run Django development server'
	@echo 'make clean - Get rid of bytecode files, build dirs, dist files'
	@echo 'make cleanall - Clean and also get rid of the virtualenvs'
	@echo -e '\nDefine the env var PY3 to work using Python 3.'
	@echo 'E.g. to create a Python 3 development environment:'
	@echo '  - make PY3=1'
	@echo 'E.g. to run tests and linter under Python 3:'
	@echo '  - make check PY3=1'
	@echo -e '\nWhen testing the application, define the env var'
	@echo 'SKIP_SELENIUM to exclude integration tests, e.g.:'
	@echo '  - make check SKIP_SELENIUM=1'
	@echo -e '\nWhen running integration tests, by default all graphical'
	@echo 'operations are performed in memory where possible. However,'
	@echo 'it is possible to run tests using a visible browser instance'
	@echo 'by defining the env var SHOW_BROWSER, e.g.:'
	@echo '  - make check SHOW_BROWSER=1'

install:
	python setup.py install

lint: develop
	@$(WITH_VENV) $(LINTER)

opendoc: doc
	@firefox $(DOC_INDEX)

release: clean
	python setup.py register sdist upload

server: develop
	@$(WITH_VENV) $(MANAGE) runserver 0.0.0.0:8000

shell: develop
	@$(WITH_VENV) $(MANAGE) shell

source:
	$(PYTHON) setup.py sdist

test: develop
	@$(WITH_VENV) $(MANAGE) test

.PHONY: all doc clean cleanall check develop install lint opendoc release \
	server shell source test
