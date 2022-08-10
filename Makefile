PACKAGE       := todoist-template

LIB_DIR       := lib
SRCS_DIR      := .
VENV_DIR      := venv

ACTIVATE      := $(VENV_DIR)/Scripts/activate
REQUIREMENTS  := requirements.txt


.PHONY: clean deps help
.DEFAULT_GOAL := help


do_activate   = @[[ $$(python makeutils/makeutils.py) == *0* ]] && . $(ACTIVATE) || true
pyenv         = $(do_activate) && $(1)


$(ACTIVATE): ## Create python virtual environment
# The venv module provides support for creating lightweight "virtual environments" with
# their own site directories, optionally isolated from system site directories.
# https://docs.python.org/3/library/venv.html
	@python -m venv $(VENV_DIR)
# convert CRLF to LF in activate bash script
	@sed -i $$'s/\\r$$//' $(ACTIVATE)
	@echo Created virtual environmenset

clean: ## Clean-up the solution
	@echo Remove virtual environments
	@rm -rf $(VENV_DIR)
	@echo Remove bytecode-compiled python files
	@/usr/bin/find $(LIB_DIR) -name __pycache__ -type d  -print0 | xargs -0 -r rm -rf

deps: $(ACTIVATE) $(REQUIREMENTS) ## Activate venv and install requirements
	$(call pyenv,pip install -Ur $(REQUIREMENTS))
	@echo Installation complete

help: ## Show Makefile help
# http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@grep -E '^[a-zA-Z_\.-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
