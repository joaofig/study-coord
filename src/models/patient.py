from dataclasses import dataclass
from typing import List

from src.db.repository.PatientRepository import PatientRepository


def patient_statuses() -> dict:
    return {
        "active": "Active",
        "completed": "Completed",
        "withdrawn": "Withdrawn Consent",
        "lost": "Lost to Follow-up",
        "deceased": "Deceased"
    }


def patient_status_name(status:str) -> str:
    return patient_statuses().get(status, "Unknown")


@dataclass
class Patient:
    id: int = 0
    study_id: int = 0
    number: str = ""
    name: str = ""
    start_date: str = ""
    exit_date: str = ""
    status: str = "active"
    comments: str = ""

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "study_id": self.study_id,
            "number": self.number,
            "name": self.name,
            "start_date": self.start_date,
            "exit_date": self.exit_date,
            "status": self.status,
            "status_text": patient_status_name(self.status),
            "comments": self.comments,
        }

    async def save(self):
        repo = PatientRepository()
        study = await repo.save(self.to_dict())
        self.id = study["id"]


class PatientList:
    patients: list[Patient] = []

    async def load_from_study(self, study_id: int) -> List[Patient]:
        repo = PatientRepository()
        self.patients = [Patient(**patient) for patient in await repo.get_by_study_id(study_id)]
        return self.patients