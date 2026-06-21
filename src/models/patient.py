from dataclasses import dataclass

from db import get_connection
from db.repository.patient_repository import PatientRepository


@dataclass
class Patient:
    id: int
    study_id: int
    study_name: str
    study_sponsor: str
    number: str
    start_date: str
    exit_date: str
    status: str = "active"
    comments: str = ""


class PatientList:
    patients: list[Patient] = []

    def load_from_study(self, study_id: int):
        conn = get_connection()
        repo = PatientRepository(conn)
        self.patients = repo.get_by_study_id(study_id)