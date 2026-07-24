from typing import List

from src.dtos.study import StudyDTO, StudyRowDTO
from src.repositories import StudyRepository


class StudyModel:
    def __init__(self):
        self.repo = StudyRepository()

    async def save(self, dto: StudyDTO):
        study: dict = await self.repo.save(dto)
        return StudyDTO(**study)

    async def load(self, study_id: int) -> StudyDTO | None:
        return await self.repo.load(study_id)

    async def delete(self, study_id: int):
        await self.repo.delete(study_id)

    async def list(self) -> List[StudyRowDTO]:
        return await self.repo.list()
