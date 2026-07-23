from datetime import datetime, date
from pydantic import BaseModel

from src.tools.user import dict_to_date, dict_to_datetime


class MonitoringDTO(BaseModel):
    monitoring_id: int = 0
    study_id: int = 0
    meeting_date: date = date.today()
    monitor: str = ""
    comments: str = ""

    created_at: datetime = datetime.now()
    created_by: str = ""
    updated_at: datetime = datetime.now()
    updated_by: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> MonitoringDTO:
        return MonitoringDTO(
            monitoring_id=data.get("monitoring_id", 0),
            study_id=data.get("study_id", 0),
            meeting_date=dict_to_date(data, "meeting_date"),
            monitor=data.get("monitor", ""),
            comments=data.get("comments", ""),
            created_at=dict_to_datetime(data, "created_at"),
            created_by=data.get("created_by", ""),
            updated_at=dict_to_datetime(data, "updated_at"),
            updated_by=data.get("updated_by", "")
        )

    def to_dict(self) -> dict:
        return {
            "monitoring_id": self.monitoring_id,
            "study_id": self.study_id,
            "meeting_date": self.meeting_date.isoformat(),
            "monitor": self.monitor,
            "comments": self.comments,
            "created_at": self.created_at.isoformat(),
            "created_by": self.created_by,
            "updated_at": self.updated_at.isoformat(),
            "updated_by": self.updated_by
        }
