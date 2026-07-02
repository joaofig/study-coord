from typing import List

from db.repository.StudyResearcherRepository import StudyResearcherRepository
from models.researcher import StudyResearcher, StudyResearcherList
from viewmodels.ViewModel import ViewModel


class StudyResearcherListViewModel(ViewModel):
    researchers: List[StudyResearcher] = []
    study_id: int = 0
    selected_id: int = 0

    def __init__(self):
        super().__init__()
        self.subscribe(channel="study_researcher_list",
                       message="load",
                       handler=self._on_load)
        self.subscribe(channel="study",
                       message="study_selected",
                       handler=self._on_study_selected)

    async def _load_study_researchers(self, study_id: int):
        researchers = StudyResearcherList()
        self.researchers = [sr.to_dict() for sr in await researchers.load_from_study(study_id)]

    async def _delete_researcher(self, researcher_id: int):
        repo = StudyResearcherRepository()
        await repo.delete(researcher_id)
        await self.load()
        await self.broadcast("study_researcher", "deleted")

    async def _on_study_selected(self, **kwargs):
        study_id = kwargs.get("study_id")
        if study_id:
            self.study_id = int(study_id)
            await self._load_study_researchers(self.study_id)

    async def load(self):
        repo = StudyResearcherRepository()
        self.researchers = [StudyResearcher(**s) for s in await repo.list(self.study_id)]

    async def _on_message(self, msg: str, **kwargs):
        match msg:
            case "load":
                await self.load()

            case "study_researcher_saved":
                await self.load()

            case "researcher_selected":
                if "researcher_id" in kwargs:
                    self.selected_id = kwargs["researcher_id"]

            case "researcher_unselected":
                self.selected_id = 0

            case "delete_researcher":
                if "researcher_id" in kwargs:
                    researcher_id = kwargs["researcher_id"]
                    await self._delete_researcher(researcher_id)

    async def _on_load(self, **kwargs):
        await self.load()
