from dataclasses import field
from datetime import date, datetime
from typing import Dict, Any

from nicegui import binding

from src.dtos.adverse_event import AdverseEventDTO
from src.models import AdverseEventModel, PatientModel
from src.viewmodels.patient import PatientViewModel
from src.viewmodels.view_model import ViewModel


@binding.bindable_dataclass
class AdverseEventViewModel(ViewModel):
    adverse_event_id: int = 0
    study_id: int = 0
    patient_id: int = 0
    event_date: str = date.today().isoformat()
    event_type: str = ""
    description: str = ""
    comments: str = ""
    changed: bool = False

    patient_name: str = ""
    patient_number: str = ""

    created_at: datetime = datetime.now()
    created_by: str = ""
    updated_at: datetime = datetime.now()
    updated_by: str = ""
    
    is_invalid: bool = False
    validation: str = ""

    patients: Dict[int, str] = field(default_factory=dict)
    selection = PatientViewModel()

    model: AdverseEventModel = AdverseEventModel()
    patient_model = PatientModel()

    def __post_init__(self):
        super().__init__()

    def to_event(self) -> AdverseEventDTO:
        return AdverseEventDTO(
            adverse_event_id=self.adverse_event_id,
            study_id=self.study_id,
            patient_id=self.patient_id,
            event_date=date.fromisoformat(self.event_date),
            event_type=self.event_type if self.event_type else "",
            description=self.description,
            comments=self.comments,
        )

    def to_dict(self):
        return {
            "adverse_event_id": self.adverse_event_id,
            "study_id": self.study_id,
            "patient_id": self.patient_id,
            "event_date": self.event_date,
            "event_type": self.event_type,
            "description": self.description,
            "comments": self.comments,
            "patient_name": self.patient_name,
            "patient_number": self.patient_number,
            "created_at": self.created_at.isoformat(),
            "created_by": self.created_by,
            "updated_at": self.updated_at.isoformat(),
            "updated_by": self.updated_by,
        }

    def from_dict(self, data: dict):
        self.adverse_event_id = data.get("adverse_event_id") or data.get("id") or 0
        self.study_id = data.get("study_id", 0)
        self.patient_id = data.get("patient_id", 0)
        self.event_date = data.get("event_date", date.today().isoformat())
        self.event_type = data.get("event_type", "")
        self.description = data.get("description", "")
        self.comments = data.get("comments", "")
        self.patient_name = data.get("patient_name", "")
        self.patient_number = data.get("patient_number", "")
        if "created_at" in data:
             from src.tools.user import dict_to_datetime
             self.created_at = dict_to_datetime(data, "created_at")
        self.created_by = data.get("created_by", "")
        if "updated_at" in data:
             from src.tools.user import dict_to_datetime
             self.updated_at = dict_to_datetime(data, "updated_at")
        self.updated_by = data.get("updated_by", "")
        self.changed = False

    async def save(self):
        event = self.to_event()
        await self.model.save(event)
        if event.adverse_event_id:
            self.adverse_event_id = event.adverse_event_id
        self.changed = False
        await self.broadcast("event", "saved")

    async def load(self, event_id: int):
        event = await self.model.load(event_id)
        if event:
            self.adverse_event_id = event.adverse_event_id
            self.study_id = event.study_id
            self.patient_id = event.patient_id
            self.event_date = event.event_date.isoformat()
            self.event_type = event.event_type
            self.description = event.description
            self.comments = event.comments
            self.patient_name = event.patient_name
            self.patient_number = event.patient_number

            patient = await self.patient_model.load(self.patient_id)
            if patient:
                self.selection.from_dict(patient.to_dict())

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "load":
                event_id = kwargs.get("adverse_event_id", 0)
                if event_id:
                    await self.load(event_id)

            case "load_patient":
                patient_id = kwargs.get("patient_id", 0)
                if patient_id:
                    patient = await self.patient_model.load(patient_id)
                    if patient:
                        self.selection.from_dict(patient.to_dict())

            case "load_patients":
                study_id = kwargs.get("study_id", 0)
                if study_id:
                    await self.load_patients(study_id)

            case "save":
                await self.save()

            case "validate":
                return await self.validate()
        return None

    async def validate(self) -> bool:
        from src.tools.validation import is_date
        self.validation = ""
        self.is_invalid = False

        if not self.patient_id or self.patient_id == 0:
            self.validation += "**Patient** is required  \r\n"

        if not self.event_date:
            self.validation += "**Event date** is required.  \r\n"
        elif not is_date(self.event_date):
            self.validation += "**Event date** must be a valid date.  \r\n"

        if not self.event_type:
            self.validation += "**Event type** is required  \r\n"

        if not self.description:
            self.validation += "**Description** is required  \r\n"

        self.is_invalid = len(self.validation) > 0
        return not self.is_invalid

    async def load_patients(self, study_id: int):
        patients = await self.patient_model.list(study_id)
        self.study_id = study_id
        self.patients = {p.patient_id: p.name for p in patients}
