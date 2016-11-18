.PHONY: clean clean-test clean-pyc clean-build help examples
.DEFAULT_GOAL := help
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

coverage: ## check code coverage and display results in web browser
	coverage run --source ptolemy setup.py test
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

coverage-ci: ## check code coverage and display results as xml for CI
	coverage run --source ptolemy setup.py test
	coverage report -m --fail-under=100
	coverage xml

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -fr {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -f coverage.xml
	rm -fr .cache/

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

examples:  ## compile example source files
	cd examples && ./build.sh && cd ..

install: clean ## install the package to the active Python's site-packages
	python setup.py install

integration-test: install  ## run integration tests
	behave integration_tests

lint: ## check style with flake8
	flake8 ptolemy tests integration_tests

pylint: ## check style with pylint
	pylint ptolemy

release: clean ## package and upload a release
	python setup.py sdist upload
	python setup.py bdist_wheel upload

test: lint unit-test-all integration-test coverage-ci  ## run all tests (ci-safe)

unit-test: ## run tests quickly with the default Python
	py.test -v tests

unit-test-all: ## run tests on every Python version with tox
	tox
