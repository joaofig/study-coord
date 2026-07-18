from typing import Any

from nicegui import binding
from nicegui.observables import ObservableSet

from src.repositories.RepositoryHub import RepositoryHub
from src.models import Study
from src.viewmodels.view_model import ViewModel


@binding.bindable_dataclass
class StudyViewModel(ViewModel):
    id: int = 0
    name: str = ""
    sponsor: str = ""
    visits: int = 1
    start_date: str = ""
    end_date: str = ""
    comments: str = ""
    data_changed: bool = False
    change_set = ObservableSet()
    changed = False
    is_old: bool = False

    def __post_init__(self):
        super().__init__()
        self.subscribe(channel="study", message="selected", handler=self._handle_study_selected)
        self.repo_hub = RepositoryHub()

    def _field_changed(self, field_name: str):
        self.changed = True
        self.change_set.add(field_name)

    async def _handle_study_selected(self, **kwargs):
        study_row = kwargs.get("study")
        if study_row:
            study_id = study_row.get("id")
            if study_id:
                study = await Study.load(study_id=study_id)
                if study:
                    self.copy(study)

    def copy(self, study: Study):
        self.id = study.id or 0
        self.name = study.name
        self.sponsor = study.sponsor
        self.visits = study.proto_visits
        self.start_date = study.start_date
        self.end_date = study.end_date or ""
        self.comments = study.comments or ""
        self.changed = False
        self.is_old = study.id is not None
        self.change_set.clear()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "sponsor": self.sponsor,
            "protocol_visits": int(self.visits),
            "start_date": self.start_date,
            "end_date": None if self.end_date == "" else self.end_date,
            "comments": self.comments,
        }

    def to_study(self) -> Study:
        return Study(
            id=self.id,
            name=self.name,
            sponsor=self.sponsor,
            proto_visits=int(self.visits),
            start_date=self.start_date,
            end_date=None if self.end_date == "" else self.end_date,
            comments=self.comments,
        )

    async def save(self):
        study = self.to_dict()
        repo = self.repo_hub.get_study_repository()
        study = await repo.save(study)
        await self.broadcast("study", "study_saved", study=study)

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "copy":
                self.copy(kwargs.get("study"))

            case "load":
                study_id = int(kwargs.get("study_id"))
                study = await Study.load(study_id)
                if study:
                    self.copy(study)

            case "save":
                await self.save()
                await self.broadcast("study_list", "load")

            case "mark_changed":
                field_name = kwargs.get("field_name")
                if field_name:
                    self._field_changed(field_name)
        return None
