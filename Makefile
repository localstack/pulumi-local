VENV_BIN ?= python3 -m venv
# Default virtual env dir
VENV_DIR ?= .venv
VENV_REQS_FILE ?= ./requirements.txt
PIP_CMD ?= pip3

ifeq ($(OS), Windows_NT)
	VENV_ACTIVATE = ./$(VENV_DIR)/Scripts/activate
else
	VENV_ACTIVATE = ./$(VENV_DIR)/bin/activate
endif

VENV_RUN = . $(VENV_ACTIVATE)
$(VENV_ACTIVATE):
	test -d $(VENV_DIR) || $(VENV_BIN) $(VENV_DIR)
	$(VENV_RUN); $(PIP_CMD) install --upgrade pip setuptools
	$(VENV_RUN); $(PIP_CMD) install $(PIP_OPTS) -r $(VENV_REQS_FILE)
	touch $(VENV_ACTIVATE)

venv: $(VENV_ACTIVATE)    ## Create a virtual environment

usage:             ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install: venv          ## Install dependencies in local virtualenv folder
	($(VENV_RUN) && $(PIP_CMD) install -e .)

publish: venv          ## Publish the library to the central PyPi repository
	# build and upload archive
	($(VENV_RUN) && ./setup.py sdist && twine upload dist/*)

lint:              ## Run code linter
	flake8 bin/pulumilocal

clean:             ## Clean up
	rm -rf $(VENV_DIR)

.PHONY: clean publish install usage
