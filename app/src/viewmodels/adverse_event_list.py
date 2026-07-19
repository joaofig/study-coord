from typing import Any

from nicegui.observables import ObservableList

from models import AdverseEventModel
from src.viewmodels.view_model import ViewModel


class AdverseEventListViewModel(ViewModel):
    def __init__(self):
        super().__init__()
        self.events = ObservableList()
        self.study_id: int = 0
        self.patient_id: int = 0
        self.event_id: int = 0
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

    async def _load_events(self, study_id: int, patient_id: int):
        self.events.clear()
        loaded_events = await self.model.list(study_id, patient_id)
        self.events.extend(loaded_events)

    async def _handle_event_saved(self, **kwargs):
        await self._load_events(self.study_id, self.patient_id)

    async def _handle_study_selected(self, **kwargs):
        study_id = kwargs.get("study_id", 0)
        if study_id:
            self.study_id = int(study_id)
        else:
            self.study_id = 0
            self.event_id = 0
        self.patient_id = 0
        self.events.clear()

    async def _handle_patient_selected(self, **kwargs):
        patient_id = kwargs.get("patient_id", 0)
        if patient_id:
            self.patient_id = int(patient_id)
            await self._load_events(self.study_id, self.patient_id)
        else:
            self.patient_id = 0
            self.event_id = 0
            self.events.clear()

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "load":
                self.study_id = kwargs.get("study_id", self.study_id)
                self.patient_id = kwargs.get("patient_id", self.patient_id)
                if self.study_id and self.patient_id:
                    await self._load_events(self.study_id, self.patient_id)

            case "event_selected":
                event_id = kwargs.get("event_id", 0)
                if event_id:
                    self.event_id = int(event_id)

            case "event_unselected":
                self.event_id = 0

            case "delete":
                event_id = kwargs.get("event_id", 0)
                if event_id:
                    await self.model.delete(event_id)
                    await self._load_events(self.study_id, self.patient_id)
        return None
