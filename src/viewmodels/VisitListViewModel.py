from models.visit import VisitList
from viewmodels.ViewModel import ViewModel


class VisitListViewModel(ViewModel):
    def __init__(self):
        super().__init__()
        self.visits: list[dict] = []
        self.study_id: int = 0
        self.visit_id: int = 0
        self.subscribe(channel="study",
                       message="study_selected",
                       handler=self._handle_study_selected)

    async def _load_visits(self, study_id: int):
        visits = VisitList()
        self.visits = [v.to_dict() for v in await visits.load_from_study(study_id)]
        await self.notify("visits_loaded")

    async def _handle_study_selected(self, **kwargs):
        study_id = kwargs.get("study_id")
        if study_id:
            self.study_id = int(study_id)
            await self._load_visits(self.study_id)

    async def _on_message(self, msg: str, **kwargs):
        match msg:
            case "study_selected":
                await self._handle_study_selected(**kwargs)
