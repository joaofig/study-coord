from typing import List

from src.dtos.monitoring import MonitoringDTO
from src.repositories.supabase.base import SupabaseRepository


TABLE = "monitoring"


class MonitoringRepository(SupabaseRepository):
    def __init__(self):
        super().__init__()

    async def load(self, monitoring_id: int) -> MonitoringDTO | None:
        await self.connect()
        if self.supabase:
            result = (
                await self.supabase.table(TABLE)
                .select("*")
                .eq("monitoring_id", monitoring_id)
                .execute()
            ).data
            if result:
                return MonitoringDTO.from_dict(result[0])
        return None

    async def list(self, study_id: int) -> List[MonitoringDTO]:
        await self.connect()
        if self.supabase:
            result = (
                await self.supabase.table(TABLE)
                .select("*")
                .eq("study_id", study_id)
                .execute()
            ).data
            if result:
                return [MonitoringDTO.from_dict(m) for m in result]
        return []

    async def save(self, monitoring: MonitoringDTO) -> dict:
        return await self.insert_or_update(TABLE, monitoring.to_dict())

    async def delete(self, *, monitoring_id: int = 0, study_id: int = 0) -> None:
        await self.connect()
        if self.supabase:
            if monitoring_id:
                await (
                    self.supabase.table(TABLE)
                    .delete()
                    .eq("monitoring_id", monitoring_id)
                    .execute()
                )
            elif study_id:
                await (
                    self.supabase.table(TABLE)
                    .delete()
                    .eq("study_id", study_id)
                    .execute()
                )
        return None
