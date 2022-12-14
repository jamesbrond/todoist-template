DIST_DIR     := dist
LOCALES_DIR  := locales
PACKAGE      := todoist_template
VERSION_FILE := lib/__version__.py
VERSION_EXP  := (__version__ = \")[0-9\.]+

-include .make/misc.mk
-include .make/py.mk
-include .make/git.mk

MAKE_INCLUDES = $(shell grep -E '^-include .*\s$$' Makefile | awk 'BEGIN {FS = " "}; {print $$2}')
$(MAKE_INCLUDES):
	@mkdir -p $$(dirname $@); \
	NAME=$$(basename $@); \
	URL=$$(echo "https://raw.githubusercontent.com/jamesbrond/jamesbrond/main/Makefile/$$NAME"); \
	echo "get $$URL"; \
	curl -s -H 'Cache-Control: no-cache, no-store' $${URL} -o $@

.PHONY: clean distclean dist
.DEFAULT_GOAL := help

clean-dist: clean clean-venv ## Clean-up solution
	@-rm -rf .make
	@-rm -rf dist

clean: clean-pycache clean-pygettext ## Clean-up generated files

deps: py-deps ## Install dependencies

devdeps: py-devdeps ## Install dependencies for depveloper

distclean: clean clean-venv clean-dist ## Clean-up the entire solution

lint: py-lint ## Lint and static-check

# ~@:-]
