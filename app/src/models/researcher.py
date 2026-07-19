from typing import List

from src.dtos.researcher import ResearcherDTO
from src.repositories import ResearcherRepository


class ResearcherModel:
    repo = ResearcherRepository()

    @classmethod
    def empty(cls) -> ResearcherDTO:
        return ResearcherDTO(id=0, number="", name="", phone="", email="", comments="", study_count=0)

    async def save(self, dto: ResearcherDTO):
        researcher = await self.repo.save(dto.to_dict())
        dto.id = researcher["id"]

    async def delete(self, researcher_id: int):
        await self.repo.delete(researcher_id)

    async def load(self, researcher_id: int) -> ResearcherDTO | None:
        researcher = await self.repo.get(researcher_id)
        return ResearcherDTO(**researcher) if researcher else None

    async def list(self) -> List[ResearcherDTO]:
        researchers = await self.repo.list()
        return [ResearcherDTO(**r) for r in researchers]


def study_researcher_roles() -> dict:
    return {
        "standard": "Standard Researcher",
        "principal": "Principal Researcher",
    }

def study_researcher_role_name(role: str) -> str:
    return study_researcher_roles().get(role, "Unknown")
