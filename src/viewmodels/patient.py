from datetime import date
from typing import Any

from nicegui import binding

from src.models import Patient
from viewmodels.view_model import ViewModel


@binding.bindable_dataclass
class PatientViewModel(ViewModel):
    id: int = 0
    study_id: int = 0
    number: str = ""
    start_date: str = date.today().isoformat()
    exit_date: str = ""
    status: str = "active"
    comments: str = ""
    statuses = {
        "active": "Active",
        "completed": "Completed",
        "withdrawn": "Withdrawn Consent",
        "lost": "Lost to Follow-up",
        "deceased": "Deceased"
    }
    changed: bool = False

    def __post_init__(self):
        super().__init__()

    def copy(self, patient: Patient):
        self.id = patient.id or 0
        self.study_id = patient.study_id
        self.number = patient.number
        self.start_date = patient.start_date
        self.exit_date = patient.exit_date or ""
        self.status = patient.status
        self.comments = patient.comments or ""
        self.changed = False

    def to_patient(self) -> Patient:
        return Patient(
            id=self.id,
            study_id=self.study_id,
            number=self.number,
            start_date=self.start_date,
            exit_date=self.exit_date or "",
            status=self.status,
            comments=self.comments or ""
        )

    async def save(self):
        patient = self.to_patient()
        await patient.save()
        if patient.id:
            self.id = patient.id
        await self.async_notify("patient_saved")
        self.changed = False

    async def handle_message(self, msg: str, data: Any = None):
        match msg:
            case "save":
                return await self.save()
        return None


class PatientListViewModel(ViewModel):
    patients: list[dict] = []

    def __post_init__(self):
        super().__init__()

    async def handle_message(self, msg: str, data: Any = None):
        # match msg:
        #     case "load_patients":
        #         study_id = int(data)
        #         patients = await Patient.get_by_study_id(study_id)
        #         self.patients = [PatientViewModel(**patient.__dict__) for patient in patients]
        #         await self.async_notify("patients_loaded")
        return None

    # async def load_patients(self, study_id: int):
    #     patients = await Patient.get_by_study_id(study_id)
    #     self.patients = [PatientViewModel(**patient.__dict__) for patient in patients]
    #     await self.async_notify("patients_loaded")
