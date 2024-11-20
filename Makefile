# Django Endless Pagination Makefile.

# Define these variables based on the system Python versions.
PYTHON ?= python3

VENV = .venv
WITH_VENV = ./tests/with_venv.sh $(VENV)
MANAGE = $(PYTHON) ./tests/manage.py
LINTER = flake8 --show-source el_pagination/ tests/
DOC_INDEX = doc/_build/html/index.html

.PHONY: all clean cleanall check develop help install lint doc opendoc release server shell source test

all: develop

# Virtual environment
$(VENV)/bin/activate: tests/develop.py tests/requirements.pip
	@$(PYTHON) tests/develop.py
	@touch $(VENV)/bin/activate
	$(VENV)/bin/pip install --upgrade pip setuptools wheel
	$(VENV)/bin/pip install -r tests/requirements.pip

develop: $(VENV)/bin/activate
	$(VENV)/bin/pip install -e .

# Documentation
$(DOC_INDEX): $(wildcard doc/*.rst)
	@$(WITH_VENV) make -C doc html

doc: develop $(DOC_INDEX)

clean:
	pip uninstall django-el-pagination -y || true
	rm -rfv .coverage build/ dist/ doc/_build MANIFEST *.egg-info
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d -delete

cleanall: clean
	rm -rf $(VENV)

check: test lint

install:
	pip install --force-reinstall -e .

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

help:
	@echo 'Django Endless Pagination - Available commands:'
	@echo
	@echo 'Development:'
	@echo '  make          - Set up development environment'
	@echo '  make install  - Install package locally'
	@echo '  make server   - Run development server'
	@echo '  make shell    - Enter Django shell'
	@echo
	@echo 'Testing:'
	@echo '  make test     - Run tests'
	@echo '  make lint     - Run code linting'
	@echo '  make check    - Run tests and linting'
	@echo
	@echo 'Documentation:'
	@echo '  make doc      - Build documentation'
	@echo '  make opendoc  - Build and open documentation'
	@echo
	@echo 'Cleaning:'
	@echo '  make clean    - Remove build artifacts'
	@echo '  make cleanall - Remove all generated files including venv'
	@echo
	@echo 'Distribution:'
	@echo '  make source   - Create source package'
	@echo '  make release  - Upload to PyPI'
	@echo
	@echo 'Environment Variables:'
	@echo '  USE_SELENIUM=1    - Include integration tests'
	@echo '  SHOW_BROWSER=1    - Show browser during Selenium tests'
	@echo
