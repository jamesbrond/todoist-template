include .make/colors.mk
include .make/py.mk
include .make/misc.mk

PACKAGE       := todoist_template

LIB_DIR       := lib
SRCS_DIR      := .

DEVREQ        := devrequirements.txt
VERSION_PY    := $(LIB_DIR)/__version__.py


.DEFAULT_GOAL := help

version       = $$($(VERSION_PY))

clean: clean-venv clean-pycache ## Clean-up the solution

devdeps: deps ## Install both application and developer requirements (pylint, flask8)
	@$(call echoclr,$(BWHITE),Installing developement requirements)
	@$(call install_deps, $(DEVREQ))
	@$(call echoclr,$(GREEN),Done)

# ~@:-]
