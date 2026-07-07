from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from gcp_foundation.config import FoundationConfig, to_tfvars


def write_json(data: dict[str, Any], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_tfvars(config: FoundationConfig, output_path: str | Path) -> Path:
    return write_json(to_tfvars(config), output_path)
