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
        return {
            "id": self.id,
            "name": self.name,
            "sponsor": self.sponsor,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "proto_visits": self.proto_visits,
            "comments": self.comments,
        }
