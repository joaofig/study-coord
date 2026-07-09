from db.repository import StudyRepository
from models.study import StudyRow
from viewmodels.ViewModel import ViewModel


class StudyListViewModel(ViewModel):
    studies: list[StudyRow] = []
    selected_id: int = 0

    def __init__(self):
        super().__init__()
        self.subscribe("study_list", "load", self._on_load)

    async def load(self):
        repo = StudyRepository()
        self.studies = [StudyRow(**s) for s in await repo.list()]
        await self.notify("list_changed")

    async def _on_call(self, msg: str, **kwargs):
        match msg:
            case "load":
                await self.load()

            case "study_saved":
                await self.load()

            case "study_selected":
                self.selected_id = kwargs["study_id"]
                await self.broadcast(channel="study",
                                     message="selected",
                                     study_id=self.selected_id)

    async def _on_load(self, **kwargs):
        await self.load()
