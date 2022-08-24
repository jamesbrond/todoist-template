VERSION_FILE = lib/__version__.py

include .make/misc.mk
include .make/py.mk
include .make/git.mk

.PHONY: clean
.DEFAULT_GOAL := help

clean: clean-venv clean-pycache ## Clean-up the solution

# ~@:-]
