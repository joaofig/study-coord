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

    def _get_patient_count_by_study(self, study_id: int) -> int:
        conn = get_connection()
        conn.row_factory = lambda _, row: int(row[0])
        sql = self.cache.get("report/get_patient_count_by_study.sql")
        return conn.execute(sql, (study_id,)).fetchone()

    def _get_researcher_count(self) -> int:
        conn = get_connection()
        conn.row_factory = lambda _, row: int(row[0])
        sql = self.cache.get("report/get_researcher_count.sql")
        return conn.execute(sql).fetchone()

    def _get_researcher_count_by_study(self, study_id: int) -> int:
        conn = get_connection()
        conn.row_factory = lambda _, row: int(row[0])
        sql = self.cache.get("report/get_researcher_count_by_study.sql")
        return conn.execute(sql, (study_id,)).fetchone()

    def _get_visit_count(self) -> int:
        conn = get_connection()
        conn.row_factory = lambda _, row: int(row[0])
        sql = self.cache.get("report/get_visit_count.sql")
        return conn.execute(sql).fetchone()

    def _get_visit_count_by_study(self, study_id: int) -> int:
        conn = get_connection()
        conn.row_factory = lambda _, row: int(row[0])
        sql = self.cache.get("report/get_visit_count_by_study.sql")
        return conn.execute(sql, (study_id,)).fetchone()

    def _get_event_count(self) -> int:
        conn = get_connection()
        conn.row_factory = lambda _, row: int(row[0])
        sql = self.cache.get("report/get_event_count.sql")
        return conn.execute(sql).fetchone()

    def _get_event_count_by_study(self, study_id: int) -> int:
        conn = get_connection()
        conn.row_factory = lambda _, row: int(row[0])
        sql = self.cache.get("report/get_event_count_by_study.sql")
        return conn.execute(sql, (study_id,)).fetchone()

    def _get_studies(self) -> list[dict]:
        conn = get_connection()
        conn.row_factory = lambda _, row: {
            "id": int(row[0]),
            "name": row[1],
        }
        sql = self.cache.get("report/get_studies.sql")
        return conn.execute(sql).fetchall()

    async def get_study_count(self) -> int:
        return await asyncio.to_thread(self._get_study_count)

    async def get_patient_count(self) -> int:
        return await asyncio.to_thread(self._get_patient_count)

    async def get_patient_count_by_study(self, study_id: int) -> int:
        return await asyncio.to_thread(self._get_patient_count_by_study, study_id)

    async def get_researcher_count(self) -> int:
        return await asyncio.to_thread(self._get_researcher_count)

    async def get_researcher_count_by_study(self, study_id: int) -> int:
        return await asyncio.to_thread(self._get_researcher_count_by_study, study_id)

    async def get_visit_count(self) -> int:
        return await asyncio.to_thread(self._get_visit_count)

    async def get_visit_count_by_study(self, study_id: int) -> int:
        return await asyncio.to_thread(self._get_visit_count_by_study, study_id)

    async def get_event_count(self) -> int:
        return await asyncio.to_thread(self._get_event_count)

    async def get_event_count_by_study(self, study_id: int) -> int:
        return await asyncio.to_thread(self._get_event_count_by_study, study_id)

    async def get_studies(self) -> list[dict]:
        return await asyncio.to_thread(self._get_studies)
