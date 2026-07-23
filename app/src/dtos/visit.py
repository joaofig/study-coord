from datetime import date
from pydantic import BaseModel

from src.dtos.patient import PatientDTO


class VisitDTO(BaseModel):
    id: int
    study_id: int
    patient_id: int
    visit_date: date = date.today()
    visit_type: str = "visit"
    comments: str = ""

    patient: PatientDTO | None = None


    @classmethod
    def from_dict(cls, data: dict) -> VisitDTO:
        return VisitDTO(
            id=data.get("id", 0),
            study_id=data.get("study_id", 0),
            patient_id=data.get("patient_id", 0),
            visit_date=date.fromisoformat(data.get("visit_date", date.today().isoformat())),
            visit_type=data.get("visit_type", ""),
            comments=data.get("comments", ""),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "study_id": self.study_id,
            "patient_id": self.patient_id,
            "visit_date": self.visit_date.isoformat(),
            "visit_type": self.visit_type,
            "comments": self.comments,
        }
