from typing import List

from src.dtos.study import StudyDTO, StudyRowDTO
from src.repositories import StudyRepository


class StudyModel:
    def __init__(self):
        self.repo = StudyRepository()

    @classmethod
    def empty(cls) -> StudyDTO:
        return StudyDTO(id=None, name="", sponsor="", start_date="", end_date=None, proto_visits=0, comments=None)

    async def save(self, dto: StudyDTO):
        study: dict = await self.repo.save(dto.to_dict())
        return StudyDTO(**study)

    async def load(self, study_id: int) -> StudyDTO | None:
        study = await self.repo.get(study_id)
        return StudyDTO(**study) if study else None

    async def delete(self, study_id: int):
        await self.repo.delete(study_id)

    async def list(self) -> List[StudyRowDTO]:
        return await self.repo.list()
