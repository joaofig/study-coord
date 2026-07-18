from supabase import AsyncClient

from repositories.supabase.client import get_supabase_client


class SupabaseRepository:
    def __init__(self):
        self.supabase: AsyncClient | None = None

    async def connect(self):
        if not self.supabase:
            self.supabase = await get_supabase_client()

    async def insert_or_update(self, table: str, event: dict) -> dict:
        await self.connect()
        if self.supabase:
            if event.get("id", 0) > 0:
                await self.supabase.table(table).update(event).eq("id", event["id"]).execute()
                return event
            else:
                event.pop("id", None)
                result = (await self.supabase.table(table).insert(event).execute()).data
                if result:
                    return result[0]
        return {}