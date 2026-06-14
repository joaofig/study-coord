from dataclasses import dataclass

from models import Patient


@dataclass
class AdverseEvent:
    id: int
    patient_id: int
    date: str
    description: str
    comments: str = ""

    patient: Patient | None = None