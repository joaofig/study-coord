from typing import Any

from nicegui.observables import ObservableList

from src.models import PatientModel
from src.viewmodels.view_model import ViewModel


class PatientListViewModel(ViewModel):
    patients = ObservableList()
    study_id: int = 0
    patient_id: int = 0
    model = PatientModel()

    def __init__(self):
        super().__init__()
        self.subscribe(
            channel="study",
            message="selected",
            handler=self._handle_study_selected
        )
        self.subscribe(
            channel="patient_list",
            message="load",
            handler=self._handle_load   # Refresh the patient list
        )

    async def _load_patients(self, study_id: int):
        self.patients.clear()
        self.patients.extend(await self.model.list(study_id))

    async def _handle_study_selected(self, **kwargs):
        study_id = kwargs.get("study_id", 0)
        if study_id:
            self.study_id = int(str(study_id))
            await self._load_patients(self.study_id)
        else:
            self.study_id = 0
            self.patients.clear()
        self.patient_id = 0

    async def _handle_load(self, **kwargs):
        await self._load_patients(self.study_id)

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "load":
                study_id = kwargs.get("study_id", 0)
                if study_id != 0:
                    self.study_id = study_id
                    await self._load_patients(self.study_id)

            case "patient_selected":
                patient_id = kwargs.get("patient_id", 0)
                if patient_id:
                    self.patient_id = patient_id
                    await self.broadcast(
                        channel="patient",
                        message="selected",
                        patient_id=self.patient_id,
                    )

            case "delete_patient":
                patient_id = kwargs.get("patient_id", 0)
                if patient_id:
                    self.patient_id = patient_id
                    await self.model.delete(self.patient_id)
                    await self._load_patients(self.study_id)
        return None
