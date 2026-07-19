from dataclasses import field
from datetime import date
from typing import Dict, Any

from nicegui import binding

from dtos.adverse_event import AdverseEventDTO
from models import AdverseEventModel, PatientModel
from src.viewmodels.patient import PatientViewModel
from src.viewmodels.view_model import ViewModel


@binding.bindable_dataclass
class AdverseEventViewModel(ViewModel):
    event_id: int = 0
    study_id: int = 0
    patient_id: int = 0
    event_date: date = date.today()
    event_type: str = ""
    description: str = ""
    comments: str = ""
    changed: bool = False

    patient_name: str = ""
    patient_number: str = ""

    patients: Dict[int, str] = field(default_factory=dict)
    selection = PatientViewModel()

    model: AdverseEventModel = AdverseEventModel()
    patient_model = PatientModel()

    def __post_init__(self):
        super().__init__()

    def to_event(self) -> AdverseEventDTO:
        return AdverseEventDTO(
            id=self.event_id,
            study_id=self.study_id,
            patient_id=self.patient_id,
            event_date=self.event_date,
            event_type=self.event_type if self.event_type else "",
            description=self.description,
            comments=self.comments,
        )

    async def save(self):
        event = self.to_event()
        await self.model.save(event)
        if event.id:
            self.event_id = event.id
        self.changed = False
        await self.broadcast("event", "saved")

    async def load(self, event_id: int):
        event = await self.model.load(event_id)
        if event:
            self.event_id = event.id
            self.study_id = event.study_id
            self.patient_id = event.patient_id
            self.event_date = event.event_date
            self.event_type = event.event_type
            self.description = event.description
            self.comments = event.comments
            self.patient_name = event.patient_name
            self.patient_number = event.patient_number

            patient = await self.patient_model.load(self.patient_id)
            if patient:
                self.selection.copy(patient)

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "load":
                event_id = kwargs.get("event_id")
                if event_id:
                    await self.load(event_id)

            case "load_patient":
                patient_id = kwargs.get("patient_id")
                if patient_id:
                    patient = await self.patient_model.load(patient_id)
                    if patient:
                        self.selection.copy(patient)

            case "load_patients":
                study_id = kwargs.get("study_id")
                if study_id:
                    await self.load_patients(study_id)

            case "save":
                await self.save()
        return None

    async def load_patients(self, study_id: int):
        patients = await self.patient_model.list(study_id)
        self.study_id = study_id
        self.patients = {p.id: p.name for p in patients}
