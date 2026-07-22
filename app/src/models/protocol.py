from typing import List

from src.dtos.protocol import ProtocolDTO
from src.repositories import ProtocolRepository


class ProtocolModel:
    repo = ProtocolRepository()

    async def save(self, dto: ProtocolDTO):
        result = await self.repo.save(dto)
        dto.id = result["id"]

    async def load(self, protocol_id: int) -> ProtocolDTO | None:
        return await self.repo.load(protocol_id)

    async def delete(self, protocol_id: int):
        await self.repo.delete(protocol_id=protocol_id)

    async def list(self, study_id: int) -> List[ProtocolDTO]:
        return await self.repo.list(study_id)
