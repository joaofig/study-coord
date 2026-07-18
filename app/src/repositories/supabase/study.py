from typing import List

from repositories.supabase.base import SupabaseRepository


TABLE = "study"


class StudyRepository(SupabaseRepository):
    def __init__(self):
        super().__init__()

    async def list(self) -> List[dict]:
        await self.connect()
        if self.supabase:
            return (await self.supabase.table(TABLE).select("*").execute()).data
        return []

    async def get(self, study_id: int) -> dict | None:
        await self.connect()
        if self.supabase:
            result = (await self.supabase.table(TABLE).select("*").eq("id", study_id).execute()).data
            if result:
                return result[0]
        return None

    async def save(self, study: dict) -> dict:
        return await self.insert_or_update(TABLE, study)

    async def delete(self, study_id: int) -> None:
        await self.connect()
        if self.supabase:
            await self.supabase.table(TABLE).delete().eq("id", study_id).execute()
        return None
