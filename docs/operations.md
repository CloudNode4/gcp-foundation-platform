# Operations Guide

## Local authentication

For local development, authenticate with Application Default Credentials:

```bash
gcloud auth application-default login
gcloud config set project YOUR_ADMIN_PROJECT
```

The authenticated principal needs permissions for organization, folder, project, IAM, logging, networking, and policy management.

## GitHub Actions authentication

Use Workload Identity Federation. Do not use long-lived service account JSON keys.

Required repository variables/secrets for `terraform-plan.yml`:

| Name | Type | Description |
|---|---|---|
| `GCP_WORKLOAD_IDENTITY_PROVIDER` | variable or secret | Full Workload Identity Provider resource name |
| `GCP_TERRAFORM_SERVICE_ACCOUNT` | variable or secret | Terraform deployer service account email |

## Terraform backend

Copy the backend example:

```bash
cp terraform/foundation/backend.tf.example terraform/foundation/backend.tf
```

Then replace the bucket name with your real remote state bucket.

## Standard workflow

```bash
gcp-foundation validate-config --config config/organization.yaml
gcp-foundation generate-tfvars --config config/organization.yaml --output terraform/foundation/terraform.auto.tfvars.json
terraform -chdir=terraform/foundation init
terraform -chdir=terraform/foundation plan
```

## Incident response

Use the runbooks in `docs/runbooks` for drift, failed project creation, and IAM rollback scenarios.
