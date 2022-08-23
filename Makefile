include .make/colors.mk

PACKAGE       := todoist-template

LIB_DIR       := lib
SRCS_DIR      := .
VENV_DIR      := venv

ACTIVATE      := $(VENV_DIR)/Scripts/activate
REQUIREMENTS  := requirements.txt
MAKE_PY_SCRIPT:= makeutils.py


.PHONY: clean help install
.DEFAULT_GOAL := help


do_activate   = @[[ $$(python $(MAKE_PY_SCRIPT) --venv) == *0* ]] && . $(ACTIVATE) || true
pyenv         = $(do_activate) && $(1)
version       = $$(python $(MAKE_PY_SCRIPT) --version)

$(ACTIVATE): ## Create python virtual environment
# The venv module provides support for creating lightweight "virtual environments" with
# their own site directories, optionally isolated from system site directories.
# https://docs.python.org/3/library/venv.html
	$(call echoclr,$(BWHITE),Creating virtual environment...)
	@python -m venv $(VENV_DIR)
# convert CRLF to LF in activate bash script
	@sed -i $$'s/\\r$$//' $(ACTIVATE)
	$(call echoclr,$(GREEN),Done)

clean: ## Clean-up the solution
	$(call echoclr,$(BWHITE),Cleaning up the solution...)
	$(call echoclr,$(BLACK),Removing virtual environment...)
	@rm -rf $(VENV_DIR)
	$(call echoclr,$(BLACK),Removing bytecode-compiled python files...)
	@/usr/bin/find $(LIB_DIR) -name __pycache__ -type d  -print0 | xargs -0 -r rm -rf
	$(call echoclr,$(GREEN),Done)

help: ## Show Makefile help
# http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@grep -E '^[a-zA-Z_\.-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":[^:]*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install: $(ACTIVATE) $(REQUIREMENTS) ## Activate venv and install requirements
	$(call echoclr,$(BWHITE),Upgrading pip)
	$(call pyenv,python -m pip install --upgrade pip)
	$(call echoclr,$(GREEN),Done)
	$(call echoclr,$(BWHITE),Installing requirements)
	$(call pyenv,pip install -Ur $(REQUIREMENTS))
	$(call echoclr,$(GREEN),Done)

# ~@:-]
