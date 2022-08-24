help: ## Show Makefile help
# http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@grep -E -h '^[a-zA-Z_\.-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(BLUE)%-20s$(COLOR_OFF) %s\n", $$1, $$2}'

# ~@:-]
