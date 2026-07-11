from db.repository.ReportRepository import ReportRepository
from viewmodels.ViewModel import ViewModel


class ReportViewModel(ViewModel):
    study_count: int = 0
    patient_count: int = 0
    researcher_count: int = 0

    def __init__(self):
        super().__init__()
        self.subscribe("reports", "load", self._on_load)

    async def load(self):
        repo = ReportRepository()
        self.study_count = await repo.get_study_count()
        self.patient_count = await repo.get_patient_count()
        self.researcher_count = await repo.get_researcher_count()

    async def _on_load(self, **kwargs):
        await self.load()

    async def _on_call(self, msg: str, **kwargs):
        match msg:
            case "load":
                await self.load()
