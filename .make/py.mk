VENV_DIR      := venv

ACTIVATE      := $(VENV_DIR)/Scripts/activate
REQ           := requirements.txt

do_activate   = [[ -z "$$VIRTUAL_ENV" ]] && . $(ACTIVATE) || true
pyenv         = $(do_activate) && $(1)

install_deps  = $(do_activate) && pip install -Ur $(1)

$(ACTIVATE): ## Create python virtual environment
# The venv module provides support for creating lightweight "virtual environments" with
# their own site directories, optionally isolated from system site directories.
# https://docs.python.org/3/library/venv.html
	@$(call echoclr,$(BWHITE),Creating virtual environment...)
	@python -m venv $(VENV_DIR)
# convert CRLF to LF in activate bash script
	@sed -i $$'s/\\r$$//' $(ACTIVATE)
	@$(call echoclr,$(GREEN),Done)

clean-pycache: ## Remove bytecode-compiled python files
	@$(call echoclr,$(BLACK),Removing bytecode-compiled python files...)
	@/usr/bin/find $(LIB_DIR) -name __pycache__ -type d  -print0 | xargs -0 -r rm -rf
	@$(call echoclr,$(GREEN),Done)

clean-venv: ## Remove virtual evnironemnt
	@$(call echoclr,$(BLACK),Removing virtual environment...)
	@rm -rf $(VENV_DIR)

deps: $(ACTIVATE) $(REQ) ## Activate venv and install requirements
	@$(call echoclr,$(BWHITE),Upgrading pip)
	@$(call pyenv,python -m pip install --upgrade pip)
	@$(call echoclr,$(GREEN),Done)
	@$(call echoclr,$(BWHITE),Installing requirements)
	@$(call install_deps, $(REQ))
	@$(call echoclr,$(GREEN),Done)

lint:  ## Lint and static-check
	@$(call echoclr,$(BWHITE),Running flake8)
	@$(call pyenv,python -m flake8 $(PACKAGE).py $(LIB_DIR)) && $(call echoclr,$(GREEN),Done) || $(call echoclr,$(RED),Failed)
	@$(call echoclr,$(BWHITE),Running pylint)
	@$(call pyenv,python -m pylint --recursive=y $(PACKAGE) $(LIB_DIR) && echo -e "$(GREEN)Done$(COLOR_OFF)" || echo -e "$(RED)Failed$(COLOR_OFF)")

# ~@:-]
