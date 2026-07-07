from __future__ import annotations

from pathlib import Path

from gcp_foundation.config import load_config
from gcp_foundation.inventory import render_inventory

FIXTURE = Path(__file__).parent / "fixtures" / "minimal.organization.yaml"


def test_inventory_contains_core_sections() -> None:
    config = load_config(FIXTURE)
    markdown = render_inventory(config)

    assert "# GCP Foundation Inventory" in markdown
    assert "## Folders" in markdown
    assert "example-foundation-host" in markdown
    assert "foundation-shared-vpc" in markdown
