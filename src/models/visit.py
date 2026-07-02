from dataclasses import dataclass

from src.models import Patient


@dataclass
class Visit:
    id: int
    patient_id: int
    date: str
    type: str = "visit"
    comments: str = ""

    patient: Patient | None = None


@dataclass
class VisitList:
    visits: list[Visit] = None

    async def load_from_patient(self, patient_id: int) -> list[Visit]:
        from db.repository.VisitRepository import VisitRepository

        repo = VisitRepository()
        visit_dicts = await repo.get_by_patient(patient_id)
        self.visits = [Visit(**v) for v in visit_dicts]
        return self.visits