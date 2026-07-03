from dataclasses import dataclass

from db.repository.VisitRepository import VisitRepository


@dataclass
class Visit:
    id: int                         # Read-only unique identifier for the visit
    study_id: int                   # Identifier for the study associated with the visit
    patient_id: int                 # Identifier for the patient associated with the visit
    visit_date: str                 # Date of the visit
    visit_type: str = "visit"       # Type of the visit
    comments: str = ""              # Additional comments about the visit

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "study_id": self.study_id,
            "patient_id": self.patient_id,
            "visit_date": self.visit_date,
            "visit_type": self.visit_type,
            "comments": self.comments,
        }

    async def save(self):
        repo = VisitRepository()
        return await repo.save(self.to_dict())


async def load_visit(visit_id: int) -> Visit | None:
    repo = VisitRepository()
    visit_dict = await repo.get(visit_id)
    if visit_dict:
        return Visit(**visit_dict)
    else:
        return None


@dataclass
class VisitList:
    visits: list[Visit] = None

    async def load_from_study(self, study_id: int) -> list[Visit]:
        from db.repository.VisitRepository import VisitRepository

        repo = VisitRepository()
        visit_dicts = await repo.get_by_study_id(study_id)
        self.visits = [Visit(**v) for v in visit_dicts]
        return self.visits
