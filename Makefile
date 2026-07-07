.PHONY: help install test repo-check validate-config generate-tfvars inventory clean

help:
	@echo "Available targets:"
	@echo "  install          Install Python package with dev dependencies"
	@echo "  test             Run unit tests"
	@echo "  repo-check       Validate expected repository structure"
	@echo "  validate-config  Validate example organization YAML"
	@echo "  generate-tfvars  Generate Terraform tfvars JSON from example config"
	@echo "  inventory        Generate Markdown inventory from example config"
	@echo "  clean            Remove generated files and caches"

install:
	python -m pip install --upgrade pip
	python -m pip install -e '.[dev]'

test:
	PYTHONPATH=src python -m pytest

repo-check:
	PYTHONPATH=src python -m gcp_foundation check-repo --path .

validate-config:
	PYTHONPATH=src python -m gcp_foundation validate-config --config config/example.organization.yaml

generate-tfvars:
	PYTHONPATH=src python -m gcp_foundation generate-tfvars --config config/example.organization.yaml --output terraform/foundation/terraform.auto.tfvars.json

inventory:
	PYTHONPATH=src python -m gcp_foundation inventory --config config/example.organization.yaml --output docs/generated/inventory.md

clean:
	rm -rf .pytest_cache .ruff_cache .mypy_cache htmlcov .coverage docs/generated
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
