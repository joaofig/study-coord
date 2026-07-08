from nicegui.observables import ObservableList

from models.patient import PatientList
from viewmodels.ViewModel import ViewModel


class PatientListViewModel(ViewModel):
    patients = ObservableList()
    study_id: int = 0
    patient_id: int = 0

    def __init__(self):
        super().__init__()
        self.subscribe(channel="study",
                       message="study_selected",
                       handler=self._handle_study_selected)

    async def _load_patients(self, study_id: int):
        patients = PatientList()
        self.patients.clear()
        self.patients.extend([p.to_dict() for p in await patients.load_from_study(study_id)])

    async def _handle_study_selected(self, **kwargs):
        study_id = kwargs.get("study_id")
        if study_id:
            self.study_id = int(study_id)
            await self._load_patients(self.study_id)

    async def _on_call(self, msg: str, **kwargs):
        match msg:
            case "load":
                study_id = kwargs.get("study_id")
                if study_id is not None:
                    self.study_id = int(study_id)
                await self._load_patients(self.study_id)

            case "patient_selected":
                patient_id = kwargs.get("patient_id")
                if patient_id:
                    self.patient_id = int(patient_id)
                    await self.broadcast(channel="patient",
                                         message="selected",
                                         patient_id=patient_id)

            case "delete_patient":
                patient_id = kwargs.get("patient_id")
                if patient_id:
                    self.patient_id = int(patient_id)
                    await PatientList.delete(self.patient_id)
                    await self._load_patients(self.study_id)

        return None

