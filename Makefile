DIST_DIR     := dist
SRCS         := $(shell /usr/bin/find lib -type f -name '*.py' ! -path '*__pycache__/*') \
                todoist_template.py \
                docs \
                templates \
                LICENSE \
                requirements.txt
VERSION_FILE := lib/__version__.py

include .make/misc.mk
include .make/py.mk
include .make/git.mk

.PHONY: clean
.DEFAULT_GOAL := help

clean: clean-venv clean-pycache ## Clean-up the solution

# ~@:-]
