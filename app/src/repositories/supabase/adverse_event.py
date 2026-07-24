from typing import List

from src.dtos.adverse_event import AdverseEventDTO
from src.repositories.supabase.base import SupabaseRepository


TABLE = "adverse_event"


class AdverseEventRepository(SupabaseRepository):
    def __init__(self):
        super().__init__()

    async def load(self, adverse_event_id: int) -> AdverseEventDTO | None:
        await self.connect()
        if self.supabase:
            result = (
                await self.supabase.table(TABLE)
                .select("*")
                .eq("adverse_event_id", adverse_event_id)
                .execute()
            ).data
            if result:
                return AdverseEventDTO.from_dict(result[0])
        return None

    async def list(
        self, *, study_id: int, patient_id: int = 0
    ) -> List[AdverseEventDTO]:
        await self.connect()
        if self.supabase:
            if patient_id:
                result = (
                    await self.supabase.table(TABLE)
                    .select("*")
                    .eq("study_id", study_id)
                    .eq("patient_id", patient_id)
                    .execute()
                ).data
            else:
                result = (
                    await self.supabase.table(TABLE)
                    .select("*")
                    .eq("study_id", study_id)
                    .execute()
                ).data
            if result:
                return [AdverseEventDTO.from_dict(m) for m in result]
        return []

    async def save(self, event: AdverseEventDTO) -> dict:
        return await self.insert_or_update(TABLE, event.to_dict())

    async def delete(self, *, study_id: int = 0, adverse_event_id: int = 0) -> None:
        await self.connect()
        if self.supabase:
            if study_id:
                await (
                    self.supabase.table(TABLE)
                    .delete()
                    .eq("study_id", study_id)
                    .execute()
                )
            else:
                await (
                    self.supabase.table(TABLE)
                    .delete()
                    .eq("adverse_event_id", adverse_event_id)
                    .execute()
                )
