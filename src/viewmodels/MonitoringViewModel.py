from datetime import date
from typing import Any

from nicegui import binding

from src.models import Monitoring
from tools.messenger import send_message
from viewmodels.ViewModel import ViewModel


@binding.bindable_dataclass
class MonitoringViewModel(ViewModel):
    id: int = 0
    study_id: int = 0
    date: str = date.today().isoformat()
    monitor: str = ""
    comments: str = ""
    changed: bool = False

    def __post_init__(self):
        super().__init__()

    def copy(self, monitoring: Monitoring):
        self.id = monitoring.id or 0
        self.study_id = monitoring.study_id
        self.date = monitoring.date
        self.monitor = monitoring.monitor
        self.comments = monitoring.comments or ""
        self.changed = False

    def to_monitoring(self) -> Monitoring:
        return Monitoring(
            id=self.id,
            study_id=self.study_id,
            date=self.date,
            monitor=self.monitor,
            comments=self.comments or ""
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "study_id": self.study_id,
            "date": self.date,
            "monitor": self.monitor,
            "comments": self.comments or ""
        }

    def from_dict(self, monitoring: dict):
        self.id = monitoring["id"] or 0
        self.study_id = monitoring["study_id"]
        self.date = monitoring["date"]
        self.monitor = monitoring["monitor"]
        self.comments = monitoring["comments"] or ""
        self.changed = False

    async def save(self):
        monitoring = self.to_monitoring()
        await monitoring.save()
        if monitoring.id:
            self.id = monitoring.id
        await send_message("study_list", "load")
        self.changed = False

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "save":
                return await self.save()
        return None
