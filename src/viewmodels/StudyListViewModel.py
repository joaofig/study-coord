from db.repository import StudyRepository
from models.study import StudyRow
from tools.messenger import get_messenger
from viewmodels.ViewModel import ViewModel


class StudyListViewModel(ViewModel):
    studies: list[StudyRow] = []

    def __init__(self):
        super().__init__()
        self.messenger = get_messenger("study_list")
        self.messenger.subscribe("load", self._on_load)

    async def load(self):
        repo = StudyRepository()
        self.studies = [StudyRow(**s) for s in await repo.list()]
        await self.notify("list_changed")

    async def handle_command(self, msg: str, **kwargs):
        match msg:
            case "load":
                await self.load()

            case "study_saved":
                await self.load()

    async def _on_load(self, **kwargs):
        await self.load()
