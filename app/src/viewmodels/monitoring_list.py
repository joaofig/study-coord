from typing import Any

from src.models import MonitoringModel
from src.tools.observability import GridList
from src.viewmodels.view_model import ViewModel


class MonitoringListViewModel(ViewModel):
    monitoring_visits = GridList()
    study_id: int = 0
    selected_id: int = 0
    model = MonitoringModel()

    def __init__(self):
        super().__init__()
        self.subscribe(
            channel="study", message="selected", handler=self._handle_study_selected
        )

    async def _load_monitoring(self, study_id: int):
        self.monitoring_visits.replace(
            [m.to_dict() for m in await self.model.list(study_id)]
        )

    async def _handle_study_selected(self, **kwargs):
        study_id = kwargs.get("study_id")
        if study_id:
            self.study_id = int(str(study_id))
            await self._load_monitoring(self.study_id)
        else:
            self.study_id = 0
            self.selected_id = 0
            self.monitoring_visits.clear()

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "load":
                study_id = kwargs.get("study_id")
                if study_id is not None:
                    self.study_id = int(str(study_id))
                    await self._load_monitoring(self.study_id)

            case "monitoring_selected":
                monitoring_id = kwargs.get("selected_id", 0)
                if monitoring_id:
                    self.selected_id = monitoring_id

            case "delete":
                monitoring_id = kwargs.get("selected_id", 0)
                if monitoring_id:
                    self.selected_id = monitoring_id
                    await self.model.delete(self.selected_id)
                    self.monitoring_visits.delete("monitoring_id", monitoring_id)

        return None
