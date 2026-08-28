from typing import LiteralString

from src.repositories.postgres.base import PostgresRepository


class ReportRepository(PostgresRepository):
    def __init__(self):
        super().__init__()

    async def get_count(self, sql: LiteralString) -> int:
        result = await self.execute_query(sql)
        if result:
            return result[0].get("count", 0)
        return 0

    async def get_count_by_study(self, sql: LiteralString, study_id: int) -> int:
        if study_id is None:
            return 0
        result = await self.execute_query(sql, (study_id,))
        if result:
            return result[0].get("count", 0)
        return 0

    async def get_study_count(self) -> int:
        return await self.get_count("SELECT COUNT(*) FROM study")

    async def get_patient_count(self) -> int:
        return await self.get_count("SELECT COUNT(*) FROM patient")

    async def get_patient_count_by_study(self, study_id: int) -> int:
        return await self.get_count_by_study(
            "SELECT COUNT(*) FROM patient WHERE study_id=%s", study_id
        )

    async def get_researcher_count(self) -> int:
        return await self.get_count("SELECT COUNT(*) FROM researcher")

    async def get_researcher_count_by_study(self, study_id: int) -> int:
        return await self.get_count_by_study(
            "SELECT COUNT(*) FROM study_researcher WHERE study_id=%s", study_id
        )

    async def get_visit_count(self) -> int:
        return await self.get_count("SELECT COUNT(*) FROM visit")

    async def get_visit_count_by_study(self, study_id: int) -> int:
        return await self.get_count_by_study(
            "SELECT COUNT(*) FROM visit WHERE study_id=%s", study_id
        )

    async def get_event_count(self) -> int:
        return await self.get_count("SELECT COUNT(*) FROM adverse_event")

    async def get_event_count_by_study(self, study_id: int) -> int:
        return await self.get_count_by_study(
            "SELECT COUNT(*) FROM adverse_event WHERE study_id=%s", study_id
        )

    async def get_studies(self) -> list:
        sql = "SELECT * FROM study"
        return await self.execute_query(sql)
