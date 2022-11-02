BUILD_DIR    := build
DIST_DIR     := dist
LOCALES_DIR  := locales
PACKAGE      := todoist_template
PYTHON       := /usr/bin/python3.10
VERSION_FILE := lib/__version__.py
VERSION_EXP  := (__version__ = \")[0-9\.]+
NG_DIR       := ui

SHELL:=/bin/bash

-include .make/misc.mk
-include .make/py.mk
-include .make/git.mk
-include .make/angular.mk

MAKE_INCLUDES = $(shell grep -E '^-include .*\s$$' Makefile | awk 'BEGIN {FS = " "}; {print $$2}')
$(MAKE_INCLUDES):
	@mkdir -p $$(dirname $@); \
	NAME=$$(basename $@); \
	URL=$$(echo "https://raw.githubusercontent.com/jamesbrond/jamesbrond/main/Makefile/$$NAME"); \
	echo "get $$URL"; \
	curl -s -H 'Cache-Control: no-cache, no-store' $${URL} -o $@

.PHONY: clean clean-dist compile deps devdeps dist lint run
.DEFAULT_GOAL := help

$(BUILD_DIR):
	mkdir -p $@

clean-dist: clean clean-venv ## Clean-up the entire solution
	@-rm -rf .make
	@-rm -rf dist

clean: clean-pycache clean-pygettext ## Clean-up generated files

deps: py-deps ## Install dependencies

devdeps: py-devdeps ## Install dependencies for depveloper
	@$(call pyenv,pip install -U PyInstaller)

lint: py-lint ng-lint ## Lint and static-check

compile: $(BUILD_DIR) ng-compile

rund: compile
	@$(call prompt-info,Run UI interface detached)
	@./todoist_template.py &

run: compile
	@$(call prompt-info,Run UI interface)
	@$(call pyenv,./todoist_template.py)

dist: compile
	@$(call pyenv,python -m eel $(PACKAGE).py $(NG_BUILD_DIR) --exclude win32com --exclude numpy --exclude cryptography)
#--onefile --noconsole

# ~@:-]
