GIT_CURRENT_BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
GIT_MAIN_BRANCH    := main
GIT_LATEST_RELEASE := $(shell git describe --tags --abbrev=0 2>/dev/null)

git_checkout = git checkout $(1) --quiet
git_stash    = git stash --include-untracked --quiet
git_unstash  = [[ $$(git stash list | wc -l) -gt 0 ]] && git stash pop --quiet

ifdef VERSION_FILE
git_update_version = sed -i -r -e 's/__version__ = "[0-9\.]+"/__version__ = "$(1)"/' $(VERSION_FILE) && \
	git add $(VERSION_FILE) && \
	git commit -m "chore: release $(1)"
else
git_update_version = $(call prompt-log,VERSION_FILE is not defined)
endif

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

# ~@:-]
