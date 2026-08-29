from typing import Any

from src.models.timeline import TimelineModel
from nicemvvm.tools.observability import GridList
from src.viewmodels import ViewModel


class TimelineViewModel(ViewModel):
    study_id: int = 0

    def __init__(self):
        super().__init__()
        self.milestones = GridList()
        self.model = TimelineModel()
        self.subscribe(channel="timeline", message="load", handler=self._on_load)
        self.subscribe(
            channel="study", message="selected", handler=self._on_study_selected
        )

    async def _on_load(self, study_id):
        milestones = await self.model.load(study_id)
        self.milestones.replace(milestones)

    async def _on_study_selected(self, **kwargs):
        self.study_id = kwargs.get("study_id", 0)
        if self.study_id:
            await self._on_load(self.study_id)
        else:
            self.milestones.clear()

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "load":
                study_id = kwargs.get("study_id", 0)
                if study_id != 0:
                    self.study_id = study_id
                    await self._on_load(self.study_id)
