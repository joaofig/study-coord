from typing import List

from dtos.monitoring import MonitoringDTO
from src.repositories import MonitoringRepository


class MonitoringModel:
    repo = MonitoringRepository()

    async def save(self, dto: MonitoringDTO):
        monitoring = await self.repo.save(dto.to_dict())
        dto.id = monitoring["id"]

    async def load(self, monitoring_id: int) -> MonitoringDTO | None:
        monitoring = await self.repo.get(monitoring_id)
        if monitoring:
            return MonitoringDTO(**monitoring)
        return None

    async def delete(self, monitoring_id: int):
        await self.repo.delete(monitoring_id)

    async def list(self, study_id: int) -> List[MonitoringDTO]:
        ms = await self.repo.get_by_study_id(study_id)
        return [MonitoringDTO(**m) for m in ms]
