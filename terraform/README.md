# Terraform

This directory contains the Terraform implementation for the GCP foundation platform.

- `foundation/` is the root module composition.
- `modules/` contains reusable building blocks.

The root module expects a generated `terraform.auto.tfvars.json` file from the Python CLI.
Do not commit generated tfvars files containing real organization data.
