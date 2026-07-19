from typing import List

from dtos.researcher import StudyResearcherDTO
from src.repositories import StudyResearcherRepository


class StudyResearcherModel:
    def __init__(self):
        self.repo = StudyResearcherRepository()

    async def get(self, sr_id: int) -> StudyResearcherDTO | None:
        researcher = await self.repo.get(sr_id)
        return StudyResearcherDTO(**researcher) if researcher else None

    async def list(self, study_id: int) -> List[StudyResearcherDTO]:
        researchers = await self.repo.list(study_id)
        return [StudyResearcherDTO(**sr) for sr in researchers]

    async def delete(self, researcher_id: int) -> None:
        await self.repo.delete(researcher_id)

    async def save(self, sr: StudyResearcherDTO) -> None:
        await self.repo.save(sr)