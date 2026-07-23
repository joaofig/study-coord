from datetime import date, datetime

from dtos.base import BaseDTO
from tools.user import dict_to_datetime


def patient_statuses() -> dict:
    return {
        "active": "Active",
        "completed": "Completed",
        "withdrawn": "Withdrawn Consent",
        "lost": "Lost to Follow-up",
        "deceased": "Deceased"
    }


def patient_status_name(status:str) -> str:
    return patient_statuses().get(status, "Unknown")


class PatientDTO(BaseDTO):
    patient_id: int = 0
    study_id: int = 0
    number: str = ""
    name: str = ""
    start_date: date = date.today()
    exit_date: date | None = None
    status: str = "active"
    comments: str = ""

    created_at: datetime = datetime.now()
    created_by: str = ""
    updated_at: datetime = datetime.now()
    updated_by: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> PatientDTO:
        return PatientDTO(
            patient_id=data.get("patient_id", 0),
            study_id=data.get("study_id", 0),
            number=data.get("number", ""),
            name=data.get("name", ""),
            start_date=date.fromisoformat(data.get("start_date", date.today().isoformat())),
            exit_date=date.fromisoformat(data.get("exit_date", date.today().isoformat())) \
                if data.get("exit_date") else None,
            status=data.get("status", "active"),
            comments=data.get("comments", ""),

            created_at=dict_to_datetime(data, "created_at"),
            created_by=data.get("created_by", ""),
            updated_at=dict_to_datetime(data, "updated_at"),
            updated_by=data.get("updated_by", "")
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
            "status_text": patient_status_name(self.status),
            "comments": self.comments,
        } | super().to_dict()
