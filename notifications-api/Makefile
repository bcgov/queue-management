.PHONY: setup sync lock export clean clean-build clean-pyc clean-test lint test run run-hot

UV ?= uv
PORT ?= 5002

setup: sync ## Sync the local development environment

sync: ## Install/update dependencies into .venv
	$(UV) sync --group dev

lock: ## Refresh the uv lockfile
	$(UV) lock

export: ## Export pinned requirements files for runtime and dev
	$(UV) export --frozen --no-dev --format requirements.txt --no-emit-project --output-file requirements.txt
	$(UV) export --frozen --group dev --format requirements.txt --no-emit-project --output-file requirements_dev.txt

clean: clean-build clean-pyc clean-test ## Clean the project
	rm -rf .venv/

clean-build: ## Clean build files
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -fr {} +

clean-pyc: ## Clean cache files
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## Clean test output
	find . -name '.pytest_cache' -exec rm -fr {} +
	rm -f .coverage
	rm -f coverage.xml
	rm -fr htmlcov/

lint: ## Lint the project
	$(UV) run ruff check .
	$(UV) run pylint src/api tests

test: ## Run tests
	$(UV) run pytest

run: ## Run the project locally
	$(UV) run python wsgi.py

run-hot: ## Run gunicorn with hot reload
	$(UV) run gunicorn wsgi:application --bind=0.0.0.0:$(PORT) --access-logfile=- --config=gunicorn_config.py --reload --timeout=0

.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
