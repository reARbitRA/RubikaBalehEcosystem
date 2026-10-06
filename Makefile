# SPEC-FORGE task entry points.
# The only hard requirement is python3 (>=3.11) and GNU make. Nothing is installed by CI.

PYTHON ?= python3
FORGE_LINT ?= $(PYTHON) tools/forge_lint.py

.PHONY: help bootstrap test lint typecheck forge-lint secret-scan check clean

help: ## Show this help
	@grep -hE '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | \
	  awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

bootstrap: ## Verify the repository tree, tooling and document inventory
	@echo "== SPEC-FORGE bootstrap =="
	@$(PYTHON) --version
	@test -f AGENTS.md || { echo "ERROR: AGENTS.md (the entry point) is missing"; exit 1; }
	@test -f .forge/STATE.md || { echo "ERROR: .forge/STATE.md is missing"; exit 1; }
	@$(FORGE_LINT)
	@echo "bootstrap: OK — next: read .forge/STATE.md, then .forge/LEDGER.md (last 3 entries)"

test: ## Run the test suite (pytest when available, stdlib unittest otherwise)
	@if $(PYTHON) -c "import pytest" 2>/dev/null; then \
	  echo "runner: pytest"; $(PYTHON) -m pytest -q tests; \
	else \
	  echo "runner: unittest (pytest not installed — see quality/TEST-STRATEGY.md §3)"; \
	  $(PYTHON) -m unittest discover -s tests -v; \
	fi

lint: ## Static checks on src/ (no-op until src/ contains code)
	@files=$$(find src -type f ! -name '.gitkeep' 2>/dev/null | wc -l); \
	if [ "$$files" -eq 0 ]; then \
	  echo "lint: OK (no-op: src/ is empty — nothing to lint yet)"; \
	else \
	  echo "lint: $$files file(s) under src/"; \
	  find src -name '*.py' -exec $(PYTHON) -m py_compile {} + && echo "lint: python compile OK"; \
	  if command -v node >/dev/null 2>&1; then \
	    find src -name '*.js' -exec node --check {} \; && echo "lint: javascript syntax OK"; \
	  fi; \
	fi

typecheck: ## Type checks on src/ (no-op until src/ contains code)
	@files=$$(find src -type f ! -name '.gitkeep' 2>/dev/null | wc -l); \
	if [ "$$files" -eq 0 ]; then \
	  echo "typecheck: OK (no-op: src/ is empty)"; \
	elif $(PYTHON) -c "import mypy" 2>/dev/null; then \
	  $(PYTHON) -m mypy src; \
	else \
	  echo "typecheck: OK (no-op: mypy not installed)"; \
	fi

forge-lint: ## Methodology gate: frontmatter, lifecycle, traceability, AC coverage, stale tasks
	@$(FORGE_LINT) $(if $(FORGE_BASE_REF),--base-ref $(FORGE_BASE_REF),)

secret-scan: ## Fail on private keys, .env files and token shapes
	@$(FORGE_LINT) --secrets-only

check: test lint typecheck secret-scan forge-lint ## Run every gate in order

clean: ## Remove caches
	@find . -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null || true
	@find . -name '*.pyc' -delete 2>/dev/null || true
	@echo "clean: OK"
