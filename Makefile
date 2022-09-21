DIST_DIR     := dist
LOCALES_DIR  := locales
PACKAGE      := todoist_template
PY_HOME      := C:\Users\320072283\bin\python
VERSION_FILE := lib/__version__.py
VERSION_EXP  := (__version__ = \")[0-9\.]+

-include .make/misc.mk
-include .make/py.mk
-include .make/git.mk

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
