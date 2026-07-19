from typing import List

from dtos.study import StudyDTO, StudyRowDTO
from repositories.supabase.base import SupabaseRepository


TABLE = "study"


class StudyRepository(SupabaseRepository):
    def __init__(self):
        super().__init__()

    async def list(self) -> List[StudyRowDTO]:
        await self.connect()
        if self.supabase:
            # We are reading from a view, not a table
            return [StudyRowDTO(**s) for s in
                        (await self.supabase.table("study_list").select("*").execute()).data
                    ]
        return []

    async def load(self, study_id: int) -> StudyDTO | None:
        await self.connect()
        if self.supabase:
            result = (await self.supabase.table(TABLE).select("*").eq("id", study_id).execute()).data
            if result:
                return result[0]
        return None

    async def save(self, study: StudyDTO) -> dict:
        return await self.insert_or_update(TABLE, study.to_dict())

    async def delete(self, study_id: int) -> None:
        await self.connect()
        if self.supabase:
            await self.supabase.table(TABLE).delete().eq("id", study_id).execute()
        return None
