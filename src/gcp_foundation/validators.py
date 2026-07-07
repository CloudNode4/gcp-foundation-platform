from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


REQUIRED_PATHS = [
    "README.md",
    "pyproject.toml",
    "Makefile",
    "config/example.organization.yaml",
    "src/gcp_foundation/cli.py",
    "terraform/foundation/main.tf",
    "terraform/foundation/variables.tf",
    "terraform/foundation/versions.tf",
    "terraform/modules/folder-factory/main.tf",
    "terraform/modules/project-factory/main.tf",
    "terraform/modules/shared-vpc/main.tf",
    "terraform/modules/iam-bindings/main.tf",
    "terraform/modules/org-policies/main.tf",
    "terraform/modules/logging/main.tf",
    "terraform/modules/monitoring/main.tf",
    ".github/workflows/ci.yml",
]

FORBIDDEN_FILES = [
    "terraform.tfstate",
    "terraform.tfstate.backup",
]


@dataclass(frozen=True)
class RepoCheckResult:
    missing_paths: list[str]
    forbidden_paths: list[str]

    @property
    def ok(self) -> bool:
        return not self.missing_paths and not self.forbidden_paths


def check_repo_structure(root: str | Path) -> RepoCheckResult:
    root_path = Path(root)
    missing = [path for path in REQUIRED_PATHS if not (root_path / path).exists()]
    forbidden = [path for path in FORBIDDEN_FILES if (root_path / path).exists()]
    return RepoCheckResult(missing_paths=missing, forbidden_paths=forbidden)
