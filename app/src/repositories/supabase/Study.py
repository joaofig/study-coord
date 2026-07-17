from typing import List

from supabase import AsyncClient

from src.repositories.supabase.client import get_supabase_client
from src.repositories import StudyRepository


class StudyRepoSupabase(StudyRepository):
    def __init__(self):
        self.supabase: AsyncClient | None = None

    async def connect(self):
        if not self.supabase:
            self.supabase = await get_supabase_client()

    async def list(self) -> List[dict]:
        await self.connect()
        if self.supabase:
            return (await self.supabase.table("study").select("*").execute()).data
        return []

    async def get(self, study_id: int) -> dict | None:
        await self.connect()
        if self.supabase:
            result = (await self.supabase.table("study").select("*").eq("id", study_id).execute()).data
            if result:
                return result[0]
        return None

    async def save(self, study: dict) -> dict:
        await self.connect()
        if self.supabase:
            if study.get("id", 0) > 0:
                await self.supabase.table("study").update(study).eq("id", study["id"]).execute()
                return study
            else:
                return (await self.supabase.table("study").insert(study).execute()).data[0]
        return {}

    async def delete(self, study_id: int) -> None:
        await self.connect()
        if self.supabase:
            await self.supabase.table("study").delete().eq("id", study_id).execute()
        return None
