from typing import List

from repositories.supabase.base import SupabaseRepository

TABLE = "study_researcher"

class StudyResearcherRepository(SupabaseRepository):
    def __init__(self):
        super().__init__()

    async def get(self, researcher_id: int) -> dict | None:
        await self.connect()
        if self.supabase:
            result = (await self.supabase.table(TABLE)
                      .select("*")
                      .eq("id", researcher_id).execute()).data
            if result:
                return result[0]
        return None

    async def list(self, study_id: int) -> List[dict]:
        await self.connect()
        if self.supabase:
            result = (await self.supabase.table(TABLE)
                      .select("*")
                      .eq("study_id", study_id).execute()).data
            if result:
                return result
        return []

    async def delete(self, researcher_id: int) -> None:
        await self.connect()
        if self.supabase:
            await self.supabase.table(TABLE).delete().eq("id", researcher_id).execute()
        return None

    async def save(self, sr: dict) -> None:
        await self.insert_or_update(TABLE, sr)

    async def delete_by_study(self, study_id: int) -> None:
        await self.connect()
        if self.supabase:
            await self.supabase.table(TABLE).delete().eq("study_id", study_id).execute()
        return None