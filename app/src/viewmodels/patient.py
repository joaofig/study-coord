from datetime import date, datetime
from typing import Any

from nicegui import binding
from src.dtos.patient import PatientDTO, patient_statuses
from src.models.patient import PatientModel
from src.tools.messenger import send_message
from src.tools.user import dict_to_datetime
from src.tools.validation import is_date
from src.viewmodels.view_model import ViewModel


@binding.bindable_dataclass
class PatientViewModel(ViewModel):
    patient_id: int = 0
    study_id: int = 0
    number: str = ""
    name: str = ""
    start_date: str = date.today().isoformat()
    exit_date: str | None = None
    status: str = "active"
    status_text: str = ""
    comments: str = ""

    created_at: datetime = datetime.now()
    created_by: str = ""
    updated_at: datetime = datetime.now()
    updated_by: str = ""

    is_invalid: bool = False
    validation: str = ""

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
            start_date=date.fromisoformat(self.start_date),
            exit_date=date.fromisoformat(self.exit_date) if self.exit_date else None,
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
            "start_date": self.start_date,
            "exit_date": self.exit_date,
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
        self.start_date = patient["start_date"]
        self.exit_date = patient["exit_date"]
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
        patient.log_change(self.patient_id)
        await self.model.save(patient)
        if patient.patient_id:
            self.patient_id = patient.patient_id
        await send_message("patient", "saved")
        self.changed = False

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "save":
                await self.save()

            case "validate":
                return await self.validate()
        return None

    async def validate(self) -> bool:
        self.validation = ""
        self.is_invalid = False

        if not self.number:
            self.validation += "**Patient Number** is required  \r\n"
        else:
            if self.patient_id == 0:
                if await self.model.patient_number_exists(self.study_id, self.number):
                    self.validation += "**Patient Number** already exists  \r\n"

        if not self.name:
            self.validation += "**Patient Name** is required  \r\n"
        else:
            if len(self.name) < 3:
                self.validation += (
                    "**Patient Name** must be at least 3 characters  \r\n"
                )
            elif len(self.name) > 128:
                self.validation += (
                    "**Patient Name** must be less than 128 characters  \r\n"
                )

        if self.exit_date and not is_date(self.exit_date):
            self.validation += "**Exit date** must be a valid date.  \r\n"

        if not self.start_date:
            self.validation += "**Start date** is required.  \r\n"

        if self.exit_date and self.start_date and self.exit_date < self.start_date:
            self.validation += "**Exit date** must be after **Start date**.  \r\n"

        if self.status != "active" and not self.exit_date:
            self.validation += (
                "**Exit date** is required for **non-active** patients.  \r\n"
            )

        if self.exit_date and self.status == "active":
            self.validation += (
                "**Exit date** must be empty for **active** patients.  \r\n"
            )

        self.is_invalid = len(self.validation) > 0
        return not self.is_invalid
