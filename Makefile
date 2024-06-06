SHELL:=/bin/zsh
.SHELLFLAGS := -eu -o pipefail -c
.ONESHELL:

PY_VERSION = 3.11.0

VENV = .venv
PY = $$(if [ -f $(VENV)/bin/python ]; then echo $(VENV)/bin/python; else echo python; fi)
PIP = $(PY) -m pip
PWD = $(shell pwd)

# Colors for echos 
ccend=$(shell tput sgr0)
ccbold=$(shell tput bold)
ccgreen=$(shell tput setaf 2)
ccso=$(shell tput smso)

.DEFAULT_GOAL := help

.PHONY: help
help: ## Display this help section
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: create_venv
create_venv: ## Create a virtual environment or update it if it exists
	@echo "$(ccbold)--> Creating virtual environment...$(ccend)"
	$(PY) -m venv ${VENV}
	$(PIP) install -U pip setuptools wheel build
	@echo "$(ccbold)-->Virtual environment created$(ccend)"

.PHONY: activate_venv 
activate_venv: install_requirements ## Activate the virtual environment
	@echo "$(ccbold)--> Activating virtual environment...$(ccend)"
	. "$(VENV)/bin/activate" && exec $(notdir $(SHELL)) 
	@echo "$(ccbold)-->Virtual environment activated$(ccend)"

.PHONY: install_requirements
install_requirements: ## Install python requirements if requirements.txt exists
	@if [ -f $(PWD)/requirements.txt ]; then \
		$(PIP) install -U -r $(PWD)/requirements.txt; \
	else \
		echo "$(ccbold)--> No requirements.txt file found$(ccend)"; \
	fi

.PHONY: deactivate_venv
deactivate_venv: ## Deactivate the virtual environment
	@echo "$(ccbold)--> Deactivating environment...$(ccend)"
	. deactivate
	@echo "$(ccbold)--> Virtual environment removed$(ccend)"


.PHONY: clean_venv
clean_venv: ## Remove the virtual environment
	@echo "$(ccbold)--> Removing virtual environment...$(ccend)"
	rm -rf $(VENV)
	@echo "$(ccbold)--> Virtual environment removed$(ccend)"

.PHONY: reset_venv
reset_venv: deactivate_venv clean_venv create_venv activate_venv ## Completely reset the virtual environment
	@echo "$(ccbold)--> Virtual environment reset$(ccend)"
