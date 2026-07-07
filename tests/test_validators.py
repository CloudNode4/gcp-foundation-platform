from __future__ import annotations

from gcp_foundation.validators import check_repo_structure


def test_repo_structure_is_valid() -> None:
    result = check_repo_structure(".")

    assert result.ok, f"missing={result.missing_paths}, forbidden={result.forbidden_paths}"
