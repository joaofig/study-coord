from datetime import date

from src.dtos.base import BaseDTO
from src.tools.user import dict_to_date, dict_to_datetime


class AdverseEventDTO(BaseDTO):
    adverse_event_id: int = 0
    study_id: int = 0
    patient_id: int = 0
    event_date: date = date.today()
    event_type: str = ""
    description: str = ""
    comments: str = ""
    patient_number: str = ""
    patient_name: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> "AdverseEventDTO":
        return AdverseEventDTO(
            adverse_event_id=data.get("adverse_event_id", 0),
            study_id=data.get("study_id", 0),
            patient_id=data.get("patient_id", 0),
            event_date=dict_to_date(data, "event_date"),
            event_type=data.get("event_type", ""),
            description=data.get("description", ""),
            comments=data.get("comments", ""),
            patient_number=data.get("patient_number", ""),
            patient_name=data.get("patient_name", ""),
            created_at=dict_to_datetime(data, "created_at"),
            created_by=data.get("created_by", ""),
            updated_at=dict_to_datetime(data, "updated_at"),
            updated_by=data.get("updated_by", ""),
        )

    def to_dict(self) -> dict:
        return {
            "adverse_event_id": self.adverse_event_id,
            "study_id": self.study_id,
            "patient_id": self.patient_id,
            "event_date": self.event_date.isoformat(),
            "event_type": self.event_type,
            "description": self.description,
            "comments": self.comments,
            "patient_number": self.patient_number,
            "patient_name": self.patient_name,
        } | super().to_dict()
