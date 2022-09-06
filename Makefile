DIST_DIR     := dist
LOCALES_DIR  := locales
PACKAGE      := todoist_template
VERSION_FILE := lib/__version__.py
VERSION_EXP  := (__version__ = \")[0-9\.]+

-include .make/user.mk
-include .make/misc.mk
-include .make/py.mk
-include .make/git.mk

.PHONY: clean distclean dist
.DEFAULT_GOAL := help

clean: clean-pycache clean-pygettext ## Clean-up generated files

distclean: clean clean-venv clean-dist ## Clean-up the entire  solution

# ~@:-]
