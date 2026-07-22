from datetime import date
from typing import Any

from nicegui import binding

from src.dtos.protocol import ProtocolDTO
from src.models.protocol import ProtocolModel
from src.tools.messenger import send_message
from src.viewmodels.view_model import ViewModel


@binding.bindable_dataclass
class ProtocolViewModel(ViewModel):
    protocol_id: int = 0
    study_id: int = 0
    title: str = ""
    event_date: date = date.today()
    description: str = ""

    created_at: date = date.today()
    created_by: str = ""
    updated_at: date = date.today()
    updated_by: str = ""

    changed: bool = False
    model = ProtocolModel()

    def __post_init__(self):
        super().__init__()

    def copy(self, protocol: ProtocolDTO):
        self.protocol_id = protocol.protocol_id or 0
        self.study_id = protocol.study_id
        self.title = protocol.title
        self.event_date = protocol.event_date
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
            event_date=self.event_date,
            description=self.description or "",

            created_at=self.created_at,
            created_by=self.created_by,
            updated_at=self.updated_at,
            updated_by=self.updated_by
        )

    def to_dict(self) -> dict:
        return {
            "protocol_id": self.protocol_id,
            "study_id": self.study_id,
            "title": self.title,
            "event_date": self.event_date.isoformat(),
            "description": self.description or "",

            "created_at": self.created_at.isoformat(),
            "created_by": self.created_by,
            "updated_at": self.updated_at.isoformat(),
            "updated_by": self.updated_by
        }

    def from_dict(self, protocol: dict):
        self.protocol_id = protocol.get("protocol_id", 0)
        self.study_id = protocol.get("study_id", 0)
        self.title = protocol.get("title", "")
        self.event_date = protocol.get("date", date.today())
        self.description = protocol.get("description", "")
        self.created_at = date.fromisoformat(protocol.get("created_at", date.today().isoformat()))
        self.created_by = protocol.get("created_by", "")
        self.updated_at = date.fromisoformat(protocol.get("updated_at", date.today().isoformat()))
        self.updated_by = protocol.get("updated_by", "")

        self.changed = False

    async def save(self):
        protocol = self.to_protocol()
        await self.model.save(protocol)
        if protocol.protocol_id:
            self.protocol_id = protocol.protocol_id
        await send_message("protocol_list", "load", study_id=self.study_id)
        self.changed = False

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "save":
                return await self.save()
        return None
