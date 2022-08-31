ifndef DIST_DIR
DIST_DIR = dist
endif

ifndef SRCS
SRCS = .
endif

GIT_CURRENT_BRANCH   := $(shell git rev-parse --abbrev-ref HEAD)
GIT_MAIN_BRANCH      := main
GIT_LATEST_RELEASE   := $(shell git describe --tags --abbrev=0 2>/dev/null)

ZIP_EXE              := 7z
ifdef PACKAGE
ZIP_BASENAME         := $(PACKAGE)
else
ZIP_BASENAME         := $(shell basename $$PWD)
endif
ZIP_MAKELIST_EXCLUDE := $(shell echo "$(MAKEFILE_LIST)" | sed -e 's/ /,/g')

git_checkout = git checkout $(1) --quiet
git_stash    = git stash --include-untracked --quiet
git_rev      = git rev-list --count HEAD
git_unstash  = [[ $$(git stash list | wc -l) -gt 0 ]] && git stash pop --quiet

zip_create   = command -v $(ZIP_EXE) &>/dev/null && \
		$(ZIP_EXE) a -y -bso0 -bsp0 -bse0 $(DIST_DIR)/$(ZIP_BASENAME)-$(1)-$(2).zip -xr@.gitignore -xr!.git* -xr!{$(ZIP_MAKELIST_EXCLUDE)} $(SRCS) || \
		$(call prompt-error,Error: command not found '$(ZIP_EXE)')

ifdef VERSION_FILE
git_update_version = sed -i -r -e "s/__version__ = \"[0-9\.]+\"/__version__ = \"$(1)\"/" $(VERSION_FILE) && git add $(VERSION_FILE) && git commit -m "chore: release $(1)"
else
git_update_version = $(call prompt-log,VERSION_FILE is not defined)
endif

$(DIST_DIR):
	@mkdir -p $(@)

git-release: ## Ask for new git tag, update version and push it to github (releases are in branch main only)
	@$(call prompt-info,Last release: $(GIT_LATEST_RELEASE))
	@$(git_stash) && \
	$(call git_checkout, $(GIT_MAIN_BRANCH)) && \
	while [ -z "$$gittag" ]; do \
		read -r -p "new git tag: " gittag; \
	done && \
	$(call git_update_version,$$gittag) && \
	git tag -a $$gittag -m "new release $$gittag" && \
	git push origin $(GIT_MAIN_BRANCH) --follow-tags && \
	$(call git_checkout, $(GIT_CURRENT_BRANCH)) && \
	$(git_unstash)

zip-release: $(DIST_DIR) ## Create a distributable zip of the latest stable release
ifneq ($(strip $(GIT_LATEST_RELEASE)),)
	@$(git_stash) && \
	$(call git_checkout,$(GIT_LATEST_RELEASE)) && \
	$(call zip_create,$(GIT_LATEST_RELEASE),$$($(git_rev))) && \
	$(call git_checkout,$(CURRENT_BRANCH)) && \
	$(git_unstash)
endif

zip-unstaged: $(DIST_DIR) ## Create a distributable zip of current branch (with unstaged changes)
	@$(call zip_create,$(GIT_CURRENT_BRANCH),$$($(git_rev)))

zip: $(DIST_DIR) ## Create a distributable zip of current branch (without unstaged changes)
	@$(git_stash) && \
	$(call zip_create,$(GIT_CURRENT_BRANCH),$$($(git_rev))) && \
	$(git_unstash)

# ~@:-]
