from dataclasses import dataclass, field

from db.repository.researcher_repository import ResearcherRepository
from src.models import Study


@dataclass
class Researcher:
    id: int | None = None
    number: str = ""
    name: str = ""
    phone: str = ""
    email: str = ""
    comments: str = ""

    @classmethod
    def empty(cls) -> Researcher:
        return Researcher(None, "", "", "", "", "", "")

    def to_dict(self):
        return {
            "id": self.id,
            "number": self.number,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "comments": self.comments,
        }

    @classmethod
    def from_dict(cls, d: dict) -> Researcher:
        return Researcher(**d)

    async def save(self):
        repo = ResearcherRepository()
        researcher = await repo.save(self.to_dict())
        self.id = researcher["id"]

    @classmethod
    async def load(cls, researcher_id: int) -> Researcher | None:
        repo = ResearcherRepository()
        researcher = await repo.get(researcher_id)
        return Researcher.from_dict(researcher) if researcher else None

@dataclass
class StudyResearcher(Researcher):
    role: str = ""
    studies: list[Study] = field(default_factory=list)

    def to_dict(self):
        return {
            **super().to_dict(),
            "role": self.role,
        }
    