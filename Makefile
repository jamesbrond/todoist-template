DIST_DIR     := dist
LOCALES_DIR = locales
SRCS         := $(shell /usr/bin/find lib -type f -name '*.py' ! -path '*__pycache__/*') \
                todoist_template.py \
                docs \
                templates \
                LICENSE \
                requirements.txt
VERSION_FILE := lib/__version__.py
PACKAGE := todoist_template

include .make/user.mk
include .make/misc.mk
include .make/py.mk
include .make/git.mk

.PHONY: clean
.DEFAULT_GOAL := help

clean: clean-venv clean-pycache ## Clean-up the solution

# ~@:-]
