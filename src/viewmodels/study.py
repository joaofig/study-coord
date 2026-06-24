from datetime import date
from typing import Any

from nicegui import binding
from nicegui.observables import ObservableSet

from src.db.repository import StudyRepository
from src.models import Study
from src.models.study import StudyRow
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
    changed: bool = False
    change_set = ObservableSet()
    is_old: bool = False

    def __post_init__(self):
        super().__init__()

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

    def to_study(self) -> Study:
        return Study(
            id=self.id,
            name=self.name,
            sponsor=self.sponsor,
            proto_visits=self.visits,
            start_date=self.start_date,
            end_date=self.end_date,
            comments=self.comments,
        )

    async def save(self):
        study = self.to_study()
        if study.is_valid():
            await study.save()
            if study.id:
                self.id = study.id
            await self.async_notify("study_saved")
            self.changed = False
            self.is_old = True
        else:
            from nicegui import ui
            ui.notify(f"Study is not valid. {study.validation_message()}", color="negative")

    async def handle_message(self, msg: str, data: Any = None):
        match msg:
            case "copy":
                self.copy(data)
            case "load_study":
                study_id = int(data)
                study = await Study.load(study_id)
                if study:
                    self.copy(study)
            case "save_study":
                await self.save()
            case "data_changed":
                # Input controls send this message whenever the user changes the value
                # The data is the changed property name
                self.changed = True
                self.change_set.add(data)


class StudyListViewModel(ViewModel):
    studies: list[StudyRow] = []
    study_vm: StudyViewModel
    sel_row = binding.BindableProperty()

    def __init__(self, study_vm: StudyViewModel):
        super().__init__()
        self.study_vm = study_vm

    async def load(self):
        repo = StudyRepository()
        self.studies = await repo.list()
        await self.async_notify("list_changed")

    async def handle_message(self, msg: str, data: Any = None):
        match msg:
            case "load":
                await self.load()
            case "study_saved":
                await self.load()
            case "study_selected":
                return await self.study_vm.message("load_study", data["id"])
            case "study_unselected":
                await self.study_vm.message("copy", Study.empty())
        return None
