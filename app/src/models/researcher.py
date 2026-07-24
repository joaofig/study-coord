from typing import List

from src.dtos.researcher import ResearcherDTO
from src.repositories import ResearcherRepository


class ResearcherModel:
    repo = ResearcherRepository()

    @classmethod
    def empty(cls) -> ResearcherDTO:
        return ResearcherDTO(
            researcher_id=0, number="", name="", phone="", email="", comments=""
        )

    async def save(self, dto: ResearcherDTO):
        researcher = await self.repo.save(dto)
        dto.researcher_id = researcher["researcher_id"]

    async def delete(self, researcher_id: int):
        await self.repo.delete(researcher_id)

    async def load(self, researcher_id: int) -> ResearcherDTO | None:
        return await self.repo.load(researcher_id)

    async def list(self) -> List[ResearcherDTO]:
        return await self.repo.list()


def study_researcher_roles() -> dict:
    return {
        "standard": "Standard Researcher",
        "principal": "Principal Researcher",
    }


def study_researcher_role_name(role: str) -> str:
    return study_researcher_roles().get(role, "Unknown")
