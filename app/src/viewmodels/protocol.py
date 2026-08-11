from datetime import date, datetime
from typing import Any

from nicegui import binding
from src.dtos.protocol import ProtocolDTO
from src.models.protocol import ProtocolModel
from src.tools.messenger import send_message
from src.tools.validation import is_date
from src.viewmodels.view_model import ViewModel


@binding.bindable_dataclass
class ProtocolViewModel(ViewModel):
    protocol_id: int = 0
    study_id: int = 0
    title: str = ""
    event_date: str = date.today().isoformat()
    description: str = ""

    created_at: datetime = datetime.now()
    created_by: str = ""
    updated_at: datetime = datetime.now()
    updated_by: str = ""

    is_invalid: bool = False
    validation: str = ""

    changed: bool = False
    model = ProtocolModel()

    def __post_init__(self):
        super().__init__()

    def copy(self, protocol: ProtocolDTO):
        self.protocol_id = protocol.protocol_id or 0
        self.study_id = protocol.study_id
        self.title = protocol.title
        self.event_date = protocol.event_date.isoformat()
        self.description = protocol.description or ""
        self.changed = False

        self.created_at = protocol.created_at
        self.created_by = protocol.created_by
        self.updated_at = protocol.updated_at
        self.updated_by = protocol.updated_by

    def to_protocol(self) -> ProtocolDTO:
        return ProtocolDTO(
            protocol_id=self.protocol_id,
            study_id=self.study_id,
            title=self.title,
            event_date=date.fromisoformat(self.event_date),
            description=self.description or "",
            created_at=self.created_at,
            created_by=self.created_by,
            updated_at=self.updated_at,
            updated_by=self.updated_by,
        )

    def to_dict(self) -> dict:
        return {
            "protocol_id": self.protocol_id,
            "study_id": self.study_id,
            "title": self.title,
            "event_date": self.event_date,
            "description": self.description or "",
            "created_at": self.created_at.isoformat(),
            "created_by": self.created_by,
            "updated_at": self.updated_at.isoformat(),
            "updated_by": self.updated_by,
        }

    def from_dict(self, protocol: dict):
        self.protocol_id = protocol.get("protocol_id") or protocol.get("id") or 0
        self.study_id = protocol.get("study_id", 0)
        self.title = protocol.get("title", "")
        self.event_date = protocol.get("event_date", date.today().isoformat())
        self.description = protocol.get("description", "")
        self.created_at = datetime.fromisoformat(
            protocol.get("created_at", datetime.now().isoformat())
        )
        self.created_by = protocol.get("created_by", "")
        self.updated_at = datetime.fromisoformat(
            protocol.get("updated_at", datetime.now().isoformat())
        )
        self.updated_by = protocol.get("updated_by", "")

        self.changed = False

    async def save(self):
        protocol = self.to_protocol()
        protocol.log_change(self.protocol_id)
        await self.model.save(protocol)
        if protocol.protocol_id:
            self.protocol_id = protocol.protocol_id
        await send_message("protocol_list", "load", study_id=self.study_id)
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

        if not self.title:
            self.validation += "**Title** is required  \r\n"
        else:
            if len(self.title) < 3:
                self.validation += "**Title** must be at least 3 characters  \r\n"
            elif len(self.title) > 128:
                self.validation += "**Title** must be less than 128 characters  \r\n"

        if not self.event_date:
            self.validation += "**Event date** is required.  \r\n"
        elif not is_date(self.event_date):
            self.validation += "**Event date** must be a valid date.  \r\n"

        self.is_invalid = len(self.validation) > 0
        return not self.is_invalid
