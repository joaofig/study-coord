from datetime import date
from pydantic import BaseModel


class MonitoringDTO(BaseModel):
    monitoring_id: int = 0
    study_id: int = 0
    meeting_date: date = date.today()
    monitor: str = ""
    comments: str = ""

    created_at: date = date.today().isoformat()
    created_by: str = ""
    updated_at: date = date.today().isoformat()
    updated_by: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> MonitoringDTO:
        today: str = date.today().isoformat()
        return MonitoringDTO(
            monitoring_id=data.get("monitoring_id", 0),
            study_id=data.get("study_id", 0),
            meeting_date=date.fromisoformat(data.get("meeting_date", today)[:10]),
            monitor=data.get("monitor", ""),
            comments=data.get("comments", ""),
            created_at=date.fromisoformat(data.get("created_at", today)[:10]),
            created_by=data.get("created_by", ""),
            updated_at=date.fromisoformat(data.get("updated_at", today)[:10]),
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
