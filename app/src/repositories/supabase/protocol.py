from typing import List

from src.dtos.protocol import ProtocolDTO
from src.repositories.supabase.base import SupabaseRepository


TABLE = "protocol"


class ProtocolRepository(SupabaseRepository):
    def __init__(self):
        super().__init__()

    async def load(self, protocol_id: int) -> ProtocolDTO | None:
        await self.connect()
        if self.supabase:
            result = (await self.supabase.table(TABLE).select("*").eq("protocol_id", protocol_id).execute()).data
            if result:
                return ProtocolDTO.from_dict(result[0])
        return None

    async def list(self, study_id: int) -> List[ProtocolDTO]:
        await self.connect()
        if self.supabase:
            result = (await self.supabase.table(TABLE).select("*").eq("study_id", study_id).execute()).data
            if result:
                return [ProtocolDTO.from_dict(p) for p in result]
        return []

    async def save(self, protocol: ProtocolDTO) -> dict:
        return await self.insert_or_update(TABLE, protocol.to_dict())

    async def delete(self, *, study_id = 0, protocol_id: int = 0) -> None:
        await self.connect()
        if self.supabase:
            if study_id:
                await self.supabase.table(TABLE).delete().eq("study_id", study_id).execute()
            else:
                await self.supabase.table(TABLE).delete().eq("protocol_id", protocol_id).execute()
