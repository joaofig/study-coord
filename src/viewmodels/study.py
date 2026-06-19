import asyncio

from dataclasses import field
from datetime import date
from typing import Any, Mapping

from nicegui import binding

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
    start_date: str = date.today().strftime("%Y-%m-%d")
    end_date: str = ""
    comments: str = ""

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
            from db.repository import StudyRepository
            repo = StudyRepository()
            await repo.save(study)
            if study.id:
                self.id = study.id
            await self.notify("save")
        else:
            from nicegui import ui
            ui.notify(f"Study is not valid. {study.validation_message()}", color="negative")

    async def async_message(self, msg: str, data: Any = None):
        if msg == "save":
            await self.save()

    def message(self, msg: str, data: Any = None):
        """No implementation for synchronous messages in StudyViewModel"""
        pass


class StudyListViewModel(ViewModel):
    studies: list[StudyRow] = []
    study_vm: StudyViewModel = StudyViewModel()

    def __init__(self):
        super().__init__()
        self.study_vm.register(self.async_message)

    async def load(self):
        repo = StudyRepository()
        self.studies = await repo.list()
        await self.async_notify("list_changed")

    async def async_message(self, msg: str, data: Any = None):
        if msg == "save":
            await self.load()

    def message(self, msg: str, data: Any = None):
        """No implementation for synchronous messages in StudyListViewModel"""
        pass