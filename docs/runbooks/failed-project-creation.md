# Runbook: Failed project creation

## Common causes

- Missing billing permissions.
- Project ID already exists globally.
- Organization policy blocks project creation.
- Service Usage API is not available for the bootstrap identity.

## Steps

1. Check Terraform error output.
2. Verify billing account access.
3. Verify folder/project creation roles.
4. Check organization policy constraints.
5. Retry with a unique project ID if needed.
