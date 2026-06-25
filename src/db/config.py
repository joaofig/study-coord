from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tomllib


@dataclass(frozen=True)
class DatabaseConfig:
    path: Path


def load_database_config(config_path: Path | None = None) -> DatabaseConfig:
    project_root = Path(__file__).resolve().parent.parent.parent
    resolved_config_path = config_path or project_root / "study-coord.toml"

    if not resolved_config_path.exists():
        return DatabaseConfig(path=project_root / "study-coord.db")

    with resolved_config_path.open("rb") as config_file:
        raw_config = tomllib.load(config_file)

    database_section = raw_config.get("database", {})
    configured_path = database_section.get("path", "study-coord.db")

    path = Path(configured_path)
    if not path.is_absolute():
        path = project_root / path

    return DatabaseConfig(path=path)
