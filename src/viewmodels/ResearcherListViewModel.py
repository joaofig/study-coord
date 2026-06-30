from db.repository.ResearcherRepository import ResearcherRepository
from models import Researcher
from viewmodels.ViewModel import ViewModel


class ResearcherListViewModel(ViewModel):
    researchers: list[Researcher] = []

    def __init__(self):
        super().__init__()
        self.subscribe("researcher", "researcher_saved", self._on_message)
        self.subscribe("researcher_list", "load", self._on_load)

    async def load(self):
        repo = ResearcherRepository()
        self.researchers = [Researcher(**s) for s in await repo.list()]
        await self.notify("list_changed")

    async def _on_message(self, msg: str, **kwargs):
        match msg:
            case "load":
                await self.load()

            case "study_saved":
                await self.load()

    async def _on_load(self, **kwargs):
        await self.load()
