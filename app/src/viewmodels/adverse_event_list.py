from typing import Any

from nicegui.observables import ObservableList

from src.models import AdverseEventModel
from src.viewmodels.view_model import ViewModel


class AdverseEventListViewModel(ViewModel):
    def __init__(self):
        super().__init__()
        self.events = ObservableList()
        self.study_id: int = 0
        self.adverse_event_id: int = 0
        self.model = AdverseEventModel()

        self.subscribe(channel="study",
                       message="selected",
                       handler=self._handle_study_selected)
        self.subscribe(channel="patient",
                       message="selected",
                       handler=self._handle_patient_selected)
        self.subscribe(channel="event",
                       message="saved",
                       handler=self._handle_event_saved)

    async def _load_events(self, study_id: int, adverse_event_id: int):
        self.events.clear()
        loaded_events = await self.model.list(study_id, adverse_event_id)
        self.events.extend(loaded_events)

    async def _handle_event_saved(self, **kwargs):
        await self._load_events(self.study_id, self.adverse_event_id)

    async def _handle_study_selected(self, **kwargs):
        study_id = kwargs.get("study_id", 0)
        if study_id:
            self.study_id = int(study_id)
        else:
            self.study_id = 0
            self.event_id = 0
        self.adverse_event_id = 0
        self.events.clear()

    async def _handle_patient_selected(self, **kwargs):
        patient_id = kwargs.get("adverse_event_id", 0)
        if patient_id:
            self.adverse_event_id = int(patient_id)
            await self._load_events(self.study_id, self.adverse_event_id)
        else:
            self.adverse_event_id = 0
            self.events.clear()

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "load":
                self.study_id = kwargs.get("study_id", self.study_id)
                self.adverse_event_id = kwargs.get("adverse_event_id", self.adverse_event_id)
                if self.study_id and self.adverse_event_id:
                    await self._load_events(self.study_id, self.adverse_event_id)

            case "event_selected":
                adverse_event_id = kwargs.get("adverse_event_id", 0)
                if adverse_event_id:
                    self.adverse_event_id = adverse_event_id

            case "event_unselected":
                self.adverse_event_id = 0

            case "delete":
                adverse_event_id = kwargs.get("adverse_event_id", 0)
                if adverse_event_id:
                    await self.model.delete(adverse_event_id)
                    await self._load_events(self.study_id, self.adverse_event_id)
        return None
