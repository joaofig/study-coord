from typing import List

from src.dtos.protocol import ProtocolDTO
from src.repositories import ProtocolRepository


class ProtocolModel:
    repo = ProtocolRepository()

    async def save(self, dto: ProtocolDTO):
        result = await self.repo.save(dto.to_dict())
        dto.id = result["id"]

    async def load(self, protocol_id: int) -> ProtocolDTO | None:
        protocol = await self.repo.get(protocol_id)
        if protocol:
            return ProtocolDTO(**protocol)
        return None

    async def delete(self, protocol_id: int):
        await self.repo.delete(protocol_id)

    async def list(self, study_id: int) -> List[ProtocolDTO]:
        protocols = await self.repo.get_by_study_id(study_id)
        return [ProtocolDTO(**p) for p in protocols]
