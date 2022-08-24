include .make/misc.mk
include .make/py.mk

PACKAGE       := todoist_template

LIB_DIR       := lib
SRCS_DIR      := .

DEVREQ        := devrequirements.txt
VERSION_PY    := $(LIB_DIR)/__version__.py

.PHONY: clean devdeps
.DEFAULT_GOAL := help

version       = $$($(VERSION_PY))

clean: clean-venv clean-pycache ## Clean-up the solution

devdeps: deps ## Install both application and developer requirements (pylint, flask8)
	@$(call prompt-info,Installing developement requirements)
	@$(call install_deps, $(DEVREQ))

# ~@:-]
