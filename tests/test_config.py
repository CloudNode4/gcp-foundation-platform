from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from gcp_foundation.config import FoundationConfig, load_config, to_tfvars

FIXTURE = Path(__file__).parent / "fixtures" / "minimal.organization.yaml"


def test_load_config() -> None:
    config = load_config(FIXTURE)

    assert config.organization_id == "123456789012"
    assert config.projects["foundation-host"].project_id == "example-foundation-host"
    assert config.networks["foundation-shared-vpc"].subnets[0].ip_cidr_range == "10.0.0.0/24"


def test_invalid_project_id_is_rejected() -> None:
    payload = {
        "organization_id": "123456789012",
        "billing_account": "000000-000000-000000",
        "folders": {"platform": {"display_name": "Platform"}},
        "projects": {
            "bad": {
                "project_id": "INVALID_PROJECT_ID",
                "name": "bad",
                "folder": "platform",
            }
        },
    }

    with pytest.raises(ValidationError):
        FoundationConfig.model_validate(payload)


def test_unknown_folder_reference_is_rejected() -> None:
    payload = {
        "organization_id": "123456789012",
        "billing_account": "000000-000000-000000",
        "folders": {"platform": {"display_name": "Platform"}},
        "projects": {
            "app": {
                "project_id": "example-app-project",
                "name": "app",
                "folder": "missing-folder",
            }
        },
    }

    with pytest.raises(ValidationError):
        FoundationConfig.model_validate(payload)


def test_tfvars_generation_shape() -> None:
    config = load_config(FIXTURE)
    tfvars = to_tfvars(config)

    assert tfvars["organization_id"] == "123456789012"
    assert tfvars["projects"]["foundation-host"]["services"] == [
        "compute.googleapis.com",
        "serviceusage.googleapis.com",
    ]
    assert (
        tfvars["org_policies"]["boolean"]["constraints/compute.skipDefaultNetworkCreation"] is True
    )
