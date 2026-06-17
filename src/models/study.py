from __future__ import annotations

from dataclasses import dataclass, field

from models import AdverseEvent
from models.patient import Patient
from models.researcher import Researcher
from models.visit import Visit


@dataclass
class Study:
    id: int
    name: str
    sponsor: str
    start_date: str
    end_date: str
    protocol_visits: int
    comments: str

    patients: list[Patient] = field(default_factory=list)
    visits: list[Visit] = field(default_factory=list)
    researchers: list[Researcher] = field(default_factory=list)
    adverse_events: list[AdverseEvent] = field(default_factory=list)


@dataclass
class StudyRow:
    id: int
    name: str
    sponsor: str
    start_date: str
    end_date: str
    
    patients: int
    visits: int
    researchers: int
    adverse_events: int
