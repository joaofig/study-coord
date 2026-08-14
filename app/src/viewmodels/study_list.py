from typing import Any

from src.models.study import StudyModel
from src.tools.observability import GridList
from src.viewmodels.view_model import ViewModel


class StudyListViewModel(ViewModel):
    selected_id: int = 0

    def __init__(self):
        super().__init__()
        self.studies = GridList()
        self.model: StudyModel = StudyModel()

        self.subscribe("study", "saved", self._load)
        self.subscribe("patient", "saved", self._load)
        self.subscribe("researcher", "saved", self._load)
        self.subscribe("event", "saved", self._load)
        self.subscribe("visit", "saved", self._load)
        self.subscribe("protocol", "saved", self._load)

    async def _load(self):
        studies = await self.model.list()
        self.studies.replace([s.to_dict() for s in studies])

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "load":
                await self._load()

            case "delete":
                study_id = kwargs["study_id"]
                await self.model.delete(study_id)
                await self._load()
                await self.broadcast("study", message="deleted", study_id=study_id)

            case "select":
                self.selected_id = kwargs.get("study_id", 0)
                if self.selected_id:
                    await self.broadcast("study", message="selected",
                                         study_id=self.selected_id)
        return None
