from datetime import datetime

from src.dtos.base import BaseDTO
from src.tools.user import dict_to_datetime


class ProtocolDTO(BaseDTO):
    protocol_id: int = 0
    study_id: int = 0
    title: str = ""
    event_date: datetime = datetime.now()
    description: str = ""

    created_at: datetime = datetime.now()
    created_by: str = ""
    updated_at: datetime = datetime.now()
    updated_by: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> "ProtocolDTO":
        return ProtocolDTO(
            protocol_id=data.get("protocol_id", 0),
            study_id=data.get("study_id", 0),
            title=data.get("title", ""),
            event_date=datetime.fromisoformat(data.get("event_date", datetime.now().isoformat())),
            description=data.get("description", ""),

            created_at=dict_to_datetime(data, "created_at"),
            created_by=data.get("created_by", ""),
            updated_at=dict_to_datetime(data, "updated_at"),
            updated_by=data.get("updated_by", "")
        )

    def to_dict(self) -> dict:
        return {
            "protocol_id": self.protocol_id,
            "study_id": self.study_id,
            "title": self.title,
            "event_date": self.event_date.isoformat(),
            "description": self.description,
        } | super().to_dict()
