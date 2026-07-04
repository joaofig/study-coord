from dataclasses import field
from typing import Dict

from nicegui import binding

from models import Visit
from models.patient import PatientList, Patient
from models.visit import load_visit
from viewmodels import PatientViewModel
from viewmodels.ViewModel import ViewModel


@binding.bindable_dataclass
class VisitViewModel(ViewModel):
    visit_id: int = 0
    study_id: int = 0
    patient_id: int = 0
    visit_date: str = ""
    visit_type: str = ""
    comments: str = ""
    changed: bool = False

    patient_name: str = ""
    patient_number: str = ""

    patients: Dict[int, str] = field(default_factory=dict)
    selection = PatientViewModel()

    def __post_init__(self):
        super().__init__()

    def to_visit(self) -> Visit:
        return Visit(
            id=self.visit_id,
            study_id=self.study_id,
            patient_id=self.patient_id,
            visit_date=self.visit_date,
            visit_type=self.visit_type,
            comments=self.comments,
        )

    async def save(self):
        visit = self.to_visit()
        await visit.save()
        if visit.id:
            self.visit_id =visit.id
        self.changed = False
        # await self.broadcast("visit", "saved")

    async def load(self, visit_id: int):
        visit = await load_visit(visit_id)
        if visit:
            self.visit_id = visit.id
            self.study_id = visit.study_id
            self.patient_id = visit.patient_id
            self.visit_date = visit.visit_date
            self.visit_type = visit.visit_type
            self.comments = visit.comments
            self.patient_name = visit.patient_name
            self.patient_number = visit.patient_number

    async def _on_message(self, msg: str, **kwargs):
        match msg:
            case "load":
                visit_id = kwargs.get("visit_id")
                if visit_id:
                    await self.load(visit_id)
                    patient = await Patient.load(self.patient_id)
                    self.selection.copy(patient)

            case "load_patients":
                await self.load_patients(kwargs["study_id"])
            case "save":
                await self.save()

    async def load_patients(self, study_id: int):
        patients = PatientList()
        await patients.load_from_study(study_id)
        self.study_id = study_id
        self.patients = {p.id: p.name for p in patients.patients}
