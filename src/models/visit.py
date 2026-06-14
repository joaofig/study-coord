from dataclasses import dataclass

from models import Patient


@dataclass
class Visit:
    id: int
    patient_id: int
    date: str
    type: str = "visit"
    comments: str = ""

    patient: Patient | None = None