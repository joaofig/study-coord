import builtins

from src.dtos.researcher import ResearcherStudyDTO
from src.repositories.postgres.researcher_study import ResearcherStudyRepository


class ResearcherStudyModel:
    def __init__(self):
        self.repo = ResearcherStudyRepository()

    async def list(self, researcher_id: int) -> builtins.list[ResearcherStudyDTO]:
        return await self.repo.list(researcher_id)