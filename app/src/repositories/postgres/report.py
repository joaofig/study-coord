from src.repositories.postgres.base import PostgresRepository


class ReportRepository(PostgresRepository):
    def __init__(self):
        super().__init__()

    async def get_count(self, table: str) -> int:
        sql = f'SELECT COUNT(*) AS count FROM "{table}"'
        result = await self.execute_query(sql)
        if result:
            return result[0].get("count", 0)
        return 0

    async def get_count_by_study(self, table: str, study_id: int) -> int:
        if study_id is None:
            return 0
        sql = f'SELECT COUNT(*) AS count FROM "{table}" WHERE study_id = %s'
        result = await self.execute_query(sql, (study_id,))
        if result:
            return result[0].get("count", 0)
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
        return await self.get_count("adverse_event")

    async def get_event_count_by_study(self, study_id: int) -> int:
        return await self.get_count_by_study("adverse_event", study_id)

    async def get_studies(self) -> list:
        sql = 'SELECT * FROM "study"'
        return await self.execute_query(sql)
