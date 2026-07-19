from datetime import date
from pydantic import BaseModel


class MonitoringDTO(BaseModel):
    id: int = 0
    study_id: int = 0
    date: date = date.today()
    monitor: str = ""
    comments: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> MonitoringDTO:
        return MonitoringDTO(
            id=data.get("id", 0),
            study_id=data.get("study_id", 0),
            date=date.fromisoformat(data.get("date", date.today().isoformat())),
            monitor=data.get("monitor", ""),
            comments=data.get("comments", ""),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "study_id": self.study_id,
            "date": self.date.isoformat(),
            "monitor": self.monitor,
            "comments": self.comments,
        }
