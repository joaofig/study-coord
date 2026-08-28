from typing import Any

from src.models.adverse_event import AdverseEventModel
from src.tools.observability import GridList
from src.viewmodels.view_model import ViewModel


class AdverseEventListViewModel(ViewModel):
    def __init__(self):
        super().__init__()
        self.events = GridList()
        self.study_id: int = 0
        self.patient_id: int = 0
        self.selected_id: int = 0
        self.model = AdverseEventModel()

        self.subscribe(
            channel="study", message="selected", handler=self._handle_study_selected
        )
        self.subscribe(
            channel="patient", message="selected", handler=self._handle_patient_selected
        )
        self.subscribe(
            channel="event", message="saved", handler=self._handle_event_saved
        )

    async def _load_events(self, study_id: int, patient_id: int):
        loaded_events = await self.model.list(study_id, patient_id)
        self.events.replace(loaded_events)

    async def _handle_event_saved(self, **kwargs):
        await self._load_events(self.study_id, self.patient_id)

    async def _handle_study_selected(self, **kwargs):
        study_id = kwargs.get("study_id", 0)
        if study_id:
            self.study_id = int(study_id)
        else:
            self.study_id = 0
            self.patient_id = 0
        self.patient_id = 0
        self.selected_id = 0
        self.events.clear()

    async def _handle_patient_selected(self, **kwargs):
        patient_id = kwargs.get("selected_id", 0)
        if patient_id:
            self.patient_id = int(patient_id)
            await self._load_events(self.study_id, self.patient_id)
        else:
            self.patient_id = 0
            self.selected_id = 0
            self.events.clear()

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "load":
                self.study_id = kwargs.get("study_id", self.study_id)
                self.patient_id = kwargs.get(
                    "patient_id", kwargs.get("adverse_event_id", self.patient_id)
                )
                if self.study_id and self.patient_id:
                    await self._load_events(self.study_id, self.patient_id)

            case "select":
                adverse_event_id = kwargs.get("selected_id", 0)
                if adverse_event_id:
                    self.selected_id = adverse_event_id

            case "delete":
                adverse_event_id = kwargs.get("selected_id", 0)
                if adverse_event_id:
                    await self.model.delete(adverse_event_id)
                    await self._load_events(self.study_id, self.patient_id)
                    await self.broadcast(
                        "adverse_event", "deleted", adverse_event_id=adverse_event_id
                    )
        return None
