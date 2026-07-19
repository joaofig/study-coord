from typing import List

from src.dtos.visit import VisitDTO
from src.repositories import VisitRepository


class VisitModel:
    def __init__(self):
        self.repo = VisitRepository()

    async def save(self, dto: VisitDTO):
        study: dict = await self.repo.save(dto.to_dict())
        return VisitDTO(**study)

    async def load(self, study_id: int) -> VisitDTO | None:
        return await self.repo.load(study_id)

    async def delete(self, study_id: int):
        await self.repo.delete(study_id)

    async def list(self, study_id: int, patient_id: int = 0) -> List[VisitDTO]:
        return await self.repo.list(study_id, patient_id)
