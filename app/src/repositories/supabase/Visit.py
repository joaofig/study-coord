from typing import List

from supabase import AsyncClient

from src.repositories.supabase.client import get_supabase_client
from src.repositories.VisitRepository import VisitRepository


class VisitRepoSupabase(VisitRepository):
    def __init__(self):
        self.supabase: AsyncClient | None = None

    async def connect(self):
        if not self.supabase:
            self.supabase = await get_supabase_client()

    async def get_by_study_id(self, study_id: int) -> List[dict]:
        await self.connect()
        if self.supabase:
            return (await self.supabase.table("study").select("*").eq("study_id", study_id).execute()).data
        return []

    async def get_by_study_id_and_patient_id(self, study_id: int, patient_id: int) -> List[dict]:
        await self.connect()
        if self.supabase:
            return (await self.supabase.table("study").select("*")
                    .eq("study_id", study_id)
                    .eq("patient_id", patient_id).execute()).data
        return []

    async def save(self, visit: dict) -> dict:
        await self.connect()
        if self.supabase:
            if visit.get("id", 0) > 0:
                await self.supabase.table("study").update(visit).eq("id", visit["id"]).execute()
                return visit
            else:
                visit.pop("id", None)  # Remove id if present to avoid conflicts
                return (await self.supabase.table("study").insert(visit).execute()).data[0]
        return {}

    async def delete(self, visit_id: int):
        await self.connect()
        if self.supabase:
            await self.supabase.table("study").delete().eq("id", visit_id).execute()

    async def delete_by_study_id_and_patient_id(self, study_id: int, patient_id: int):
        await self.connect()
        if self.supabase:
            await (self.supabase.table("study").delete()
                   .eq("study_id", study_id)
                   .eq("patient_id", patient_id).execute())
