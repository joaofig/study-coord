from typing import Any

from nicegui.observables import ObservableList

from src.models.visit import VisitList
from src.viewmodels.ViewModel import ViewModel


class VisitListViewModel(ViewModel):
    def __init__(self):
        super().__init__()
        self.visits = ObservableList()
        self.study_id: int = 0
        self.patient_id: int = 0
        self.visit_id: int = 0
        self.subscribe(channel="study",
                       message="selected",
                       handler=self._handle_study_selected)
        self.subscribe(channel="visit",
                       message="saved",
                       handler=self._handle_visit_saved)
        self.subscribe(channel="patient",
                       message="selected",
                       handler=self._handle_patient_selected)

    async def _load_visits(self, study_id: int, patient_id: int):
        visits = VisitList()
        self.visits.clear()
        self.visits.extend([v.to_dict() for v in await visits.load_from_study_and_patient(study_id, patient_id)])

    async def _handle_visit_saved(self, **kwargs):
        await self._load_visits(self.study_id, self.patient_id)

    async def _handle_study_selected(self, **kwargs):
        study_id = kwargs.get("study_id")
        if study_id:
            self.study_id = int(study_id)
        else:
            self.study_id = 0
        self.patient_id = 0
        self.visit_id = 0
        self.visits.clear()

    async def _handle_patient_selected(self, **kwargs):
        patient_id = kwargs.get("patient_id")
        if patient_id:
            self.patient_id = int(patient_id)
            await self._load_visits(self.study_id, self.patient_id)
        else:
            self.patient_id = 0
            self.visit_id = 0
            self.visits.clear()

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "load":
                self.study_id = kwargs.get("study_id")
                if self.study_id:
                    await self._load_visits(self.study_id, self.patient_id)
                else:
                    print("Missing study_id parameter.")

            case "study_selected":
                await self._handle_study_selected(**kwargs)

            case "visit_selected":
                self.visit_id = kwargs.get("visit_id")
        return None
