from typing import List

from nicegui.helpers import await_with_context

from repositories.supabase.base import SupabaseRepository


TABLE = "patient"


class PatientRepository(SupabaseRepository):
    def __init__(self):
        super().__init__()

    async def get(self, patient_id: int) -> dict | None:
        await self.connect()
        if self.supabase:
            result = (await self.supabase.table(TABLE).select("*").eq("id", patient_id).execute()).data
            if result:
                return result[0]
        return None

    async def load_from_study(self, study_id: int) -> List[dict]:
        await self.connect()
        if self.supabase:
            result = (await self.supabase.table(TABLE).select("*").eq("study_id", study_id).execute()).data
            if result:
                print(result)
                return result
        return []

    async def save(self, patient: dict) -> dict:
        return await self.insert_or_update(TABLE, patient)

    async def delete(self, patient_id: int) -> None:
        await self.connect()
        if self.supabase:
            await self.supabase.table(TABLE).delete().eq("id", patient_id).execute()
        return None

    async def delete_by_study_id(self, study_id: int) -> None:
        await self.connect()
        if self.supabase:
            await self.supabase.table(TABLE).delete().eq("study_id", study_id).execute()
        return None
