from dataclasses import dataclass

from src.models import Patient


@dataclass
class Visit:
    id: int
    patient_id: int
    patient_number: str
    patient_name: str
    date: str
    type: str = "visit"
    comments: str = ""

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "patient_number": self.patient_number,
            "patient_name": self.patient_name,
            "date": self.date,
            "type": self.type,
            "comments": self.comments,
        }

@dataclass
class VisitList:
    visits: list[Visit] = None

    async def load_from_study(self, study_id: int) -> list[Visit]:
        from db.repository.VisitRepository import VisitRepository

        repo = VisitRepository()
        visit_dicts = await repo.get_by_study_id(study_id)
        self.visits = [Visit(**v) for v in visit_dicts]
        return self.visits
