VENV_BIN ?= virtualenv
# Default virtual env dir
VENV_DIR ?= .venv
PIP_CMD ?= pip3
TEST_PATH ?= tests

ifeq ($(OS), Windows_NT)
	VENV_ACTIVATE = ./$(VENV_DIR)/Scripts/activate
else
	VENV_ACTIVATE = ./$(VENV_DIR)/bin/activate
endif

VENV_RUN = . $(VENV_ACTIVATE)

venv:   		## Create a virtual environment
	(test `which virtualenv`|| $(PIP_CMD) install --user virtualenv) && \
		(test -d $(VENV_DIR) || $(VENV_BIN) $(VENV_OPTS) $(VENV_DIR))

usage:           	## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install: venv      	## Install dependencies in local virtualenv folder
	$(VENV_RUN); $(PIP_CMD) install -e .[test]

publish: venv       	## Publish the library to the central PyPi repository
	# build and upload archive
	$(VENV_RUN); $(PIP_CMD) install --upgrade setuptools wheel twine
	(./setup.py sdist && twine upload --repository pulumi-local dist/*)

lint: venv        	## Run code linter
	$(VENV_RUN); flake8 --ignore=E501,W503 bin/pulumilocal tests

test: venv       	## Run unit/integration tests
	$(VENV_RUN); pytest $(PYTEST_ARGS) -sv $(TEST_PATH)

clean:             	## Clean up
	rm -rf $(VENV_DIR)
	rm -rf dist
	rm -rf *.egg-info

.PHONY: clean publish install usage lint test venv