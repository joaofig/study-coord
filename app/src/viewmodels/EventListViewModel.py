from typing import Any

from nicegui.observables import ObservableList

from src.repositories.RepositoryHub import RepositoryHub
from src.viewmodels.ViewModel import ViewModel


class EventListViewModel(ViewModel):
    def __init__(self):
        super().__init__()
        self.events = ObservableList()
        self.study_id: int = 0
        self.patient_id: int = 0
        self.event_id: int = 0
        self.repo_hub = RepositoryHub()

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
        repo = self.repo_hub.get_event_repository()
        loaded_events = await repo.get_by_study_and_patient(study_id, patient_id)
        self.events.extend([e.to_dict() for e in loaded_events])

    async def _handle_event_saved(self, **kwargs):
        await self._load_events(self.study_id, self.patient_id)

    async def _handle_study_selected(self, **kwargs):
        study_id = kwargs.get("study_id")
        if study_id:
            self.study_id = int(study_id)
        else:
            self.study_id = 0
            self.event_id = 0
        self.patient_id = 0
        self.events.clear()

    async def _handle_patient_selected(self, **kwargs):
        patient_id = kwargs.get("patient_id")
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
                self.event_id = kwargs.get("event_id")

            case "event_unselected":
                self.event_id = 0

            case "delete":
                event_id = kwargs.get("event_id")
                if event_id:
                    repo = self.repo_hub.get_event_repository()
                    await repo.delete(event_id)
                    await self._load_events(self.study_id, self.patient_id)
        return None
