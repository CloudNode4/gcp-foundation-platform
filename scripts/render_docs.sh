#!/usr/bin/env bash
set -euo pipefail

python -m gcp_foundation inventory \
  --config config/example.organization.yaml \
  --output docs/generated/inventory.md
