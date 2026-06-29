from datetime import date
from typing import Any

from nicegui import binding

from models.patient import patient_statuses
from src.models import Patient
from tools.messenger import send_message
from viewmodels.ViewModel import ViewModel


@binding.bindable_dataclass
class PatientViewModel(ViewModel):
    id: int = 0
    study_id: int = 0
    number: str = ""
    name: str = ""
    start_date: str = date.today().isoformat()
    exit_date: str = ""
    status: str = "active"
    comments: str = ""
    statuses = patient_statuses()
    changed: bool = False

    def __post_init__(self):
        super().__init__()

    def copy(self, patient: Patient):
        self.id = patient.id or 0
        self.study_id = patient.study_id
        self.number = patient.number
        self.name = patient.name
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
            name=self.name,
            start_date=self.start_date,
            exit_date=self.exit_date or "",
            status=self.status,
            comments=self.comments or ""
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "study_id": self.study_id,
            "number": self.number,
            "name": self.name,
            "start_date": self.start_date,
            "exit_date": self.exit_date or "",
            "status": self.status,
            "comments": self.comments or ""
        }

    def from_dict(self, patient: dict):
        self.id = patient["id"] or 0
        self.study_id = patient["study_id"]
        self.number = patient["number"]
        self.name = patient["name"]
        self.start_date = patient["start_date"]
        self.exit_date = patient["exit_date"] or ""
        self.status = patient["status"]
        self.comments = patient["comments"] or ""
        self.changed = False

    async def save(self):
        patient = self.to_patient()
        await patient.save()
        if patient.id:
            self.id = patient.id
        await self.notify("patient_saved")
        await send_message("study_list", "load")
        self.changed = False

    async def handle_command(self, msg: str, data: Any = None):
        match msg:
            case "save":
                return await self.save()
        return None
