from datetime import date
from pydantic import BaseModel


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


class PatientDTO(BaseModel):
    patient_id: int = 0
    study_id: int = 0
    number: str = ""
    name: str = ""
    start_date: date = date.today()
    exit_date: date | None = None
    status: str = "active"
    comments: str = ""

    created_at: date = date.today()
    created_by: str = ""
    updated_at: date = date.today()
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

            created_at=date.fromisoformat(data.get("created_at", date.today().isoformat())),
            created_by=data.get("created_by", ""),
            updated_at=date.fromisoformat(data.get("updated_at", date.today().isoformat())),
            updated_by=data.get("updated_by", ""),
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
            "status_text": patient_status_name(self.status),
            "comments": self.comments,

            "created_at": self.created_at.isoformat(),
            "created_by": self.created_by,
            "updated_at": self.updated_at.isoformat(),
            "updated_by": self.updated_by,
        }