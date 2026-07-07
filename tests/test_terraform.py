from __future__ import annotations

from pathlib import Path

import pytest

from gcp_foundation.terraform import build_command


def test_build_plan_command() -> None:
    command = build_command(
        action="plan",
        workdir=Path("terraform/foundation"),
        var_file="terraform.auto.tfvars.json",
        terraform_bin="terraform",
    )

    assert command.as_list() == [
        "terraform",
        "-chdir=terraform/foundation",
        "plan",
        "-var-file=terraform.auto.tfvars.json",
    ]


def test_rejects_unknown_action() -> None:
    with pytest.raises(ValueError):
        build_command(action="explode", workdir="terraform/foundation")
