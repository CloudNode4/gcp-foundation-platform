# ADR 0001: Use Python CLI as the platform automation layer

## Status

Accepted

## Context

A GCP foundation repository needs more than Terraform modules. Engineers need a repeatable way to validate input, generate variables, render reports, and run operational commands.

## Decision

Use Python with Typer, Pydantic, Rich, and PyYAML to implement a `gcp-foundation` CLI.

## Consequences

Positive:

- Strong validation before Terraform runs.
- Better developer experience.
- Easy extension for reporting and policy checks.
- Good demonstration of platform engineering skills.

Negative:

- Slightly more maintenance than shell scripts.
- Requires Python packaging discipline.
