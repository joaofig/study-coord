from typing import List

from src.dtos.study import StudyDTO, StudyRowDTO
from src.repositories.supabase.base import SupabaseRepository


TABLE = "study"


class StudyRepository(SupabaseRepository):
    def __init__(self):
        super().__init__()

    async def list(self) -> List[StudyRowDTO]:
        await self.connect()
        if self.supabase:
            # We are reading from a view, not a table
            result = (await self.supabase.table("study_list").select("*").execute()).data
            return [StudyRowDTO.from_dict(s) for s in result]
        return []

    async def load(self, study_id: int) -> StudyDTO | None:
        await self.connect()
        if self.supabase:
            result = (await self.supabase.table(TABLE).select("*").eq("study_id", study_id).execute()).data
            if result:
                return StudyDTO.from_dict(result[0])
        return None

    async def save(self, study: StudyDTO) -> dict:
        return await self.insert_or_update(TABLE, study.to_dict())

    async def delete(self, study_id: int) -> None:
        await self.connect()
        if self.supabase:
            await self.supabase.table(TABLE).delete().eq("study_id", study_id).execute()
        return None
