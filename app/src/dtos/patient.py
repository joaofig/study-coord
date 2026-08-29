from datetime import date, datetime
from typing import Self

from src.dtos.base import BaseDTO
from nicemvvm.tools.user import dict_to_date, dict_to_datetime, get_user_name


def patient_statuses() -> dict:
    return {
        "active": "😃 Active",
        "completed": "✅ Completed",
        "withdrawn": "🚫 Withdrawn Consent",
        "screen_failed": "😡 Screening Failure",
        "lost": "🤷‍♂️ Lost to Follow-up",
        "dead": "☠️ Dead",
    }


def patient_status_name(status: str) -> str:
    return patient_statuses().get(status, "Unknown")


class PatientDTO(BaseDTO):
    patient_id: int = 0
    study_id: int = 0
    number: str = ""
    name: str = ""
    start_date: date = date.today()
    exit_date: date | None = None
    status: str = "active"
    status_text: str = "Active"
    comments: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(
            patient_id=data.get("patient_id", 0),
            study_id=data.get("study_id", 0),
            number=data.get("number", ""),
            name=data.get("name", ""),
            start_date=dict_to_date(data, "start_date") or date.today(),
            exit_date=dict_to_date(data, "exit_date", None),
            status=data.get("status", "active"),
            status_text=patient_status_name(data.get("status", "active")),
            comments=data.get("comments", ""),
            created_at=dict_to_datetime(data, "created_at") or datetime.now(),
            created_by=data.get("created_by", get_user_name()),
            updated_at=dict_to_datetime(data, "updated_at") or datetime.now(),
            updated_by=data.get("updated_by", get_user_name()),
        )

    def to_dict(self) -> dict:
        return {
            "patient_id": self.patient_id,
            "study_id": self.study_id,
            "number": self.number,
            "name": self.name,
            "start_date": self.start_date.isoformat(),
            "exit_date": self.exit_date.isoformat() if self.exit_date else None,
            "status": self.status,
            "status_text": self.status_text,
            "comments": self.comments,
        } | super().to_dict()

    def to_grid(self) -> dict:
        return {
            "patient_id": self.patient_id,
            "study_id": self.study_id,
            "number": self.number,
            "name": self.name,
            "start_date": self.start_date.isoformat(),
            "exit_date": self.exit_date.isoformat() if self.exit_date else None,
            "status": self.status,
            "status_text": self.status_text,
            "comments": self.comments,
        } | super().to_dict()
