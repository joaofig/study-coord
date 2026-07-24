from datetime import date
from typing import Any, Callable

from nicegui import binding
from nicegui.observables import ObservableSet

from src.dtos.study import StudyDTO
from src.models import StudyModel
from src.viewmodels.view_model import ViewModel


@binding.bindable_dataclass
class StudyViewModel(ViewModel):
    study_id: int = 0
    name: str = ""
    sponsor: str = ""
    protocol_visits: int = 1
    start_date: str = date.today().isoformat()
    end_date: str | None = None
    comments: str = ""
    data_changed: bool = False
    change_set = ObservableSet()
    changed = False
    is_old: bool = False
    model: StudyModel = StudyModel()

    def __post_init__(self):
        super().__init__()
        self.subscribe(
            channel="study", message="selected", handler=self._handle_study_selected
        )

    def _field_changed(self, field_name: str):
        self.changed = True
        self.change_set.add(field_name)

    async def _handle_study_selected(self, **kwargs):
        study_row = kwargs.get("study")
        if study_row:
            study_id = study_row.get("study_id", 0)
            if study_id:
                study = await self.model.load(study_id=study_id)
                if study:
                    self.copy(study)

    def copy(self, study: StudyDTO):
        self.study_id = study.study_id or 0
        self.name = study.name
        self.sponsor = study.sponsor
        self.protocol_visits = study.protocol_visits
        self.start_date = study.start_date.isoformat()
        self.end_date = study.end_date.isoformat() if study.end_date else None
        self.comments = study.comments or ""
        self.changed = False
        self.is_old = study.study_id is not None
        self.change_set.clear()

    def to_dict(self) -> dict:
        return {
            "study_id": self.study_id,
            "name": self.name,
            "sponsor": self.sponsor,
            "protocol_visits": int(self.protocol_visits),
            "start_date": self.start_date,
            "end_date": None if not self.end_date else self.end_date,
            "comments": self.comments,
        }

    def to_dto(self) -> StudyDTO:
        return StudyDTO(
            study_id=self.study_id,
            name=self.name,
            sponsor=self.sponsor,
            protocol_visits=int(self.protocol_visits),
            start_date=date.fromisoformat(self.start_date),
            end_date=None if not self.end_date else date.fromisoformat(self.end_date),
            comments=self.comments,
        )

    async def save(self):
        study = await self.model.save(self.to_dto())
        self.study_id = study.study_id
        await self.broadcast("study", "study_saved", study=study)

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "load":
                study_id = kwargs.get("study_id", 0)
                study = await self.model.load(int(study_id))
                if study:
                    self.copy(study)

            case "save":
                await self.save()
                await self.broadcast("study_list", "load")

            case "mark_changed":
                field_name = kwargs.get("field_name", "")
                if field_name:
                    self._field_changed(field_name)

            case "validate":
                field_name = kwargs.get("field_name", "")
                value = kwargs.get("value", "")
                if field_name and value:
                    return self.validate_field(str(field_name), str(value))
        return None

    def validate_field(self, field_name: str, value: str) -> str:
        match field_name:
            case "name":
                if not value or len(value.strip()) == 0:
                    return "Name is required."
                if len(value) < 3:
                    return "Name must be at least 3 characters long."
                if len(value) > 128:
                    return "Name must be at most 128 characters long."

            case "sponsor":
                if not value or len(value.strip()) == 0:
                    return "Sponsor is required."
                if len(value) < 3:
                    return "Sponsor must be at least 3 characters long."
                if len(value) > 128:
                    return "Sponsor must be at most 128 characters long."
        return ""