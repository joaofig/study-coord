from dataclasses import dataclass

from src.db import get_connection
from src.db.repository.patient_repository import PatientRepository


@dataclass
class Patient:
    id: int
    study_id: int
    number: str
    start_date: str
    exit_date: str
    status: str = "active"
    comments: str = ""

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "study_id": self.study_id,
            "number": self.number,
            "start_date": self.start_date,
            "exit_date": self.exit_date,
            "status": self.status,
            "comments": self.comments,
        }

    async def save(self):
        repo = PatientRepository()
        study: dict = await repo.save(self.to_dict())
        self.id = study["id"]


class PatientList:
    patients: list[Patient] = []

    def load_from_study(self, study_id: int):
        conn = get_connection()
        repo = PatientRepository(conn)
        self.patients = repo.get_by_study_id(study_id)