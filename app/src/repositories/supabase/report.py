from postgrest import CountMethod

from repositories.supabase.base import SupabaseRepository


class ReportRepository(SupabaseRepository):
    def __init__(self):
        super().__init__()

    async def get_count(self, table: str) -> int:
        await self.connect()
        if self.supabase:
            response = await (self.supabase.table(table)
                          .select("*", count=CountMethod.exact, head=True).execute())
            if response.count:
                return response.count
        return 0

    async def get_count_by_study(self, table: str, study_id: int) -> int:
        await self.connect()
        if self.supabase:
            response = await (self.supabase.table(table)
                          .select("*", count=CountMethod.exact, head=True)
                          .eq("study_id", study_id)
                          .execute())
            if response.count:
                return response.count
        return 0

    async def get_study_count(self) -> int:
        return await self.get_count("study")

    async def get_patient_count(self) -> int:
        return await self.get_count("patient")

    async def get_patient_count_by_study(self, study_id: int) -> int:
        return await self.get_count_by_study("patient", study_id)

    async def get_researcher_count(self) -> int:
        return await self.get_count("researcher")

    async def get_researcher_count_by_study(self, study_id: int) -> int:
        return await self.get_count_by_study("study_researcher", study_id)

    async def get_visit_count(self) -> int:
        return await self.get_count("visit")

    async def get_visit_count_by_study(self, study_id: int) -> int:
        return await self.get_count_by_study("visit", study_id)

    async def get_event_count(self) -> int:
        return await self.get_count("event")

    async def get_event_count_by_study(self, study_id: int) -> int:
        return await self.get_count_by_study("event", study_id)
