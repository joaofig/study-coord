from typing import List

from repositories.supabase.base import SupabaseRepository


TABLE = "visit"


class VisitRepository(SupabaseRepository):
    def __init__(self):
        super().__init__()

    async def get_by_study_id(self, study_id: int) -> List[dict]:
        await self.connect()
        if self.supabase:
            return (await self.supabase.table(TABLE).select("*").eq("study_id", study_id).execute()).data
        return []

    async def get_by_study_id_and_patient_id(self, study_id: int, patient_id: int) -> List[dict]:
        await self.connect()
        if self.supabase:
            return (await self.supabase.table(TABLE).select("*")
                    .eq("study_id", study_id)
                    .eq("patient_id", patient_id).execute()).data
        return []

    async def save(self, visit: dict) -> dict:
        return await self.insert_or_update(TABLE, visit)

    async def delete(self, visit_id: int):
        await self.connect()
        if self.supabase:
            await self.supabase.table(TABLE).delete().eq("id", visit_id).execute()

    async def delete_by_study_id_and_patient_id(self, study_id: int, patient_id: int):
        await self.connect()
        if self.supabase:
            await (self.supabase.table(TABLE).delete()
                   .eq("study_id", study_id)
                   .eq("patient_id", patient_id).execute())
