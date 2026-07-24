from typing import List

from src.dtos.visit import VisitDTO
from src.repositories import VisitRepository


class VisitModel:
    repo = VisitRepository()

    async def save(self, dto: VisitDTO):
        visit: dict = await self.repo.save(dto)
        dto.visit_id = visit["visit_id"]
        return dto

    async def load(self, visit_id: int) -> VisitDTO | None:
        return await self.repo.load(visit_id)

    async def delete(self, visit_id: int):
        await self.repo.delete(visit_id)

    async def list(self, study_id: int, patient_id: int = 0) -> List[VisitDTO]:
        return await self.repo.list(study_id, patient_id)
