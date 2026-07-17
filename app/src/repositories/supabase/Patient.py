from typing import List

from supabase import AsyncClient

from repositories.PatientRepository import PatientRepository
from repositories.supabase.client import get_supabase_client


class PatientRepoSupabase(PatientRepository):
    def __init__(self):
        self.supabase: AsyncClient | None = None

    async def connect(self):
        if not self.supabase:
            self.supabase = await get_supabase_client()

    async def get(self, patient_id: int) -> dict | None:
        await self.connect()
        if self.supabase:
            result = (await self.supabase.table("patient").select("*").eq("id", patient_id).execute()).data
            if result:
                return result[0]
        return None

    async def get_by_study_id(self, study_id: int) -> List[dict]:
        await self.connect()
        if self.supabase:
            result = (await self.supabase.table("patient").select("*").eq("study_id", study_id).execute()).data
            if result:
                return result
        return []

    async def save(self, patient: dict) -> dict:
        await self.connect()
        if self.supabase:
            if patient.get("id", 0) > 0:
                await self.supabase.table("patient").update(patient).eq("id", patient["id"]).execute()
                return patient
            result = (await self.supabase.table("patient").insert(patient).execute()).data
            if result:
                return result[0]
        return {}

    async def delete(self, patient_id: int) -> None:
        await self.connect()
        if self.supabase:
            await self.supabase.table("patient").delete().eq("id", patient_id).execute()
        return None

    async def delete_by_study_id(self, study_id: int) -> None:
        await self.connect()
        if self.supabase:
            await self.supabase.table("patient").delete().eq("study_id", study_id).execute()
        return None
