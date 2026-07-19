from typing import List

from src.dtos.researcher import StudyResearcherDTO
from src.models import StudyModel, ResearcherModel
from src.repositories import StudyResearcherRepository


class StudyResearcherModel:
    def __init__(self):
        self.repo = StudyResearcherRepository()

    async def load(self, sr_id: int) -> StudyResearcherDTO | None:
        researcher = await self.repo.get(sr_id)
        dto = StudyResearcherDTO(**researcher) if researcher else None
        if dto:
            study_model = StudyModel()
            researcher_model = ResearcherModel()
            if dto.researcher_id:
                dto.researcher = await researcher_model.load(dto.researcher_id)

            if dto.study_id:
                dto.study = await study_model.load(dto.study_id)
        return dto

    async def list(self, study_id: int) -> List[StudyResearcherDTO]:
        researchers = await self.repo.list(study_id)
        return [StudyResearcherDTO(**sr) for sr in researchers]

    async def delete(self, researcher_id: int) -> None:
        await self.repo.delete(researcher_id)

    async def save(self, sr: StudyResearcherDTO) -> None:
        await self.repo.save(sr.to_dict())