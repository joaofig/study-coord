from typing import Any

from src.models.researcher import ResearcherModel
from nicemvvm.tools.observability import GridList
from nicemvvm.viewmodels.view_model import ViewModel


class ResearcherListViewModel(ViewModel):
    researchers = GridList()
    selected_id: int = 0
    model: ResearcherModel = ResearcherModel()

    def __init__(self):
        super().__init__()
        self.subscribe(channel="study_researcher", message="saved", handler=self._load)

    async def _load(self):
        researchers = [r.to_dict() for r in await self.model.list()]
        self.researchers.replace(researchers)

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "load":
                await self._load()

            case "study_saved":
                await self._load()

            case "researcher_selected":
                if "researcher_id" in kwargs:
                    self.selected_id = kwargs["researcher_id"]

            case "delete":
                researcher_id = kwargs.get("researcher_id", 0)
                if researcher_id:
                    await self.model.delete(researcher_id=researcher_id)
                    self.researchers.delete("researcher_id", researcher_id)
                    await self.broadcast(
                        "researcher", "deleted", researcher_id=researcher_id
                    )
        return None
