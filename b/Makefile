SHELL := /bin/bash
SHELLFLAGS := -eu -o pipefail -c

.ONESHELL:
.PHONY: pip dev end-dev run tree clean test

PY = python
PROJECT = $(shell grep -m 1 '^name =' pyproject.toml | cut -d '"' -f 2)
DEPTH = 3

WH_BG = 47
BU = 94
YW = 93
GR = 92
TX_IN = $(shell printf '\033[1;$(YW);$(WH_BG)m')
TX_OUT = $(shell printf '\033[1;$(GR);$(WH_BG)m')
R = $(shell printf '\033[0m')


# --- TARGETS ---

pip: 
	@echo "$(TX_IN)- INSTALLING DEPENDENCIES -$(R)"
	@pip install .
	@echo "$(TX_OUT)- DEPENDENCIES INSTALLED-$(R)"

dev:
	@echo "$(TX_IN)- INSTALLING IN EDITABLE MODE -$(R)"
	@pip install -e ".[dev]" 
	@echo "$(TX_OUT)- DEV MODE ACTIVE (editable install) -$(R)"

run:
	@echo "$(TX_IN)- STARTING DEV SERVER -$(R)"
	@$(PY) -m App --log WARNING --tail 
	@echo "$(TX_OUT)- SERVER STOPPED -$(R)"


tree:
	@echo "$(TX_IN)- PROJECT STRUCTURE -$(R)"
	@tree -C -L $(DEPTH) -I '__pycache__|*.py[co]|*.sw?|.DS_Store|.git|node_modules|hidden|build|dist|*.egg-info|*.yaml'
	@echo "$(TX_OUT)- FINISHED -$(R)"



end-dev:
	@echo "$(TX_IN)- UNINSTALLING EDITABLE PACKAGE -$(R)"
	@pip uninstall -y $(PROJECT) || true
	@echo "$(TX_OUT)- DEV MODE DISABLED -$(R)"

clean: end-dev
	@echo "$(TX_IN)- CLEANING BUILD ARTIFACTS -$(R)"
	@rm -rf build/ dist/ *.egg-info/ .pytest_cache/ __pycache__/ .nox/ .mypy_cache
	@echo "$(TX_OUT)- CLEANED -$(R)"


# --- NOX ---

test-routes: dev
	@echo "$(TX_IN)- RUNNING INTEGRATION TESTS -$(R)"
	@nox -s integration
	@echo "$(TX_OUT)- INTEGRATION TESTS COMPLETE -$(R)"

test-memcell: dev
	@echo "$(TX_IN)- NOX INIT -$(R)"
	nox -s test_memcell
	@echo "$(TX_OUT)- COMPLETED -$(R)"

test-yamel: dev
	@echo "$(TX_IN)- NOX INIT -$(R)"
	nox -s test_yamel
	@echo "$(TX_OUT)- COMPLETED -$(R)"


# --- JENKINS ---

jenkins-start:
	@echo "$(TX_IN)- STARTING JENKINS -$(R)"
	sudo service jenkins start
	@echo "$(TX_OUT)- JENKINS STARTED -$(R)"

jenkins-stop:
	@echo "$(TX_IN)- STOPPING JENKINS -$(R)"
	sudo service jenkins stop
	@echo "$(TX_OUT)- JENKINS STOPPED -$(R)"

jenkins-restart:
	@echo "$(TX_IN)- RESTARTING JENKINS -$(R)"
	sudo service jenkins restart
	@echo "$(TX_OUT)- JENKINS RESTARTED -$(R)"

jenkins-status:
	@echo "$(TX_IN)- JENKINS STATUS -$(R)"
	sudo service jenkins status
	@echo "$(TX_OUT)- STATUS CHECK COMPLETE -$(R)"