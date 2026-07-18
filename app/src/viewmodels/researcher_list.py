from typing import Any

from nicegui.observables import ObservableList

from src.db.repository.ResearcherRepository import ResearcherRepository
from src.models import Researcher
from src.viewmodels.view_model import ViewModel


class ResearcherListViewModel(ViewModel):
    researchers = ObservableList()
    selected_id: int = 0

    def __init__(self):
        super().__init__()
        self.subscribe(channel="researcher_list",
                       message="load",
                       handler=self._on_load)

    async def load(self):
        repo = ResearcherRepository()
        self.researchers.clear()
        self.researchers.extend([Researcher(**s) for s in await repo.list()])

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "load":
                await self.load()

            case "study_saved":
                await self.load()

            case "researcher_selected":
                if "researcher_id" in kwargs:
                    self.selected_id = kwargs["researcher_id"]

            case "delete":
                researcher_id = kwargs.get("researcher_id")
                await Researcher.delete(researcher_id=int(researcher_id))
                await self.load()
                await self.broadcast("researcher_list", "load")
        return None

    async def _on_load(self, **kwargs):
        await self.load()
