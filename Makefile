PROJ_PTH=$(dir $(abspath $(lastword $(MAKEFILE_LIST))))
PYTHON_EXEC?=python

APP_PATH = src/cloudflare_dns_updater

LINT_PATHS = \
$(APP_PATH) \
tests \

run:
	cloudflare_dns_updater

test:
	pytest -n 5

test-ci:
	$(PYTHON_EXEC) -m autoflake --check --recursive --ignore-init-module-imports --remove-duplicate-keys --remove-unused-variables --remove-all-unused-imports $(LINT_PATHS) > /dev/null 2>&1
	$(PYTHON_EXEC) -m isort --check-only $(LINT_PATHS)
	$(PYTHON_EXEC) -m black --check $(LINT_PATHS)
	$(PYTHON_EXEC) -m mypy $(APP_PATH) --ignore-missing-imports
	pytest -n auto --vcr-record=none --cov=cloudflare_dns_updater tests/

lint:
	$(PYTHON_EXEC) -m autoflake --in-place --recursive --ignore-init-module-imports --remove-duplicate-keys --remove-unused-variables --remove-all-unused-imports $(LINT_PATHS)
	$(PYTHON_EXEC) -m black $(LINT_PATHS)
	$(PYTHON_EXEC) -m isort $(LINT_PATHS)
	$(PYTHON_EXEC) -m mypy $(APP_PATH) --ignore-missing-imports


compile-deps:
	$(PYTHON_EXEC) -m piptools compile --no-annotate --no-header "${PROJ_PTH}requirements.in"


recompile-deps:
	$(PYTHON_EXEC) -m piptools compile --no-annotate --no-header --upgrade "${PROJ_PTH}requirements.in"

sync-deps:
	$(PYTHON_EXEC) -m piptools sync "${PROJ_PTH}requirements.txt"
	$(PYTHON_EXEC) -m pip install -e .