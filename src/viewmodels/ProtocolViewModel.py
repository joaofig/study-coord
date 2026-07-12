from datetime import date
from typing import Any

from nicegui import binding

from src.models.protocol import Protocol
from tools.messenger import send_message
from viewmodels.ViewModel import ViewModel


@binding.bindable_dataclass
class ProtocolViewModel(ViewModel):
    id: int = 0
    study_id: int = 0
    title: str = ""
    date: str = date.today().isoformat()
    description: str = ""
    changed: bool = False

    def __post_init__(self):
        super().__init__()

    def copy(self, protocol: Protocol):
        self.id = protocol.id or 0
        self.study_id = protocol.study_id
        self.title = protocol.title
        self.date = protocol.date
        self.description = protocol.description or ""
        self.changed = False

    def to_protocol(self) -> Protocol:
        return Protocol(
            id=self.id,
            study_id=self.study_id,
            title=self.title,
            date=self.date,
            description=self.description or ""
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "study_id": self.study_id,
            "title": self.title,
            "date": self.date,
            "description": self.description or ""
        }

    def from_dict(self, protocol: dict):
        self.id = protocol.get("id", 0)
        self.study_id = protocol.get("study_id", 0)
        self.title = protocol.get("title", "")
        self.date = protocol.get("date", date.today().isoformat())
        self.description = protocol.get("description", "")
        self.changed = False

    async def save(self):
        protocol = self.to_protocol()
        await protocol.save()
        if protocol.id:
            self.id = protocol.id
        await send_message("protocol_list", "load", study_id=self.study_id)
        self.changed = False

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "save":
                return await self.save()
        return None
