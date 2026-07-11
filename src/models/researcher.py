from dataclasses import dataclass
from typing import List

from db.repository.StudyResearcherRepository import StudyResearcherRepository
from db.repository.ResearcherRepository import ResearcherRepository


@dataclass
class Researcher:
    id: int = 0
    number: str = ""
    name: str = ""
    phone: str = ""
    email: str = ""
    comments: str = ""
    study_count: int = 0

    @classmethod
    def empty(cls) -> Researcher:
        return Researcher(0, "", "", "", "", "", 0)

    def to_dict(self):
        return {
            "id": self.id,
            "number": self.number,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "comments": self.comments,
            "study_count": self.study_count,
        }

    @classmethod
    def from_dict(cls, d: dict) -> Researcher:
        return Researcher(**d)

    async def save(self):
        repo = ResearcherRepository()
        researcher = await repo.save(self.to_dict())
        self.id = researcher["id"]

    @classmethod
    async def delete(cls, researcher_id: int):
        repo = ResearcherRepository()
        await repo.delete(researcher_id)

    @classmethod
    async def load(cls, researcher_id: int) -> Researcher | None:
        repo = ResearcherRepository()
        researcher = await repo.get(researcher_id)
        return Researcher.from_dict(researcher) if researcher else None


def study_researcher_roles() -> dict:
    return {
        "standard": "Standard Researcher",
        "principal": "Principal Researcher",
    }

def study_researcher_role_name(role: str) -> str:
    return study_researcher_roles().get(role, "Unknown")


class ResearcherList:
    researchers: list[Researcher] = []

    async def load(self) -> List[Researcher]:
        repo = ResearcherRepository()
        self.researchers = [Researcher(**r) for r in await repo.list()]
        return self.researchers


@dataclass
class StudyResearcher:
    id: int = 0
    study_id: int = 0
    researcher_id: int = 0
    role: str = ""
    study_comments: str = ""
    number: str = ""
    name: str = ""
    phone: str = ""
    email: str = ""
    # studies: list[Study] = field(default_factory=list)

    def to_dict(self):
        return {
            "id": self.id,
            "study_id": self.study_id,
            "researcher_id": self.researcher_id,
            "role": self.role,
            "role_text": study_researcher_role_name(self.role),
            "study_comments": self.study_comments,
            "number": self.number,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
        }

    def to_researcher(self) -> Researcher | None:
        return Researcher(
            id=self.researcher_id,
            number=self.number,
            name=self.name,
            phone=self.phone,
            email=self.email,
        )

    async def save(self):
        repo = StudyResearcherRepository()
        researcher = await repo.save(self.to_dict())
        self.id = researcher["id"]

    @staticmethod
    async def load(sr_id: int) -> StudyResearcher | None:
        repo = StudyResearcherRepository()
        researcher = await repo.get(sr_id)
        return StudyResearcher(**researcher)


class StudyResearcherList:
    researchers: list[StudyResearcher] = []

    async def load_from_study(self, study_id: int) -> List[StudyResearcher]:
        repo = StudyResearcherRepository()
        self.researchers = [StudyResearcher(**sr) for sr in await repo.list(study_id)]
        return self.researchers