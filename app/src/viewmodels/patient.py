from datetime import date
from typing import Any

from nicegui import binding

from dtos.patient import PatientDTO
from src.models.patient import patient_statuses
from src.models import PatientModel
from src.tools.messenger import send_message
from src.viewmodels.view_model import ViewModel


@binding.bindable_dataclass
class PatientViewModel(ViewModel):
    id: int = 0
    study_id: int = 0
    number: str = ""
    name: str = ""
    start_date: date = date.today().isoformat()
    exit_date: date | None = None
    status: str = "active"
    status_text: str = ""
    comments: str = ""
    statuses = patient_statuses()
    changed: bool = False
    model = PatientModel()

    def __post_init__(self):
        super().__init__()

    def copy(self, patient: PatientDTO):
        self.id = patient.id or 0
        self.study_id = patient.study_id
        self.number = patient.number
        self.name = patient.name
        self.start_date = patient.start_date
        self.exit_date = patient.exit_date
        self.status = patient.status
        self.status_text = patient_statuses().get(patient.status, "")
        self.comments = patient.comments or ""
        self.changed = False

    def to_dto(self) -> PatientDTO:
        return PatientDTO(
            id=self.id,
            study_id=self.study_id,
            number=self.number,
            name=self.name,
            start_date=self.start_date,
            exit_date=self.exit_date,
            status=self.status,
            comments=self.comments or ""
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "study_id": self.study_id,
            "number": self.number,
            "name": self.name,
            "start_date": self.start_date.isoformat(),
            "exit_date": self.exit_date.isoformat() if self.exit_date else None,
            "status": self.status,
            "status_text": self.status_text,
            "comments": self.comments or ""
        }

    def from_dict(self, patient: dict):
        self.id = patient["id"] or 0
        self.study_id = patient["study_id"]
        self.number = patient["number"]
        self.name = patient["name"]
        self.start_date = date.fromisoformat(patient["start_date"])
        self.exit_date = date.fromisoformat(patient["exit_date"]) if patient["exit_date"] else None
        self.status = patient["status"]
        self.status_text = patient_statuses().get(patient["status"], "")
        self.comments = patient["comments"] or ""
        self.changed = False

    async def save(self):
        patient = self.to_dto()
        await self.model.save(patient)
        if patient.id:
            self.id = patient.id
        await send_message("study_list", "load")
        self.changed = False

    async def _on_call(self, msg: str, data: Any = None) -> Any:
        match msg:
            case "save":
                return await self.save()
        return None
