from datetime import date, datetime
from typing import Any, Self

from nicegui import app
from pydantic import BaseModel

from src.dtos.base import BaseDTO
from src.tools.user import dict_to_datetime, get_user_name


class StudyDTO(BaseDTO):
    study_id: int | None
    name: str
    sponsor: str
    start_date: date = date.today()
    end_date: date | None
    protocol_visits: int  # Protocol visits
    comments: str | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            study_id=data.get("study_id") or data.get("id") or 0,
            name=data.get("name", ""),
            sponsor=data.get("sponsor", ""),
            start_date=date.fromisoformat(
                str(data.get("start_date", date.today().isoformat()))
            ),
            end_date=date.fromisoformat(data.get("end_date", date.today().isoformat()))
            if data.get("end_date")
            else None,
            protocol_visits=data.get("protocol_visits")
            or data.get("proto_visits")
            or 1,
            comments=data.get("comments", ""),
            created_at=dict_to_datetime(data, "created_at") or datetime.now(),
            created_by=data.get("created_by", get_user_name()),
            updated_at=dict_to_datetime(data, "updated_at") or datetime.now(),
            updated_by=data.get("updated_by", get_user_name())
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "study_id": self.study_id,
            "name": self.name,
            "sponsor": self.sponsor,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "protocol_visits": self.protocol_visits,
            "comments": self.comments,
        } | super().to_dict()


class StudyRowDTO(BaseModel):
    study_id: int
    name: str
    sponsor: str
    start_date: date = date.today()
    end_date: date | None
    protocol_visits: int  # Protocol visits
    comments: str | None

    patients: int = 0
    visits: int = 0
    researchers: int = 0
    events: int = 0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if isinstance(start_date, str):
            start_date = date.fromisoformat(start_date)
        if isinstance(end_date, str):
            end_date = date.fromisoformat(end_date)

        return cls(
            study_id=data.get("study_id") or data.get("id") or 0,
            name=data.get("name", ""),
            sponsor=data.get("sponsor", ""),
            start_date=start_date,
            end_date=end_date,
            protocol_visits=data.get("protocol_visits")
            or data.get("proto_visits")
            or 1,
            comments=data.get("comments", ""),
            patients=data.get("patients", 0),
            visits=data.get("visits", 0),
            researchers=data.get("researchers", 0),
            events=data.get("events", 0),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "study_id": self.study_id,
            "name": self.name,
            "sponsor": self.sponsor,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "protocol_visits": self.protocol_visits,
            "comments": self.comments,
            "patients": self.patients,
            "visits": self.visits,
            "researchers": self.researchers,
            "events": self.events,
        }
