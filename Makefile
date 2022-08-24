include .make/misc.mk
include .make/py.mk

.PHONY: clean
.DEFAULT_GOAL := help

clean: clean-venv clean-pycache ## Clean-up the solution

# ~@:-]
