from typing import List, Any

from src.dtos.researcher import StudyResearcherDTO
from src.models import StudyResearcherModel
from src.viewmodels.view_model import ViewModel


class StudyResearcherListViewModel(ViewModel):
    researchers: List[StudyResearcherDTO] = []
    study_id: int = 0
    selected_id: int = 0
    model: StudyResearcherModel = StudyResearcherModel()

    def __init__(self):
        super().__init__()
        self.subscribe(
            channel="study_researcher_list", message="load", handler=self._on_load
        )
        self.subscribe(
            channel="study", message="selected", handler=self._on_study_selected
        )

    async def _load_study_researchers(self, study_id: int):
        self.researchers = await self.model.list(study_id)

    async def _delete_researcher(self, researcher_id: int):
        await self.model.delete(researcher_id)
        await self.load()
        await self.broadcast(channel="study_researcher", message="deleted")

    async def _on_study_selected(self, **kwargs):
        study_id = kwargs.get("study_id", 0)
        if study_id:
            self.study_id = int(study_id)
            await self._load_study_researchers(self.study_id)
        else:
            self.study_id = 0
            self.selected_id = 0
            self.researchers.clear()

    async def load(self):
        self.researchers = await self.model.list(self.study_id)

    async def _on_call(self, msg: str, **kwargs) -> Any:
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
        return None

    async def _on_load(self, **kwargs):
        await self.load()
