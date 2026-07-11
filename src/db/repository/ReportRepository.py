import asyncio

from db import get_connection, SQLCache


class ReportRepository:
    def __init__(self):
        self.cache = SQLCache()

    def _get_study_count(self) -> int:
        conn = get_connection()
        conn.row_factory = lambda _, row: int(row[0])
        sql = self.cache.get("report/get_study_count.sql")
        return conn.execute(sql).fetchone()

    def _get_patient_count(self) -> int:
        conn = get_connection()
        conn.row_factory = lambda _, row: int(row[0])
        sql = self.cache.get("report/get_patient_count.sql")
        return conn.execute(sql).fetchone()

    def _get_researcher_count(self) -> int:
        conn = get_connection()
        conn.row_factory = lambda _, row: int(row[0])
        sql = self.cache.get("report/get_researcher_count.sql")
        return conn.execute(sql).fetchone()

    async def get_study_count(self) -> int:
        return await asyncio.to_thread(self._get_study_count)

    async def get_patient_count(self) -> int:
        return await asyncio.to_thread(self._get_patient_count)

    async def get_researcher_count(self) -> int:
        return await asyncio.to_thread(self._get_researcher_count)