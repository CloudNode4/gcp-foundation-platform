# Validation Report

Generated on 2026-07-07.

## Completed local checks

| Check | Result |
|---|---:|
| Python bytecode compilation for `src` and `tests` | PASS |
| Python unit tests | PASS, 8 tests |
| CLI config validation against `config/example.organization.yaml` | PASS |
| CLI tfvars generation to temporary file | PASS |
| CLI inventory rendering to temporary file | PASS |
| CLI Terraform dry-run command generation | PASS |
| Repository structure check | PASS |
| YAML parsing for repository YAML files | PASS |
| JSON parsing for repository JSON files | PASS |
| Shell script syntax check with `bash -n` | PASS |
| Basic Terraform HCL delimiter sanity check | PASS |

## Not executed locally

| Check | Reason |
|---|---|
| `terraform init` / `terraform validate` | Terraform binary and provider plugins are not available in the local sandbox environment. The GitHub Actions CI workflow includes these checks with `hashicorp/setup-terraform@v3`. |
| `terraform plan` / `terraform apply` against GCP | Requires real GCP organization ID, billing account, permissions, remote state bucket, and authentication. |
| GCP integration tests | Requires a disposable GCP test organization/project and billing account. |

## Reproduce local checks

```bash
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python -m gcp_foundation validate-config --config config/example.organization.yaml
PYTHONPATH=src python -m gcp_foundation generate-tfvars --config config/example.organization.yaml --output /tmp/foundation.tfvars.json
PYTHONPATH=src python -m gcp_foundation inventory --config config/example.organization.yaml --output /tmp/foundation-inventory.md
PYTHONPATH=src python -m gcp_foundation terraform --action plan --workdir terraform/foundation --var-file terraform.auto.tfvars.json --dry-run
PYTHONPATH=src python -m gcp_foundation check-repo --path .
```

## Recommended first CI run after pushing to GitHub

After creating the repository, push the project and let `.github/workflows/ci.yml` run. That workflow performs Python checks and Terraform `fmt`, `init -backend=false`, and `validate` using Terraform 1.15.7.
