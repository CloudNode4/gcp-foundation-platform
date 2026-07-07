from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


VALID_ACTIONS = {"init", "validate", "fmt", "plan", "apply", "destroy"}


@dataclass(frozen=True)
class TerraformCommand:
    executable: str
    action: str
    workdir: Path
    args: tuple[str, ...]

    def as_list(self) -> list[str]:
        return [self.executable, f"-chdir={self.workdir}", self.action, *self.args]


def require_terraform() -> str:
    terraform = shutil.which("terraform")
    if not terraform:
        raise RuntimeError("Terraform binary not found in PATH")
    return terraform


def build_command(
    action: str,
    workdir: str | Path,
    var_file: str | Path | None = None,
    auto_approve: bool = False,
    extra_args: list[str] | None = None,
    terraform_bin: str = "terraform",
) -> TerraformCommand:
    if action not in VALID_ACTIONS:
        raise ValueError(
            f"Unsupported Terraform action '{action}'. Valid actions: {sorted(VALID_ACTIONS)}"
        )

    args: list[str] = []
    if action in {"plan", "apply", "destroy"} and var_file:
        args.append(f"-var-file={var_file}")
    if action in {"apply", "destroy"} and auto_approve:
        args.append("-auto-approve")
    if extra_args:
        args.extend(extra_args)

    return TerraformCommand(
        executable=terraform_bin,
        action=action,
        workdir=Path(workdir),
        args=tuple(args),
    )


def run_command(command: TerraformCommand) -> int:
    completed = subprocess.run(command.as_list(), check=False)
    return completed.returncode
