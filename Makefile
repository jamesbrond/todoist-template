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


GETTEXT         := /usr/bin/pygettext3.10
MSGFMT          := /mnt/c/Users/320072283/bin/python/Tools/i18n/msgfmt.py
LANG_BASE_FILE  := $(LOCALES_DIR)/$(PACKAGE).pot
LANG_DIRS       := $(shell /usr/bin/find $(LOCALES_DIR)/* -type d -prune)
LANG_SRCS       := $(shell /usr/bin/find $(LOCALES_DIR) -name "*.po" -print)
LANG_OBJS       := $(LANG_SRCS:.po=.mo)

.PHONY: build clean distclean dist lint
.SUFFIXES: .po .mo
.DEFAULT_GOAL := help


.po.mo:
	$(PYTHON) $(MSGFMT) -o $@ $<


build:: ## Compile the entire program
	@$(call log-info,MAKE,$@ done)

clean:: ## Delete all files created by this makefile, however don’t delete the files that record configuration or environment
	@$(call prompt-log,Removing pot file "$(LANG_BASE_FILE)")
	@-rm $(LANG_BASE_FILE)
	@$(call prompt-log,Removing compiled locale translations files)
	@-rm $(LANG_OBJS)
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

$(LANG_BASE_FILE):
	@$(GETTEXT) -d base -o $(LANG_BASE_FILE) $(PY_SRCS)
	@sed -i 's/SOME DESCRIPTIVE TITLE/TODOIST-TEMPLATE LANGUAGE CATALOG/' $(LANG_BASE_FILE)
	@sed -i 's/Copyright (C) YEAR ORGANIZATION/Copyright (C) 2023/' $(LANG_BASE_FILE)
	@sed -i 's/FIRST AUTHOR <EMAIL@ADDRESS>, YEAR/Diego Brondo <jamesbrond@gmail.com>, 2023/' $(LANG_BASE_FILE)

$(LANG_OBJS): $(LANG_SRCS)

$(LOCALES_DIR)/$(ln)/LC_MESSAGES/$(PACKAGE).po: $(LANG_BASE_FILE)
ifdef ln
	@$(call prompt-info,Create empty locale $(@))
	@mkdir -p $(LOCALES_DIR)/$(ln)/LC_MESSAGES
	@-cp $(@) $(@:.po=-$(now).bak) > /dev/null 2>&1 || true
	@cp $(<) $(@)
else
	@$(call prompt-error,Missing language: set it with ln=LANG. Example ln=it)
endif

i18n-base: $(LANG_BASE_FILE)
	@echo $(LANG_DIRS)

i18n-add: $(LOCALES_DIR)/$(ln)/LC_MESSAGES/$(PACKAGE).po ## Create new empty locale. Example usage make pygettext-add ln=it
## Create new empty locale. Example usage make i18n-add ln=it

i18n: $(LANG_OBJS)

# ~@:-]
