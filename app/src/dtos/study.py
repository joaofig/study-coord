from typing import Any

from pydantic import BaseModel


class StudyDTO(BaseModel):
    id: int | None
    name: str
    sponsor: str
    start_date: str
    end_date: str | None
    proto_visits: int   # Protocol visits
    comments: str | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> StudyDTO:
        return StudyDTO(**data)

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump()

