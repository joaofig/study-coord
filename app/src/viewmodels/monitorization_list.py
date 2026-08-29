from typing import Any

from src.models.monitorization import MonitorizationModel
from nicemvvm.tools.observability import GridList
from nicemvvm.viewmodels.view_model import ViewModel


class MonitoringListViewModel(ViewModel):
    monitorization_visits = GridList()
    selected_id: int = 0
    model = MonitorizationModel()

    def __init__(self):
        super().__init__()
        self.subscribe(
            channel="study", message="selected", handler=self._study_selected
        )

    async def _load_monitorizations(self, study_id: int):
        visits = [m.to_dict() for m in await self.model.list(study_id)]
        self.monitorization_visits.replace(visits)

    async def _study_selected(self, **kwargs):
        study_id = kwargs.get("study_id", 0)
        if study_id:
            await self._load_monitorizations(study_id)

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "load":
                study_id = kwargs.get("study_id", 0)
                if study_id is not None:
                    await self._load_monitorizations(study_id)

            case "select":
                monitoring_id = kwargs.get("monitoring_id", 0)
                if monitoring_id:
                    self.selected_id = monitoring_id

            case "delete":
                monitoring_id = kwargs.get("monitoring_id", 0)
                if monitoring_id:
                    await self.model.delete(monitoring_id)
                    self.monitorization_visits.delete("monitoring_id", monitoring_id)
                    await self.broadcast(
                        channel="monitorization",
                        message="deleted",
                        monitoring_id=monitoring_id,
                    )
        return None
