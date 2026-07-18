from dataclasses import dataclass
from typing import List

from src.repositories import MonitoringRepository


@dataclass
class Monitoring:
    id: int = 0
    study_id: int = 0
    date: str = ""
    monitor: str = ""
    comments: str = ""

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "study_id": self.study_id,
            "date": self.date,
            "monitor": self.monitor,
            "comments": self.comments,
        }

    async def save(self):
        repo = MonitoringRepository()
        monitoring = await repo.save(self.to_dict())
        self.id = monitoring["id"]

    @classmethod
    async def load(cls, monitoring_id: int) -> "Monitoring | None":
        repo = MonitoringRepository()
        monitoring = await repo.get(monitoring_id)
        if monitoring:
            return Monitoring(**monitoring)
        return None


class MonitoringList:
    monitoring_visits: list[Monitoring] = []

    async def load_from_study(self, study_id: int) -> List[Monitoring]:
        repo = MonitoringRepository()
        self.monitoring_visits = [Monitoring(**m) for m in await repo.get_by_study_id(study_id)]
        return self.monitoring_visits

    @classmethod
    async def delete(cls, monitoring_id: int):
        repo = MonitoringRepository()
        await repo.delete(monitoring_id)
