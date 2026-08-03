
import builtins

from src.dtos.study import StudyDTO, StudyRowDTO
from src.repositories import StudyRepository


class StudyModel:
    repo = StudyRepository()

    async def save(self, dto: StudyDTO) -> StudyDTO:
        study: dict = await self.repo.save(dto)
        return StudyDTO.from_dict(study)

    async def load(self, study_id: int) -> StudyDTO | None:
        study = await self.repo.load(study_id)
        if study:
            return StudyDTO.from_dict(study)
        return None

    async def delete(self, study_id: int):
        await self.repo.delete(study_id)

    async def list(self) -> builtins.list[StudyRowDTO]:
        return await self.repo.list()

    async def study_exists(self, name: str) -> bool:
        return await self.repo.study_exists(name)
