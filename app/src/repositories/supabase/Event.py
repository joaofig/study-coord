from aiohttp.web_routedef import delete
from supabase import AsyncClient

from src.repositories.supabase.client import get_supabase_client
from src.repositories.EventRepository import EventRepository


class EventRepoSupabase(EventRepository):
    def __init__(self):
        self.supabase: AsyncClient | None = None

    async def connect(self):
        if not self.supabase:
            self.supabase = await get_supabase_client()

    async def get(self, patient_id: int) -> dict | None:
        await self.connect()
        if self.supabase:
            result = (await self.supabase.table("event").select("*").eq("id", patient_id).execute()).data
            if result:
                return result[0]
        return None


    async def get_by_study_and_patient(self, study_id: int, patient_id: int) -> list[dict]:
        await self.connect()
        if self.supabase:
            result = (await self.supabase.table("event").select("*")
                      .eq("study_id", study_id)
                      .eq("patient_id", patient_id).execute()).data
            if result:
                return result
        return []

    async def save(self, event: dict) -> dict:
        await self.connect()
        if self.supabase:
            if event.get("id", 0) > 0:
                await self.supabase.table("event").update(event).eq("id", event["id"]).execute()
                return event
            else:
                event.pop("id", None)
                result = (await self.supabase.table("event").insert(event).execute()).data
                if result:
                    return result[0]
        return {}

    async def delete(self, event_id: int) -> None:
        await self.connect()
        if self.supabase:
            await self.supabase.table("event").delete().eq("id", event_id).execute()

    async def delete_by_study_id(self, study_id: int) -> None:
        await self.connect()
        if self.supabase:
            await self.supabase.table("event").delete().eq("study_id", study_id).execute()
