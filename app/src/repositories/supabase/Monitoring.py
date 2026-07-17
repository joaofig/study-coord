from supabase import AsyncClient

from src.repositories.supabase.client import get_supabase_client
from src.repositories.MonitoringRepository import MonitoringRepository


class MonitoringRepoSupabase(MonitoringRepository):
    def __init__(self):
        self.supabase: AsyncClient | None = None

    async def connect(self):
        if not self.supabase:
            self.supabase = await get_supabase_client()

    async def get(self, monitoring_id: int) -> dict | None:
        await self.connect()
        if self.supabase:
            result = (await self.supabase.table("monitoring").select("*").eq("id", monitoring_id).execute()).data
            if result:
                return result[0]
        return None

    async def get_by_study_id(self, study_id: int) -> list[dict]:
        await self.connect()
        if self.supabase:
            result = (await self.supabase.table("monitoring").select("*").eq("study_id", study_id).execute()).data
            if result:
                return result
        return []

    async def save(self, monitoring: dict) -> dict:
        await self.connect()
        if self.supabase:
            if monitoring.get("id", 0) > 0:
                await self.supabase.table("monitoring").update(monitoring).eq("id", monitoring["id"]).execute()
                return monitoring
            result = (await self.supabase.table("monitoring").insert(monitoring).execute()).data
            if result:
                return result[0]
        return {}

    async def delete(self, monitoring_id: int) -> None:
        await self.connect()
        if self.supabase:
            await self.supabase.table("monitoring").delete().eq("id", monitoring_id).execute()
        return None

    async def delete_by_study_id(self, study_id: int) -> None:
        await self.connect()
        if self.supabase:
            await self.supabase.table("monitoring").delete().eq("study_id", study_id).execute()
        return None
