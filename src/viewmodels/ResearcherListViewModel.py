from nicegui.observables import ObservableList

from db.repository.ResearcherRepository import ResearcherRepository
from models import Researcher
from viewmodels.ViewModel import ViewModel


class ResearcherListViewModel(ViewModel):
    researchers = ObservableList()

    def __init__(self):
        super().__init__()
        self.subscribe(channel="researcher_list",
                       message="load",
                       handler=self._on_load)

    async def load(self):
        repo = ResearcherRepository()
        self.researchers.clear()
        self.researchers.extend([Researcher(**s) for s in await repo.list()])

    async def _on_message(self, msg: str, **kwargs):
        match msg:
            case "load":
                await self.load()

            case "study_saved":
                await self.load()

    async def _on_load(self, **kwargs):
        await self.load()
