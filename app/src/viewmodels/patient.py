from datetime import date, datetime
from typing import Any

from nicegui import binding

from src.dtos.patient import PatientDTO, patient_statuses
from src.models import PatientModel
from src.tools.messenger import send_message
from src.viewmodels.view_model import ViewModel
from tools.user import dict_to_datetime


@binding.bindable_dataclass
class PatientViewModel(ViewModel):
    patient_id: int = 0
    study_id: int = 0
    number: str = ""
    name: str = ""
    start_date: date = date.today()
    exit_date: date | None = None
    status: str = "active"
    status_text: str = ""
    comments: str = ""

    created_at: datetime = datetime.now()
    created_by: str = ""
    updated_at: datetime = datetime.now()
    updated_by: str = ""

    statuses = patient_statuses()
    changed: bool = False
    model = PatientModel()

    def __post_init__(self):
        super().__init__()

    def to_dto(self) -> PatientDTO:
        return PatientDTO(
            patient_id=self.patient_id,
            study_id=self.study_id,
            number=self.number,
            name=self.name,
            start_date=self.start_date,
            exit_date=self.exit_date,
            status=self.status,
            comments=self.comments or "",
            created_at=self.created_at,
            created_by=self.created_by,
            updated_at=self.updated_at,
            updated_by=self.updated_by,
        )

    def to_dict(self) -> dict:
        return {
            "patient_id": self.patient_id,
            "study_id": self.study_id,
            "number": self.number,
            "name": self.name,
            "start_date": self.start_date.isoformat(),
            "exit_date": self.exit_date.isoformat() if self.exit_date else None,
            "status": self.status,
            "status_text": self.status_text,
            "comments": self.comments or "",
            "created_at": self.created_at.isoformat(),
            "created_by": self.created_by,
            "updated_at": self.updated_at.isoformat(),
            "updated_by": self.updated_by,
        }

    def from_dict(self, patient: dict):
        self.patient_id = patient["patient_id"] or 0
        self.study_id = patient["study_id"]
        self.number = patient["number"]
        self.name = patient["name"]
        self.start_date = date.fromisoformat(patient["start_date"])
        self.exit_date = date.fromisoformat(patient["exit_date"]) if patient["exit_date"] else None
        self.status = patient["status"]
        self.status_text = patient_statuses().get(patient["status"], "")
        self.comments = patient["comments"] or ""

        self.created_at = dict_to_datetime(patient, "created_at")
        self.created_by = patient["created_by"]
        self.updated_at = dict_to_datetime(patient, "updated_at")
        self.updated_by = patient["updated_by"]
        self.changed = False

    async def save(self):
        patient = self.to_dto()
        await self.model.save(patient)
        if patient.patient_id:
            self.patient_id = patient.patient_id
        await send_message("study_list", "load")
        self.changed = False

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "save":
                return await self.save()
        return None
