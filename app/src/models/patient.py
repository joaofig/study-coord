from typing import List

from src.dtos.patient import PatientDTO
from src.repositories import PatientRepository


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


class PatientModel:
    repo = PatientRepository()

    async def save(self, dto: PatientDTO):
        patient = await self.repo.save(dto)
        dto.id = patient["id"]

    async def load(self, patient_id: int) -> PatientDTO | None:
        patient = await self.repo.load(patient_id)
        if patient:
            return PatientDTO(**patient)
        return None

    async def delete(self, patient_id: int):
        await self.repo.delete(patient_id)

    async def list(self, study_id: int) -> List[PatientDTO]:
        patients = await self.repo.list(study_id)
        return [PatientDTO(**patient) for patient in patients]
