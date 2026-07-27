from dataclasses import field
from datetime import date, datetime
from typing import Dict, Any

from nicegui import binding

from src.models import PatientModel
from src.models import VisitModel
from src.dtos.visit import VisitDTO
from src.tools.validation import is_date
from .patient import PatientViewModel
from .view_model import ViewModel


@binding.bindable_dataclass
class VisitViewModel(ViewModel):
    visit_id: int = 0
    study_id: int = 0
    patient_id: int = 0
    visit_date: str = date.today().isoformat()
    visit_type: str = ""
    comments: str = ""
    changed: bool = False

    created_at: datetime = datetime.now()
    created_by: str = ""
    updated_at: datetime = datetime.now()
    updated_by: str = ""

    is_invalid: bool = False
    validation: str = ""

    patient_name: str = ""
    patient_number: str = ""

    patients: Dict[int, str] = field(default_factory=dict)
    selection: PatientViewModel = field(default_factory=PatientViewModel)

    model = VisitModel()

    def __post_init__(self):
        super().__init__()

    def to_dto(self) -> VisitDTO:
        return VisitDTO(
            visit_id=self.visit_id,
            study_id=self.study_id,
            patient_id=self.patient_id,
            visit_date=date.fromisoformat(self.visit_date),
            visit_type=self.visit_type,
            comments=self.comments,
            created_at=self.created_at,
            created_by=self.created_by,
            updated_at=self.updated_at,
            updated_by=self.updated_by,
        )

    def to_dict(self):
        return {
            "visit_id": self.visit_id,
            "study_id": self.study_id,
            "patient_id": self.patient_id,
            "visit_date": self.visit_date,
            "visit_type": self.visit_type,
            "comments": self.comments,
            "created_at": self.created_at.isoformat(),
            "created_by": self.created_by,
            "updated_at": self.updated_at.isoformat(),
            "updated_by": self.updated_by,
        }

    def from_dict(self, data: dict):
        self.visit_id = data.get("visit_id") or data.get("id") or 0
        self.study_id = data.get("study_id", 0)
        self.patient_id = data.get("patient_id", 0)
        self.visit_date = data.get("visit_date", date.today().isoformat())
        self.visit_type = data.get("visit_type", "")
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
        visit = self.to_dto()
        await self.model.save(visit)
        if visit.visit_id:
            self.visit_id = visit.visit_id
        self.changed = False
        await self.broadcast("visit", "saved")

    async def load(self, visit_id: int):
        visit = await self.model.load(visit_id)
        if visit:
            self.visit_id = visit.visit_id
            self.study_id = visit.study_id
            self.patient_id = visit.patient_id
            self.visit_date = visit.visit_date.isoformat()
            self.visit_type = visit.visit_type
            self.comments = visit.comments
            self.patient_name = visit.patient_name if hasattr(visit, "patient_name") else ""
            self.patient_number = visit.patient_number if hasattr(visit, "patient_number") else ""

            if visit.patient:
                self.selection.from_dict(visit.patient.to_dict())

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "load":
                visit_id = kwargs.get("visit_id")
                if visit_id:
                    await self.load(visit_id)

            case "load_patient":
                patient_id = kwargs.get("patient_id")
                if patient_id:
                    model = PatientModel()
                    patient = await model.load(patient_id)
                    if patient:
                        self.selection.from_dict(patient.to_dict())

            case "load_patients":
                await self.load_patients(kwargs["study_id"])

            case "save":
                await self.save()

            case "validate":
                return await self.validate()
        return None

    async def validate(self) -> bool:
        self.validation = ""
        self.is_invalid = False

        if not self.patient_id or self.patient_id == 0:
            self.validation += "**Patient** is required  \r\n"

        if not self.visit_date:
            self.validation += "**Visit date** is required.  \r\n"
        elif not is_date(self.visit_date):
            self.validation += "**Visit date** must be a valid date.  \r\n"

        if not self.visit_type:
            self.validation += "**Visit type** is required  \r\n"

        self.is_invalid = len(self.validation) > 0
        return not self.is_invalid

    async def load_patients(self, study_id: int):
        model = PatientModel()
        patients = await model.list(study_id)
        self.study_id = study_id
        self.patients = {p.patient_id: p.name for p in patients}
