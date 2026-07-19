from datetime import date
from typing import Any

from pydantic import BaseModel


class StudyDTO(BaseModel):
    id: int | None
    name: str
    sponsor: str
    start_date: date = date.today()
    end_date: date | None
    proto_visits: int   # Protocol visits
    comments: str | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> StudyDTO:
        return StudyDTO(
            id=data.get("id", 0),
            name=data.get("name", ""),
            sponsor=data.get("sponsor", ""),
            start_date=date.fromisoformat(str(data.get("start_date", date.today().isoformat()))),
            end_date=date.fromisoformat(data.get("end_date", date.today().isoformat())) \
                if data.get("end_date") else None,
            proto_visits=data.get("proto_visits", 1),
            comments=data.get("comments", ""),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "sponsor": self.sponsor,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "proto_visits": self.proto_visits,
            "comments": self.comments,
        }


class StudyRowDTO(StudyDTO):
    patients: int = 0
    visits: int = 0
    researcher: int = 0
    events: int = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> StudyRowDTO:
        return StudyRowDTO(**data)