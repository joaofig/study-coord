from typing import List

from src.dtos.researcher import StudyResearcherDTO
from src.repositories.supabase.base import SupabaseRepository

TABLE = "study_researcher"

class StudyResearcherRepository(SupabaseRepository):
    def __init__(self):
        super().__init__()

    async def load(self, researcher_id: int) -> StudyResearcherDTO | None:
        await self.connect()
        if self.supabase:
            result = (await self.supabase.table(TABLE)
                      .select("*")
                      .eq("researcher_id", researcher_id).execute()).data
            if result:
                return StudyResearcherDTO.from_dict(result[0])
        return None

    async def list(self, study_id: int) -> List[StudyResearcherDTO]:
        await self.connect()
        if self.supabase:
            result = (await self.supabase.table(TABLE)
                      .select("*")
                      .eq("study_id", study_id).execute()).data
            if result:
                return [StudyResearcherDTO.from_dict(sr) for sr in result]
        return []

    async def delete(self, researcher_id: int) -> None:
        await self.connect()
        if self.supabase:
            await self.supabase.table(TABLE).delete().eq("researcher_id", researcher_id).execute()
        return None

    async def save(self, sr: StudyResearcherDTO) -> None:
        await self.insert_or_update(TABLE, sr.to_dict())

    async def delete_by_study(self, study_id: int) -> None:
        await self.connect()
        if self.supabase:
            await self.supabase.table(TABLE).delete().eq("study_id", study_id).execute()
        return None