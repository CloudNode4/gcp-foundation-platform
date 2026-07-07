# Onboarding

## For new platform engineers

1. Read `README.md`.
2. Read `docs/architecture.md`.
3. Run local setup:

```bash
scripts/bootstrap_local.sh
```

4. Review the example config in `config/example.organization.yaml`.
5. Generate inventory:

```bash
make inventory
```

6. Review Terraform modules under `terraform/modules`.

## Expected knowledge

- Terraform basics
- Google Cloud resource hierarchy
- IAM and service accounts
- Shared VPC networking
- GitHub Actions basics
- Python packaging basics
