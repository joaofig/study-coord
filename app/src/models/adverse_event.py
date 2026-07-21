from typing import List

from src.dtos.adverse_event import AdverseEventDTO
from src.repositories import AdverseEventRepository


class AdverseEventModel:
    repo = AdverseEventRepository()

    async def save(self, dto: AdverseEventDTO):
        event_dict = await self.repo.save(dto)
        dto.adverse_event_id = event_dict["id"]

    async def load(self, event_id: int) -> AdverseEventDTO | None:
        return await self.repo.load(event_id)

    async def list(self, study_id: int, patient_id: int) -> List[AdverseEventDTO]:
        return await self.repo.list(study_id=study_id, patient_id=patient_id)

    async def delete(self, adverse_event_id: int):
        await self.repo.delete(adverse_event_id=adverse_event_id)
