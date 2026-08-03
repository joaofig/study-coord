
import builtins

from src.dtos.researcher import StudyResearcherDTO, StudyResearcherRow
from src.models.researcher import ResearcherModel
from src.models.study import StudyModel
from src.repositories import StudyResearcherRepository


class StudyResearcherModel:
    def __init__(self):
        self.repo = StudyResearcherRepository()

    async def load(self, sr_id: int) -> StudyResearcherDTO | None:
        dto = await self.repo.load(sr_id)
        if dto:
            study_model = StudyModel()
            researcher_model = ResearcherModel()
            if dto.researcher_id:
                dto.researcher = await researcher_model.load(dto.researcher_id)
            if dto.study_id:
                dto.study = await study_model.load(dto.study_id)
        return dto

    async def list(self, study_id: int) -> builtins.list[StudyResearcherRow]:
        return await self.repo.list(study_id)

    async def delete(self, researcher_id: int) -> None:
        await self.repo.delete(researcher_id)

    async def save(self, sr: StudyResearcherDTO) -> None:
        await self.repo.save(sr)
