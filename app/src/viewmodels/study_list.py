from typing import Any

from nicegui.observables import ObservableList

from src.models import StudyModel
from src.viewmodels.view_model import ViewModel


class StudyListViewModel(ViewModel):
    studies = ObservableList()
    selected_id: int = 0
    model: StudyModel = StudyModel()

    def __init__(self):
        super().__init__()
        self.selected_id: int = 0
        self.subscribe("study_list", "load", self._on_load)

    async def load(self):
        self.studies.clear()
        studies = await self.model.list()
        self.studies.extend([s.to_dict() for s in studies])

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "load":
                await self.load()

            case "study_saved":
                await self.load()

            case "delete_study":
                study_id = kwargs["study_id"]
                await self.model.delete(study_id)
                await self.load()

            case "study_selected":
                self.selected_id = kwargs["study_id"]
                await self.broadcast(channel="study",
                                     message="selected",
                                     study_id=self.selected_id)
        return None

    async def _on_load(self, **kwargs):
        await self.load()
