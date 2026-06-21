from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from db.repository import StudyRepository


@dataclass
class Study:
    id: int | None
    name: str
    sponsor: str
    start_date: str
    end_date: str | None
    proto_visits: int   # Protocol visits
    comments: str | None

    @classmethod
    def empty(cls) -> Study:
        return Study(None, "", "", "", None, 0, None)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Study:
        return Study(
            id=data.get("id"),
            name=data.get("name", ""),
            sponsor=data.get("sponsor", ""),
            start_date=data.get("start_date", ""),
            end_date=data.get("end_date"),
            proto_visits=data.get("proto_visits", 0),
            comments=data.get("comments"),
        )

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

    def is_valid(self) -> bool:
        """
        Check if the study is valid.
        A study is considered valid if it has a name, sponsor, start date, and at least one protocol visit.
        :return: True if the study is valid, False otherwise.
        """
        if not self.name or not self.sponsor or not self.start_date:
            return False
        if self.proto_visits < 1:
            return False
        return True

    def validation_message(self) -> str:
        """
        Get the validation message for the study.
        :return: Validation message if the study is invalid, empty string otherwise.
        """
        if not self.name:
            return "Study name is required."
        if not self.sponsor:
            return "Sponsor is required."
        if not self.start_date:
            return "Start date is required."
        if self.proto_visits < 1:
            return "At least one protocol visit is required."
        return ""

    async def save(self):
        await StudyRepository.save(self.to_dict())

    @classmethod
    async def load(cls, study_id: int) -> Study | None:
        repo = StudyRepository()
        study = await repo.get(study_id)
        return Study.from_dict(study) if study else None

@dataclass
class StudyRow(Study):
    patients: int
    visits: int
    researchers: int
    adverse_events: int

    def do_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "sponsor": self.sponsor,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "patients": self.patients,
            "visits": self.visits,
            "researchers": self.researchers,
            "adverse_events": self.adverse_events,
        }
