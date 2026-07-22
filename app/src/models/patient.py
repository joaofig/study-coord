from typing import List

from src.dtos.patient import PatientDTO
from src.repositories import PatientRepository


class PatientModel:
    repo = PatientRepository()

    async def save(self, dto: PatientDTO):
        patient = await self.repo.save(dto)
        dto.patient_id = patient["patient_id"]

    async def load(self, patient_id: int) -> PatientDTO | None:
        return await self.repo.load(patient_id)

    async def delete(self, patient_id: int):
        await self.repo.delete(patient_id=patient_id)

    async def list(self, study_id: int) -> List[PatientDTO]:
        return await self.repo.list(study_id)
