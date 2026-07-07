# Runbook: Terraform drift detection

## Symptoms

- Terraform plan shows unexpected changes.
- Resources have been modified manually in Google Cloud Console.

## Steps

1. Run a read-only plan:

```bash
terraform -chdir=terraform/foundation plan -refresh-only
```

2. Identify whether drift is intentional.
3. If intentional, update Terraform code or YAML configuration.
4. If accidental, revert the manual change or apply Terraform to restore desired state.
5. Document the incident in the pull request.
