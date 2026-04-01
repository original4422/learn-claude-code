.DEFAULT_GOAL := help

EXP_DIR  := experiments
VENV     := $(EXP_DIR)/.venv
PY       := $(VENV)/bin/python
PIP      := $(VENV)/bin/pip

CORE_EXPS := \
	exp_03_core_agent_loop \
	exp_04_tool_system \
	exp_05_permission_engine \
	exp_06_prompt_assembly \
	exp_07_memory_system \
	exp_09_mcp_client \
	exp_10_multi_agent \
	exp_12_streaming_api \
	exp_14_context_compaction

ALL_EXPS := \
	exp_02_startup_flow \
	$(CORE_EXPS) \
	exp_08_terminal_ui \
	exp_11_plugin_skill \
	exp_13_config_system \
	exp_15_command_system \
	exp_16_design_patterns

.PHONY: help setup test-all test-core test lint fmt clean check-venv

help: ## Show this help message
	@echo ""
	@echo "  learn_claude_code"
	@echo "  ================"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "  Examples:"
	@echo "    make setup              Create venv and install dependencies"
	@echo "    make test EXP=03        Run experiment 03 with mock provider"
	@echo "    make test-all           Run all 15 experiments"
	@echo ""

setup: ## Create virtualenv and install dependencies
	@if [ ! -d "$(VENV)" ]; then \
		echo "Creating virtualenv at $(VENV)..."; \
		python3 -m venv $(VENV); \
	fi
	$(PIP) install --upgrade pip -q
	$(PIP) install -r $(EXP_DIR)/requirements.txt -q
	@echo "Done. Activate with: source $(VENV)/bin/activate"

check-venv:
	@test -x "$(PY)" || { echo "Error: venv not found. Run 'make setup' first."; exit 1; }

test-all: check-venv ## Run all 15 experiments (--mock)
	@failed=0; \
	for pkg in $(ALL_EXPS); do \
		printf "  %-35s" "$$pkg"; \
		if cd $(EXP_DIR) && $(abspath $(PY)) -m $$pkg.main --mock > /dev/null 2>&1; then \
			cd ..; echo "\033[32mOK\033[0m"; \
		else \
			cd ..; echo "\033[31mFAIL\033[0m"; failed=$$((failed + 1)); \
		fi; \
	done; \
	if [ $$failed -gt 0 ]; then echo "\n$$failed experiment(s) failed."; exit 1; fi; \
	echo "\nAll experiments passed."

test-core: check-venv ## Run 9 focused-track experiments (--mock)
	@for pkg in $(CORE_EXPS); do \
		printf "  %-35s" "$$pkg"; \
		if cd $(EXP_DIR) && $(abspath $(PY)) -m $$pkg.main --mock > /dev/null 2>&1; then \
			cd ..; echo "\033[32mOK\033[0m"; \
		else \
			cd ..; echo "\033[31mFAIL\033[0m"; \
		fi; \
	done

test: check-venv ## Run one experiment: make test EXP=03
	@test -n "$(EXP)" || { echo "Usage: make test EXP=03"; exit 1; }
	@pkg=$$(ls -d $(EXP_DIR)/exp_$(EXP)_* 2>/dev/null | head -1); \
	if [ -z "$$pkg" ]; then echo "No experiment matching exp_$(EXP)_*"; exit 1; fi; \
	pkg=$$(basename $$pkg); \
	echo "Running $$pkg..."; \
	cd $(EXP_DIR) && $(abspath $(PY)) -m $$pkg.main --mock

lint: check-venv ## Lint experiments and examples with ruff
	@$(PIP) show ruff > /dev/null 2>&1 || $(PIP) install ruff -q
	$(VENV)/bin/ruff check $(EXP_DIR)/ examples/ --config pyproject.toml

fmt: check-venv ## Auto-format code with ruff
	@$(PIP) show ruff > /dev/null 2>&1 || $(PIP) install ruff -q
	$(VENV)/bin/ruff format $(EXP_DIR)/ examples/ --config pyproject.toml

clean: ## Remove virtualenv and cached files
	find . -type d -name __pycache__ -print0 | xargs -0 rm -rf 2>/dev/null || true
	find . -type d -name .ruff_cache -print0 | xargs -0 rm -rf 2>/dev/null || true
	find . -type d -name .pytest_cache -print0 | xargs -0 rm -rf 2>/dev/null || true
	rm -rf $(VENV)
	@echo "Cleaned."
