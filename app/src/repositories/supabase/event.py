from repositories.supabase.base import SupabaseRepository


TABLE = "event"


class EventRepository(SupabaseRepository):
    def __init__(self):
        super().__init__()

    async def get(self, patient_id: int) -> dict | None:
        await self.connect()
        if self.supabase:
            result = (await self.supabase.table(TABLE).select("*").eq("id", patient_id).execute()).data
            if result:
                return result[0]
        return None


    async def get_by_study_and_patient(self, study_id: int, patient_id: int) -> list[dict]:
        await self.connect()
        if self.supabase:
            result = (await self.supabase.table(TABLE).select("*")
                      .eq("study_id", study_id)
                      .eq("patient_id", patient_id).execute()).data
            if result:
                return result
        return []

    async def save(self, event: dict) -> dict:
        return await self.insert_or_update(TABLE, event)

    async def delete(self, event_id: int) -> None:
        await self.connect()
        if self.supabase:
            await self.supabase.table(TABLE).delete().eq("id", event_id).execute()

    async def delete_by_study_id(self, study_id: int) -> None:
        await self.connect()
        if self.supabase:
            await self.supabase.table(TABLE).delete().eq("study_id", study_id).execute()
