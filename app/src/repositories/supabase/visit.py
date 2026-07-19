from typing import List

from src.repositories import PatientRepository
from src.dtos.visit import VisitDTO
from src.repositories.supabase.base import SupabaseRepository


TABLE = "visit"


class VisitRepository(SupabaseRepository):
    def __init__(self):
        super().__init__()

    async def load(self, visit_id: int) -> VisitDTO | None:
        await self.connect()
        if self.supabase:
            result = (await self.supabase.table(TABLE).select("*").eq("id", visit_id).execute()).data[0]
            visit = VisitDTO.from_dict(result) if result else None
            if visit:
                repo = PatientRepository()
                visit.patient = await repo.load(visit.patient_id)
                return visit
        return None

    async def list(self, study_id: int, patient_id: int = 0) -> List[VisitDTO]:
        await self.connect()
        if self.supabase:
            if patient_id == 0:
                return [VisitDTO.from_dict(v) for v in \
                        (await self.supabase.table(TABLE).select("*").eq("study_id", study_id).execute()).data]
            else:
                return [VisitDTO.from_dict(v) for v in \
                        (await self.supabase.table(TABLE).select("*")
                         .eq("study_id", study_id)
                         .eq("patient_id", patient_id).execute()).data]
        return []

    async def save(self, visit: VisitDTO) -> dict:
        return await self.insert_or_update(TABLE, visit.to_dict())

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
