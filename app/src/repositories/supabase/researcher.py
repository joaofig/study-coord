from typing import List

from repositories.supabase.base import SupabaseRepository

TABLE = "researcher"

class ResearcherRepository(SupabaseRepository):
    def __init__(self):
        super().__init__()

    async def get(self, researcher_id: int) -> dict | None:
        await self.connect()
        if self.supabase:
            result = (await self.supabase.table(TABLE).select("*").eq("id", researcher_id).execute()).data
            if result:
                return result[0]
        return None

    async def save(self, patient: dict) -> dict:
        return await self.insert_or_update(TABLE, patient)

    async def delete(self, researcher_id: int):
        await self.connect()
        if self.supabase:
            await self.supabase.table(TABLE).delete().eq("id", researcher_id).execute()

    async def load(self) -> List[dict]:
        await self.connect()
        if self.supabase:
            result = (await self.supabase.table(TABLE).select("*").execute()).data
            if result:
                return result
        return []