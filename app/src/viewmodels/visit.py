from dataclasses import field
from datetime import date
from typing import Dict, Any

from nicegui import binding

from models import PatientModel
from src.models import VisitModel
from src.dtos.visit import VisitDTO
from .patient import PatientViewModel
from .view_model import ViewModel


@binding.bindable_dataclass
class VisitViewModel(ViewModel):
    visit_id: int = 0
    study_id: int = 0
    patient_id: int = 0
    visit_date: date = date.today()
    visit_type: str = ""
    comments: str = ""
    changed: bool = False

    patient_name: str = ""
    patient_number: str = ""

    patients: Dict[int, str] = field(default_factory=dict)
    selection: PatientViewModel = field(default_factory=PatientViewModel)

    model = VisitModel()

    def __post_init__(self):
        super().__init__()

    def to_dto(self) -> VisitDTO:
        return VisitDTO(
            id=self.visit_id,
            study_id=self.study_id,
            patient_id=self.patient_id,
            visit_date=self.visit_date,
            visit_type=self.visit_type,
            comments=self.comments,
        )

    async def save(self):
        visit = self.to_dto()
        await self.model.save(visit)
        if visit.id:
            self.visit_id =visit.id
        self.changed = False
        await self.broadcast("visit", "saved")

    async def load(self, visit_id: int):
        visit = await self.model.load(visit_id)
        if visit:
            self.visit_id = visit.id
            self.study_id = visit.study_id
            self.patient_id = visit.patient_id
            self.visit_date = visit.visit_date
            self.visit_type = visit.visit_type
            self.comments = visit.comments
            self.patient_name = visit.patient_name
            self.patient_number = visit.patient_number

            patient = await PatientModel.list(self.patient_id)
            self.selection.copy(patient)

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "load":
                visit_id = kwargs.get("visit_id")
                if visit_id:
                    await self.load(visit_id)

            case "load_patient":
                patient_id = kwargs.get("patient_id")
                if patient_id:
                    patient = await PatientModel.list(self.patient_id)
                    self.selection.copy(patient)

            case "load_patients":
                await self.load_patients(kwargs["study_id"])

            case "save":
                await self.save()
        return None

    async def load_patients(self, study_id: int):
        patients = PatientList()
        await patients.list(study_id)
        self.study_id = study_id
        self.patients = {p.id: p.name for p in patients.patients}
