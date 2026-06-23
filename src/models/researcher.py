from dataclasses import dataclass, field
from src.models import Study


@dataclass
class Researcher:
    id: int | None = None
    number: str = ""
    name: str = ""
    comments: str = ""

    def to_dict(self):
        return {
            "id": self.id,
            "number": self.number,
            "name": self.name,
            "comments": self.comments,
        }


@dataclass
class StudyResearcher(Researcher):
    role: str = ""
    studies: list[Study] = field(default_factory=list)

    def to_dict(self):
        return {
            **super().to_dict(),
            "role": self.role,
        }
    