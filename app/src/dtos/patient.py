from datetime import date
from pydantic import BaseModel


class PatientDTO(BaseModel):
    id: int = 0
    study_id: int = 0
    number: str = ""
    name: str = ""
    start_date: date = date.today()
    exit_date: date | None = None
    status: str = "active"
    comments: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> PatientDTO:
        return PatientDTO(
            id=data.get("id", 0),
            study_id=data.get("study_id", 0),
            number=data.get("number", ""),
            name=data.get("name", ""),
            start_date=date.fromisoformat(data.get("start_date", date.today().isoformat())),
            exit_date=date.fromisoformat(data.get("exit_date", date.today().isoformat())) \
                if data.get("exit_date") else None,
            status=data.get("status", "active"),
            comments=data.get("comments", ""),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "study_id": self.study_id,
            "number": self.number,
            "name": self.name,
            "start_date": self.start_date.isoformat(),
            "exit_date": self.exit_date.isoformat() if self.exit_date else None,
            "status": self.status,
            "comments": self.comments,
        }