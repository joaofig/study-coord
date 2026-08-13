from typing import Any

from src.models.study import StudyModel
from src.tools.observability import GridList
from src.viewmodels.view_model import ViewModel


class StudyListViewModel(ViewModel):
    selected_id: int = 0

    def __init__(self):
        super().__init__()
        self.studies = GridList()
        self.subscribe("study_list", "load", self._on_load)
        self.model: StudyModel = StudyModel()

    async def load(self):
        studies = await self.model.list()
        self.studies.replace([s.to_dict() for s in studies])

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "load":
                await self.load()

            case "study_saved":
                # study = kwargs["study"]
                # self.studies.append(study.to_dict())
                await self.load()

            case "delete_study":
                study_id = kwargs["study_id"]
                await self.model.delete(study_id)
                await self.load()

            case "select":
                self.selected_id = kwargs.get("study_id", 0)
                if self.selected_id:
                    await self.broadcast("study", message="selected",
                                         study_id=self.selected_id)

        return None

    async def _on_load(self, **kwargs):
        await self.load()
