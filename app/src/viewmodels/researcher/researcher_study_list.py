from typing import Any

from nicemvvm.tools.observability import GridList
from nicemvvm.viewmodels.view_model import ViewModel
from src.models.researcher_study import ResearcherStudyModel


class ResearcherStudyListViewModel(ViewModel):
    studies = GridList()
    researcher_id: int = 0
    model: ResearcherStudyModel = ResearcherStudyModel()

    def __init__(self):
        super().__init__()
        self.subscribe(channel="researcher", message="selected", handler=self._on_researcher_selected)

    async def _on_researcher_selected(self, **kwargs):
        researcher_id = kwargs.get("researcher_id", 0)
        await self._load_researcher_studies(researcher_id)

    async def _load_researcher_studies(self, researcher_id: int):
        self.researcher_id = researcher_id
        studies = await self.model.list(researcher_id)
        self.studies.replace([r.to_dict() for r in studies])

    async def _on_call(self, msg: str, **kwargs) -> Any:
        pass
