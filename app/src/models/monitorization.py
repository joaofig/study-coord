import builtins

from src.dtos.monitorization import MonitorizationDTO
from src.repositories import MonitorizationRepository


class MonitorizationModel:
    repo = MonitorizationRepository()

    async def save(self, dto: MonitorizationDTO):
        monitorization = await self.repo.save(dto)
        dto.monitoring_id = monitorization["monitoring_id"]
        return dto

    async def load(self, monitoring_id: int) -> MonitorizationDTO | None:
        monitorization = await self.repo.load(monitoring_id)
        if monitorization:
            return monitorization
        return None

    async def delete(self, monitoring_id: int):
        await self.repo.delete(monitoring_id=monitoring_id)

    async def list(self, study_id: int) -> builtins.list[MonitorizationDTO]:
        ms = await self.repo.list(study_id)
        return ms
