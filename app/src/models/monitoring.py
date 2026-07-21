from typing import List

from src.dtos.monitoring import MonitoringDTO
from src.repositories import MonitoringRepository


class MonitoringModel:
    repo = MonitoringRepository()

    async def save(self, dto: MonitoringDTO):
        monitoring = await self.repo.save(dto)
        dto.monitoring_id = monitoring["monitoring_id"]

    async def load(self, monitoring_id: int) -> MonitoringDTO | None:
        monitoring = await self.repo.load(monitoring_id)
        if monitoring:
            return monitoring
        return None

    async def delete(self, monitoring_id: int):
        await self.repo.delete(monitoring_id=monitoring_id)

    async def list(self, study_id: int) -> List[MonitoringDTO]:
        ms = await self.repo.list(study_id)
        return ms
