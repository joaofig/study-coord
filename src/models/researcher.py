from dataclasses import dataclass, field
from models import Study


@dataclass
class Researcher:
    id: int | None = None
    number: str = ""
    name: str = ""
    studies: list[Study] = field(default_factory=list)
    