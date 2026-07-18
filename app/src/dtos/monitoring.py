from pydantic import BaseModel


class MonitoringDTO(BaseModel):
    id: int = 0
    study_id: int = 0
    date: str = ""
    monitor: str = ""
    comments: str = ""

    def to_dict(self) -> dict:
        return self.model_dump()
