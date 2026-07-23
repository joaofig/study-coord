from typing import List

from src.dtos.researcher import ResearcherDTO
from src.repositories.supabase.base import SupabaseRepository

TABLE = "researcher"

class ResearcherRepository(SupabaseRepository):
    def __init__(self):
        super().__init__()

    async def load(self, researcher_id: int) -> ResearcherDTO | None:
        await self.connect()
        if self.supabase:
            result = (await self.supabase.table(TABLE).select("*").eq("researcher_id", researcher_id).execute()).data
            if result:
                return ResearcherDTO.from_dict(result[0])
        return None

    async def save(self, researcher: ResearcherDTO) -> dict:
        return await self.insert_or_update(TABLE, researcher.to_dict())

    async def delete(self, researcher_id: int):
        await self.connect()
        if self.supabase:
            await self.supabase.table(TABLE).delete().eq("researcher_id", researcher_id).execute()

    async def list(self) -> List[ResearcherDTO]:
        await self.connect()
        if self.supabase:
            result = (await self.supabase.table(TABLE).select("*").execute()).data
            if result:
                return [ResearcherDTO.from_dict(r) for r in result]
        return []