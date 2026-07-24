from datetime import date
from typing import Any

from nicegui import binding

from src.dtos.monitoring import MonitoringDTO
from src.models import MonitoringModel
from src.tools.messenger import send_message
from src.viewmodels.view_model import ViewModel


@binding.bindable_dataclass
class MonitoringViewModel(ViewModel):
    monitoring_id: int = 0
    study_id: int = 0
    meeting_date: date = date.today().isoformat()
    monitor: str = ""
    comments: str = ""
    created_at: date = date.today().isoformat()
    created_by: str = ""
    updated_at: date = date.today().isoformat()
    updated_by: str = ""
    changed: bool = False

    model = MonitoringModel()

    def __post_init__(self):
        super().__init__()

    def to_dict(self) -> dict:
        return {
            "monitoring_id": self.monitoring_id,
            "study_id": self.study_id,
            "meeting_date": self.meeting_date,
            "monitor": self.monitor,
            "comments": self.comments or "",
            "created_at": self.created_at.isoformat(),
            "created_by": self.created_by,
            "updated_at": self.updated_at.isoformat(),
            "updated_by": self.updated_by,
        }

    def to_dto(self) -> MonitoringDTO:
        return MonitoringDTO(
            monitoring_id=self.monitoring_id,
            study_id=self.study_id,
            meeting_date=self.meeting_date,
            monitor=self.monitor,
            comments=self.comments or "",
            created_at=self.created_at,
            created_by=self.created_by,
            updated_at=self.updated_at,
            updated_by=self.updated_by,
        )

    def from_dict(self, monitoring: dict):
        self.monitoring_id = monitoring["monitoring_id"] or 0
        self.study_id = monitoring["study_id"]
        self.meeting_date = monitoring["meeting_date"]
        self.monitor = monitoring["monitor"]
        self.comments = monitoring["comments"] or ""
        self.created_at = date.fromisoformat(monitoring["created_at"])
        self.created_by = monitoring["created_by"]
        self.updated_at = date.fromisoformat(monitoring["updated_at"])
        self.updated_by = monitoring["updated_by"]
        self.changed = False

    async def save(self):
        monitoring = self.to_dto()
        monitoring = await self.model.save(monitoring)
        if monitoring.monitoring_id:
            self.monitoring_id = monitoring.monitoring_id
        await send_message("study_list", "load")
        self.changed = False

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "save":
                return await self.save()
        return None
