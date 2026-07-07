from dataclasses import dataclass
from typing import List

from db.repository.EventRepository import EventRepository


@dataclass
class Event:
    id: int = 0
    study_id: int = 0
    patient_id: int = 0
    date: str = ""
    event_type: str = ""
    description: str = ""
    comments: str = ""
    patient_number: str = ""
    patient_name: str = ""

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "study_id": self.study_id,
            "patient_id": self.patient_id,
            "date": self.date,
            "event_type": self.event_type,
            "description": self.description,
            "comments": self.comments,
            "patient_number": self.patient_number,
            "patient_name": self.patient_name,
        }

    async def save(self):
        repo = EventRepository()
        event_dict = await repo.save(self.to_dict())
        self.id = event_dict["id"]

    @classmethod
    async def load(cls, event_id: int) -> "Event | None":
        repo = EventRepository()
        event_dict = await repo.get(event_id)
        if event_dict:
            return Event(**event_dict)
        return None


class EventList:
    events: list[Event] = []

    async def load_from_study_and_patient(self, study_id: int, patient_id: int) -> List[Event]:
        repo = EventRepository()
        event_dicts = await repo.get_by_study_and_patient(study_id, patient_id)
        self.events = [Event(**e) for e in event_dicts]
        return self.events

    @classmethod
    async def delete(cls, event_id: int):
        repo = EventRepository()
        await repo.delete(event_id)
