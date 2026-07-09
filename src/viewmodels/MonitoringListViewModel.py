from nicegui.observables import ObservableList

from models.monitoring import MonitoringList
from viewmodels.ViewModel import ViewModel


class MonitoringListViewModel(ViewModel):
    monitoring_visits = ObservableList()
    study_id: int = 0
    monitoring_id: int = 0

    def __init__(self):
        super().__init__()
        self.subscribe(channel="study",
                       message="selected",
                       handler=self._handle_study_selected)

    async def _load_monitoring(self, study_id: int):
        monitoring_list = MonitoringList()
        self.monitoring_visits.clear()
        self.monitoring_visits.extend([m.to_dict() for m in await monitoring_list.load_from_study(study_id)])

    async def _handle_study_selected(self, **kwargs):
        study_id = kwargs.get("study_id")
        if study_id:
            self.study_id = int(study_id)
            await self._load_monitoring(self.study_id)

    async def _on_call(self, msg: str, **kwargs):
        match msg:
            case "load":
                study_id = kwargs.get("study_id")
                if study_id is not None:
                    self.study_id = int(study_id)
                await self._load_monitoring(self.study_id)

            case "monitoring_selected":
                monitoring_id = kwargs.get("monitoring_id")
                if monitoring_id:
                    self.monitoring_id = int(monitoring_id)

            case "delete_monitoring":
                monitoring_id = kwargs.get("monitoring_id")
                if monitoring_id:
                    self.monitoring_id = int(monitoring_id)
                    await MonitoringList.delete(self.monitoring_id)
                    await self._load_monitoring(self.study_id)

        return None
