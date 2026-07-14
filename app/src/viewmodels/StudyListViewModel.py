from typing import Any

from nicegui.observables import ObservableList

from src.db.repository import StudyRepository
from src.models.study import Study
from src.viewmodels.ViewModel import ViewModel


class StudyListViewModel(ViewModel):
    studies = ObservableList()
    selected_id: int = 0

    def __init__(self):
        super().__init__()
        self.selected_id: int = 0
        self.subscribe("study_list", "load", self._on_load)

    async def load(self):
        repo = StudyRepository()
        self.studies.clear()
        self.studies.extend(await repo.list())

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "load":
                await self.load()

            case "study_saved":
                await self.load()

            case "delete_study":
                study_id = kwargs["study_id"]
                await Study.delete(study_id)
                await self.load()

            case "study_selected":
                self.selected_id = kwargs["study_id"]
                await self.broadcast(channel="study",
                                     message="selected",
                                     study_id=self.selected_id)
        return None

    async def _on_load(self, **kwargs):
        await self.load()
