from dataclasses import dataclass, field
from src.models import Study


@dataclass
class Researcher:
    id: int | None = None
    number: str = ""
    name: str = ""
    comments: str = ""
    role: str = ""
    studies: list[Study] = field(default_factory=list)
    