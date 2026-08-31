from typing import Any

from src.models.study import StudyModel
from nicemvvm.tools.observability import GridList
from nicemvvm.viewmodels.view_model import ViewModel


class StudyListViewModel(ViewModel):
    selected_id: int = 0

    def __init__(self):
        super().__init__()
        self.studies = GridList()
        self.model: StudyModel = StudyModel()

        self.subscribe(channel="study", messages=["saved"], handler=self._load)
        self.subscribe(
            channel="patient", messages=["saved", "deleted"], handler=self._load
        )
        self.subscribe(
            channel="researcher", messages=["saved", "deleted"], handler=self._load
        )
        self.subscribe(
            channel="adverse_event", messages=["saved", "deleted"], handler=self._load
        )
        self.subscribe(
            channel="visit", messages=["saved", "deleted"], handler=self._load
        )
        self.subscribe(
            channel="protocol", messages=["saved", "deleted"], handler=self._load
        )
        self.subscribe(
            channel="monitorization", messages=["saved", "deleted"], handler=self._load
        )

    async def _load(self, **kwargs):
        studies = await self.model.list()
        self.studies.replace([s.to_dict() for s in studies])

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "load":
                await self._load()

            case "delete":
                study_id = kwargs["study_id"]
                await self.model.delete(study_id)
                await self._load()
                await self.broadcast(
                    channel="study",
                    message="deleted",
                    study_id=study_id
                )

            case "select":
                self.selected_id = kwargs.get("study_id", 0)
                if self.selected_id:
                    await self.broadcast(
                        channel="study",
                        message="selected",
                        study_id=self.selected_id
                    )
        return None
