from datetime import date
from pydantic import BaseModel


class VisitDTO(BaseModel):
    id: int                         # Read-only unique identifier for the visit
    study_id: int                   # Identifier for the study associated with the visit
    patient_id: int                 # Identifier for the patient associated with the visit
    visit_date: date = date.today() # Date of the visit
    visit_type: str = "visit"       # Type of the visit
    comments: str = ""              # Additional comments about the visit
    patient_number: str = ""
    patient_name: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> VisitDTO:
        return VisitDTO(
            id=data.get("id", 0),
            study_id=data.get("study_id", 0),
            patient_id=data.get("patient_id", 0),
            visit_date=date.fromisoformat(data.get("visit_date", date.today().isoformat())),
            visit_type=data.get("visit_type", ""),
            comments=data.get("comments", ""),
            patient_number=data.get("patient_number", ""),
            patient_name=data.get("patient_name", ""),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "study_id": self.study_id,
            "patient_id": self.patient_id,
            "visit_date": self.visit_date.isoformat(),
            "visit_type": self.visit_type,
            "comments": self.comments,
            "patient_number": self.patient_number,
            "patient_name": self.patient_name,
        }
