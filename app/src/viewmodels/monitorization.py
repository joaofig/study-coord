from datetime import date, datetime
from typing import Any

from nicegui import binding
from src.dtos.monitorization import MonitorizationDTO
from src.models.monitorization import MonitorizationModel
from src.tools.messenger import send_message
from src.tools.validation import is_date
from src.viewmodels.view_model import ViewModel


@binding.bindable_dataclass
class MonitorizationViewModel(ViewModel):
    monitoring_id: int = 0
    study_id: int = 0
    meeting_date: str = date.today().isoformat()
    monitor: str = ""
    comments: str = ""
    created_at: datetime = datetime.now()
    created_by: str = ""
    updated_at: datetime = datetime.now()
    updated_by: str = ""
    changed: bool = False

    is_invalid: bool = False
    validation: str = ""

    model = MonitorizationModel()

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

    def to_dto(self) -> MonitorizationDTO:
        return MonitorizationDTO(
            monitoring_id=self.monitoring_id,
            study_id=self.study_id,
            meeting_date=date.fromisoformat(self.meeting_date),
            monitor=self.monitor,
            comments=self.comments or "",
            created_at=self.created_at,
            created_by=self.created_by,
            updated_at=self.updated_at,
            updated_by=self.updated_by,
        )

    def from_dict(self, monitoring: dict):
        self.monitoring_id = (
            monitoring.get("monitoring_id") or monitoring.get("id") or 0
        )
        self.study_id = monitoring.get("study_id", 0)
        self.meeting_date = monitoring.get("meeting_date", date.today().isoformat())
        self.monitor = monitoring.get("monitor", "")
        self.comments = monitoring.get("comments", "")

        if "created_at" in monitoring:
            from src.tools.user import dict_to_datetime

            self.created_at = dict_to_datetime(monitoring, "created_at")
        self.created_by = monitoring.get("created_by", "")

        if "updated_at" in monitoring:
            from src.tools.user import dict_to_datetime

            self.updated_at = dict_to_datetime(monitoring, "updated_at")
        self.updated_by = monitoring.get("updated_by", "")
        self.changed = False

    async def save(self):
        monitoring = self.to_dto()
        monitoring.log_change(self.monitoring_id)
        monitoring = await self.model.save(monitoring)
        if monitoring.monitoring_id:
            self.monitoring_id = monitoring.monitoring_id
        await send_message("monitorization", "saved", monitoring_id=self.monitoring_id)
        self.changed = False

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "save":
                return await self.save()
            case "validate":
                return await self.validate()
        return None

    async def validate(self) -> bool:
        self.validation = ""
        self.is_invalid = False

        if not self.meeting_date:
            self.validation += "**Date** is required.  \r\n"
        elif not is_date(self.meeting_date):
            self.validation += "**Date** must be a valid date.  \r\n"

        if not self.monitor:
            self.validation += "**Monitor** is required.  \r\n"

        self.is_invalid = len(self.validation) > 0
        return not self.is_invalid
