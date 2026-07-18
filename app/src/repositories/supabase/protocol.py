from typing import List

from repositories.supabase.base import SupabaseRepository


TABLE = "protocol"


class ProtocolRepository(SupabaseRepository):
    def __init__(self):
        super().__init__()

    async def get(self, protocol_id: int) -> dict | None:
        await self.connect()
        if self.supabase:
            result = (await self.supabase.table(TABLE).select("*").eq("id", protocol_id).execute()).data
            if result:
                return result[0]
        return None

    async def get_by_study_id(self, study_id: int) -> List[dict]:
        await self.connect()
        if self.supabase:
            result = (await self.supabase.table(TABLE).select("*").eq("study_id", study_id).execute()).data
            if result:
                return result
        return []

    async def save(self, protocol: dict) -> dict:
        return await self.insert_or_update(TABLE, protocol)

    async def delete(self, protocol_id: int) -> None:
        await self.connect()
        if self.supabase:
            await self.supabase.table(TABLE).delete().eq("id", protocol_id).execute()

    async def delete_by_study_id(self, study_id: int) -> None:
        await self.connect()
        if self.supabase:
            await self.supabase.table(TABLE).delete().eq("study_id", study_id).execute()
