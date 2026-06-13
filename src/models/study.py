from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Study:
    id: int
    name: str
    sponsor: str
    start_date: str
    end_date: str

