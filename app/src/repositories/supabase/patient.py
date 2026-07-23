from typing import List

from src.dtos.patient import PatientDTO
from src.repositories.supabase.base import SupabaseRepository


TABLE = "patient"


class PatientRepository(SupabaseRepository):
    def __init__(self):
        super().__init__()

    async def load(self, patient_id: int) -> PatientDTO | None:
        await self.connect()
        if self.supabase:
            result = (await self.supabase.table(TABLE).select("*").eq("patient_id", patient_id).execute()).data
            if result:
                return PatientDTO.from_dict(result[0])
        return None

    async def list(self, study_id: int) -> List[PatientDTO]:
        await self.connect()
        if self.supabase:
            result = (await self.supabase.table(TABLE).select("*").eq("study_id", study_id).execute()).data
            if result:
                return [PatientDTO.from_dict(p) for p in result]
        return []

    async def save(self, patient: PatientDTO) -> dict:
        return await self.insert_or_update(TABLE, patient.to_dict())

    async def delete(self, *, patient_id: int = 0, study_id: int = 0) -> None:
        await self.connect()
        if self.supabase:
            if study_id:
                await self.supabase.table(TABLE).delete().eq("study_id", study_id).execute()
            else:
                await self.supabase.table(TABLE).delete().eq("patient_id", patient_id).execute()
        return None
