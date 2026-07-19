from typing import List

from src.dtos.adverse_event import AdverseEventDTO
from src.repositories import AdverseEventRepository


class AdverseEventModel:
    repo = AdverseEventRepository()

    async def save(self, dto: AdverseEventDTO):
        event_dict = await self.repo.save(dto.to_dict())
        dto.id = event_dict["id"]

    async def load(self, event_id: int) -> AdverseEventDTO | None:
        event_dict = await self.repo.get(event_id)
        if event_dict:
            return AdverseEventDTO(**event_dict)
        return None

    async def list(self, study_id: int, patient_id: int) -> List[AdverseEventDTO]:
        event_dicts = await self.repo.get_by_study_and_patient(study_id, patient_id)
        return [AdverseEventDTO(**e) for e in event_dicts]

    async def delete(self, event_id: int):
        await self.repo.delete(event_id)
