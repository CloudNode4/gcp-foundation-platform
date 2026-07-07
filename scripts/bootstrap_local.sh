#!/usr/bin/env bash
set -euo pipefail

python -m venv .venv
# shellcheck source=/dev/null
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
python -m gcp_foundation validate-config --config config/example.organization.yaml
python -m pytest
