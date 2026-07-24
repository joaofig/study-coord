from datetime import date

from src.dtos.base import BaseDTO
from src.dtos.patient import PatientDTO
from src.tools.user import dict_to_datetime


class VisitDTO(BaseDTO):
    visit_id: int
    study_id: int
    patient_id: int
    visit_date: date = date.today()
    visit_type: str = "visit"
    comments: str = ""

    patient: PatientDTO | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "VisitDTO":
        return VisitDTO(
            visit_id=data.get("visit_id", 0),
            study_id=data.get("study_id", 0),
            patient_id=data.get("patient_id", 0),
            visit_date=date.fromisoformat(
                data.get("visit_date", date.today().isoformat())
            ),
            visit_type=data.get("visit_type", ""),
            comments=data.get("comments", ""),
            created_at=dict_to_datetime(data, "created_at"),
            created_by=data.get("created_by", ""),
            updated_at=dict_to_datetime(data, "updated_at"),
            updated_by=data.get("updated_by", ""),
        )

    def to_dict(self) -> dict:
        return {
            "visit_id": self.visit_id,
            "study_id": self.study_id,
            "patient_id": self.patient_id,
            "visit_date": self.visit_date.isoformat(),
            "visit_type": self.visit_type,
            "comments": self.comments,
        } | super().to_dict()
