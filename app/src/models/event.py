from dataclasses import dataclass
from typing import List

from dtos.event import EventDTO
from src.repositories import EventRepository


@dataclass
class EventModel:
    repo = EventRepository()

    async def save(self, dto: EventDTO):
        event_dict = await self.repo.save(dto.to_dict())
        dto.id = event_dict["id"]

    async def load(self, event_id: int) -> EventDTO | None:
        event_dict = await self.repo.get(event_id)
        if event_dict:
            return EventDTO(**event_dict)
        return None

    async def list(self, study_id: int) -> List[EventDTO]:
        event_dicts = await self.repo.get_by_study(study_id)
        return [EventDTO(**e) for e in event_dicts]

    async def delete(self, event_id: int):
        await self.repo.delete(event_id)
