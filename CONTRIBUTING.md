# Contributing

## Development workflow

1. Create a feature branch from `main`.
2. Update or add tests for any Python changes.
3. Run local checks:

```bash
make test
make repo-check
```

4. Open a pull request with a clear description and screenshots/diagrams if architecture changes.

## Commit style

Use conventional commits where possible:

```text
feat: add shared vpc nat configuration
fix: validate duplicate subnet names
chore: update terraform provider constraint
```

## Pull request checklist

- [ ] Python tests pass.
- [ ] Terraform files are formatted.
- [ ] Documentation updated.
- [ ] Generated files are not committed.
- [ ] No credentials, state files, or secrets are committed.
