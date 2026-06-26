from db.repository import StudyRepository
from models.study import StudyRow
from viewmodels.ViewModel import ViewModel


class StudyListViewModel(ViewModel):
    studies: list[StudyRow] = []

    def __init__(self):
        super().__init__()

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
