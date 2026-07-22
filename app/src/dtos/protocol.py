from datetime import datetime
from pydantic import BaseModel


class ProtocolDTO(BaseModel):
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
    def from_dict(cls, data: dict) -> ProtocolDTO:
        return ProtocolDTO(
            protocol_id=data.get("protocol_id", 0),
            study_id=data.get("study_id", 0),
            title=data.get("title", ""),
            event_date=datetime.fromisoformat(data.get("event_date", datetime.now().isoformat())),
            description=data.get("description", ""),

            created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat())),
            created_by=data.get("created_by", ""),
            updated_at=datetime.fromisoformat(data.get("updated_at", datetime.now().isoformat())),
            updated_by=data.get("updated_by", ""),
        )

    def to_dict(self) -> dict:
        return {
            "protocol_id": self.protocol_id,
            "study_id": self.study_id,
            "title": self.title,
            "event_date": self.event_date.isoformat(),
            "description": self.description,

            "created_at": self.created_at.isoformat(),
            "created_by": self.created_by,
            "updated_at": self.updated_at.isoformat(),
            "updated_by": self.updated_by,
        }
