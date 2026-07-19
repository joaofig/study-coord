from datetime import date
from typing import Any

from nicegui import binding

from dtos.monitoring import MonitoringDTO
from src.models import MonitoringModel
from src.tools.messenger import send_message
from src.viewmodels.view_model import ViewModel


@binding.bindable_dataclass
class MonitoringViewModel(ViewModel):
    id: int = 0
    study_id: int = 0
    date: date = date.today().isoformat()
    monitor: str = ""
    comments: str = ""
    changed: bool = False

    model = MonitoringModel()

    def __post_init__(self):
        super().__init__()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "study_id": self.study_id,
            "date": self.date,
            "monitor": self.monitor,
            "comments": self.comments or ""
        }

    def to_dto(self) -> MonitoringDTO:
        return MonitoringDTO(
            id=self.id,
            study_id=self.study_id,
            date=self.date,
            monitor=self.monitor,
            comments=self.comments or ""
        )

    def from_dict(self, monitoring: dict):
        self.id = monitoring["id"] or 0
        self.study_id = monitoring["study_id"]
        self.date = monitoring["date"]
        self.monitor = monitoring["monitor"]
        self.comments = monitoring["comments"] or ""
        self.changed = False

    async def save(self):
        monitoring = self.to_dto()
        monitoring = await self.model.save(monitoring)
        if monitoring["id"]:
            self.id = monitoring["id"]
        await send_message("study_list", "load")
        self.changed = False

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "save":
                return await self.save()
        return None
