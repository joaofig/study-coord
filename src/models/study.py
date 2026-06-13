from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Study:
    name: str
    location_id: int
    start_date: str
    sponsor: str | None = None
    id: int | None = None
