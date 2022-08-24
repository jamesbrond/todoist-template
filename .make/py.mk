# requires misc.mk

VENV_DIR      := venv

ACTIVATE      := $(VENV_DIR)/Scripts/activate
REQ           := requirements.txt

do_activate   = [[ -z "$$VIRTUAL_ENV" ]] && . $(ACTIVATE) || true
pyenv         = $(do_activate) && $(1)

install_deps  = $(do_activate) && pip install -Ur $(1)

.PHONY: clean-pycache clean-venv deps lint

$(ACTIVATE): ## Create python virtual environment
# The venv module provides support for creating lightweight "virtual environments" with
# their own site directories, optionally isolated from system site directories.
# https://docs.python.org/3/library/venv.html
	@$(call prompt-log,Creating virtual environment)
	@python -m venv $(VENV_DIR)
# convert CRLF to LF in activate bash script
	@sed -i $$'s/\\r$$//' $(ACTIVATE)

clean-pycache: ## Remove bytecode-compiled python files
	@$(call prompt-log,Removing bytecode-compiled python files)
	@/usr/bin/find $(LIB_DIR) -name __pycache__ -type d  -print0 | xargs -0 -r rm -rf

clean-venv: ## Remove virtual evnironemnt
	@$(call prompt-log,Removing virtual environment)
	@rm -rf $(VENV_DIR)

deps: $(ACTIVATE) $(REQ) ## Activate venv and install requirements
	@$(call prompt-info,Upgrading pip)
	@$(call pyenv,python -m pip install --upgrade pip)
	@$(call prompt-info,Installing dependencies)
	@$(call install_deps, $(REQ))

lint:  ## Lint and static-check
	@$(call prompt-info,Running flake8)
	@$(call pyenv,python -m flake8 $(PACKAGE).py $(LIB_DIR)) && $(call prompt-success,Done) || $(call prompt-error,Failed)
	@$(call prompt-info,Running pylint)
	@$(call pyenv,python -m pylint --recursive=y $(PACKAGE) $(LIB_DIR)) && $(call prompt-success,Done) || $(call prompt-error,Failed)

# ~@:-]
