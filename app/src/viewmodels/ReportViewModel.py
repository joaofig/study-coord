from typing import Any

from nicegui.observables import ObservableDict

from src.db.repository.ReportRepository import ReportRepository
from src.viewmodels.ViewModel import ViewModel


class ReportViewModel(ViewModel):
    study_count: int = 0
    patient_count: int = 0
    researcher_count: int = 0
    visit_count: int = 0
    event_count: int = 0

    study_id: int = 0
    study_patient_count: int = 0
    study_researcher_count: int = 0
    study_visit_count: int = 0
    study_event_count: int = 0

    studies = ObservableDict()

    def __init__(self):
        super().__init__()
        self.subscribe("reports", "load", self._on_load)
        self.subscribe("study_list", "load", self._on_reload_studies)

    async def load(self):
        repo = ReportRepository()
        self.study_count = await repo.get_study_count()
        self.patient_count = await repo.get_patient_count()
        self.researcher_count = await repo.get_researcher_count()
        self.visit_count = await repo.get_visit_count()
        self.event_count = await repo.get_event_count()

        self.studies.clear()
        studies = await repo.get_studies()
        for row in studies:
            self.studies[row["id"]] = row["name"]

    async def _on_load(self, **kwargs):
        await self.load()

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "load":
                await self.load()

            case "load_detail":
                await self._load_detail()
        return None

    async def _load_detail(self):
        repo = ReportRepository()

        self.study_patient_count = await repo.get_patient_count_by_study(self.study_id)
        self.study_researcher_count = await repo.get_researcher_count_by_study(self.study_id)
        self.study_visit_count = await repo.get_visit_count_by_study(self.study_id)
        self.study_event_count = await repo.get_event_count_by_study(self.study_id)

    async def _on_reload_studies(self, **kwargs):
        repo = ReportRepository()
        self.studies.clear()
        studies = await repo.get_studies()
        for row in studies:
            self.studies[row["id"]] = row["name"]
