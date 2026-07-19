from datetime import date
from pydantic import BaseModel


class ProtocolDTO(BaseModel):
    id: int = 0
    study_id: int = 0
    title: str = ""
    date: date = date.today()
    description: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> ProtocolDTO:
        return ProtocolDTO(
            id=data.get("id", 0),
            study_id=data.get("study_id", 0),
            title=data.get("title", ""),
            date=date.fromisoformat(data.get("date", date.today().isoformat())),
            description=data.get("description", ""),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "study_id": self.study_id,
            "title": self.title,
            "date": self.date.isoformat(),
            "description": self.description,
        }
