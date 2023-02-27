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
-include .make/git.mk
-include .make/py.mk
-include .make/angular.mk

.make:
	@echo "make directory .make"
	@mkdir -p $@

.make/%.mk: | .make
	@URL=$$(echo "https://raw.githubusercontent.com/jamesbrond/jamesbrond/main/Makefile/$$(basename $@)"); \
	echo "get $$URL"; \
	curl -s -H 'Cache-Control: no-cache, no-store' $${URL} -o $@


.PHONY: build clean distclean dist lint
.DEFAULT_GOAL := help


build:: ## Compile the entire program
	@$(call log-info,MAKE,$@ done)

clean:: ## Delete all files created by this makefile, however don’t delete the files that record configuration or environment
	@$(call log-info,MAKE,$@ done)

distclean:: clean ## Delete all files in the current directory (or created by this makefile) that are created by configuring or building the program
	@-rm -rf $(BUILD_DIR)
	@-rm -rf $(DIST_DIR)
	@-rm -rf .make
	@$(call log-info,MAKE,$@ done)

dist:: build ## Create a distribution file or files for this program
	@$(call log-info,MAKE,$@ done)

lint:: ## Perform static linting
	@$(call log-info,MAKE,$@ done)

run: build
	@$(call log-info,MAKE,Run UI interface)
	@$(call pyenv,python todoist_template.py)

# ~@:-]
