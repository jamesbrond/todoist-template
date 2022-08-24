# requires misc.mk

VENV_DIR      := venv

ACTIVATE      := $(VENV_DIR)/Scripts/activate
PY_SRCS       := $(shell /usr/bin/find . -path ./$(VENV_DIR) -prune -o -name "*.py" -print)
REQUIREMENTS  := requirements.txt

do_activate   = [[ -z "$$VIRTUAL_ENV" ]] && . $(ACTIVATE) || true
install_deps  = $(do_activate) && pip install -Ur $(1)
pyenv         = $(do_activate) && $(1)


.PHONY: clean-pycache clean-venv deps devdeps lint

$(ACTIVATE): ## Create python virtual environment
# The venv module provides support for creating lightweight "virtual environments" with
# their own site directories, optionally isolated from system site directories.
# https://docs.python.org/3/library/venv.html
	@$(call prompt-info,Creating virtual environment)
	@python -m venv $(VENV_DIR)
# convert CRLF to LF in activate bash script
	@sed -i $$'s/\\r$$//' $(ACTIVATE)

clean-pycache: ## Remove bytecode-compiled python files
	@$(call prompt-log,Removing bytecode-compiled python files)
	@/usr/bin/find . -name __pycache__ -type d  -print0 | xargs -0 -r rm -rf

clean-venv: ## Remove virtual evnironemnt
	@$(call prompt-log,Removing virtual environment)
	@rm -rf $(VENV_DIR)

deps: $(ACTIVATE) $(REQUIREMENTS) ## Activate venv and install requirements
	@$(call prompt-info,Upgrading pip)
	@$(call pyenv,python -m pip install --upgrade pip)
	@$(call prompt-info,Installing dependencies)
	@$(call install_deps, $(REQUIREMENTS))

devdeps: deps ## Install both application and developer requirements (pylint, flake8)
	@$(call prompt-info,Installing developement requirements)
	@$(call pyenv,pip install -U pylint flake8)

lint:  ## Lint and static-check
	@$(call prompt-info,Running flake8)
	@$(call pyenv,python -m flake8 --config .github/linters/.flake8 $(PY_SRCS)) && $(call prompt-success,Done) || $(call prompt-error,Failed)
	@$(call prompt-info,Running pylint)
	@$(call pyenv,python -m pylint $(PY_SRCS)) && $(call prompt-success,Done) || $(call prompt-error,Failed)

# ~@:-]
