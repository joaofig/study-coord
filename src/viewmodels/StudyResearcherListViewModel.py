from typing import List

from db.repository.StudyResearcherRepository import StudyResearcherRepository
from models.researcher import StudyResearcher, StudyResearcherList
from tools.messenger import get_messenger
from viewmodels.ViewModel import ViewModel


class StudyResearcherListViewModel(ViewModel):
    researchers: List[StudyResearcher] = []
    study_id: int = 0

    def __init__(self):
        super().__init__()
        self.study_messenger = get_messenger("study")
        self.messenger = get_messenger("study_research_list")
        self.messenger.subscribe("load", self._on_load)
        self.study_messenger.subscribe("study_selected", self._on_study_selected)

    async def _load_study_researchers(self, study_id: int):
        researchers = StudyResearcherList()
        self.researchers = [sr.to_dict() for sr in await researchers.load_from_study(study_id)]
        await self.notify("study_researchers_loaded")

    async def _on_study_selected(self, **kwargs):
        study_id = kwargs.get("study_id")
        if study_id:
            self.study_id = int(study_id)
            await self._load_study_researchers(self.study_id)

    async def load(self):
        repo = StudyResearcherRepository()
        self.researchers = [StudyResearcher(**s) for s in await repo.list(self.study_id)]
        await self.notify("list_changed")

    async def handle_command(self, msg: str, **kwargs):
        match msg:
            case "load":
                await self.load()

            case "study_researcher_saved":
                await self.load()

    async def _on_load(self, **kwargs):
        await self.load()
