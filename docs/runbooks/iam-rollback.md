# Runbook: IAM rollback

## Goal

Rollback a bad additive IAM member change.

## Steps

1. Identify the pull request or commit that introduced the binding.
2. Revert the YAML change.
3. Regenerate tfvars.
4. Run Terraform plan and confirm the IAM member removal.
5. Apply through the normal approved pipeline.

Avoid manual IAM changes unless emergency access is required.
