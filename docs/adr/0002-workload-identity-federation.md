# ADR 0002: Use Workload Identity Federation for GitHub Actions

## Status

Accepted

## Context

Long-lived Google Cloud service account keys are operationally risky and difficult to rotate safely across many repositories.

## Decision

Use GitHub Actions OIDC with Google Cloud Workload Identity Federation for CI/CD authentication.

## Consequences

Positive:

- No static service account keys in GitHub.
- Short-lived credentials.
- Cleaner audit trail.

Negative:

- Requires initial bootstrap configuration.
- Engineers must understand IAM conditions and provider attributes.
