from typing import Any

from nicegui.observables import ObservableList

from src.viewmodels.view_model import ViewModel
from src.models.protocol import ProtocolModel


class ProtocolListViewModel(ViewModel):
    protocols = ObservableList()
    study_id: int = 0
    protocol_id: int = 0
    model = ProtocolModel()

    def __init__(self):
        super().__init__()
        self.subscribe(
            channel="study", message="selected", handler=self._handle_study_selected
        )
        self.subscribe(
            channel="protocol_list", message="load", handler=self._handle_load
        )

    async def _load_protocols(self, study_id: int):
        self.protocols.clear()
        self.protocols.extend([p.to_dict() for p in await self.model.list(study_id)])

    async def _handle_study_selected(self, **kwargs):
        study_id = kwargs.get("study_id")
        if study_id:
            self.study_id = int(str(study_id))
            await self._load_protocols(self.study_id)
        else:
            self.study_id = 0
            self.protocol_id = 0
            self.protocols.clear()

    async def _handle_load(self, **kwargs):
        study_id = kwargs.get("study_id")
        if study_id:
            self.study_id = int(str(study_id))
            await self._load_protocols(self.study_id)

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "load":
                study_id = kwargs.get("study_id")
                if study_id is not None:
                    self.study_id = int(str(study_id))
                    await self._load_protocols(self.study_id)

            case "protocol_selected":
                protocol_id = kwargs.get("protocol_id")
                if protocol_id:
                    self.protocol_id = int(str(protocol_id))

            case "delete_protocol":
                protocol_id = kwargs.get("protocol_id")
                if protocol_id:
                    self.protocol_id = int(str(protocol_id))
                    await self.model.delete(self.protocol_id)
                    await self._load_protocols(self.study_id)

        return None
