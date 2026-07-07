# Security Policy

## Supported versions

This repository is currently in pre-1.0 development. Security fixes are applied to the `main` branch.

## Reporting a vulnerability

Open a private security advisory in GitHub or contact the repository maintainer.

## Secret handling

Never commit:

- Terraform state files,
- service account keys,
- generated `terraform.auto.tfvars.json` files containing real organization data,
- `.env` files,
- kubeconfigs,
- OAuth tokens,
- GitHub personal access tokens.

Use Workload Identity Federation for GitHub Actions and Application Default Credentials for local development.
