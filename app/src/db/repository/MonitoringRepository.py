import asyncio
from typing import List

from src.db import SQLCache, get_connection


class MonitoringRepository:
    def __init__(self):
        self.cache = SQLCache()

    def _get_by_id(self, monitoring_id: int) -> dict | None:
        conn = get_connection()
        conn.row_factory = lambda _, row: {
            "id": row[0],
            "study_id": row[1],
            "date": row[2],
            "monitor": row[3],
            "comments": row[4],
        }
        cursor = conn.execute(self.cache.load("monitoring/get_by_id.sql"), (monitoring_id,))
        return cursor.fetchone()

    def _get_by_study_id(self, study_id: int) -> List[dict]:
        conn = get_connection()
        conn.row_factory = lambda _, row: {
            "id": row[0],
            "study_id": row[1],
            "date": row[2],
            "monitor": row[3],
            "comments": row[4],
        }
        cursor = conn.execute(self.cache.load("monitoring/get_by_study_id.sql"), (study_id,))
        return cursor.fetchall()

    def _save(self, monitoring: dict) -> dict:
        conn = get_connection()
        if monitoring.get("id", 0) > 0:
            conn.execute(
                self.cache.load("monitoring/update.sql"),
                (monitoring["study_id"], monitoring["date"], monitoring["monitor"], monitoring["comments"], monitoring["id"])
            )
        else:
            cur = conn.execute(
                self.cache.load("monitoring/save.sql"),
                (monitoring["study_id"], monitoring["date"], monitoring["monitor"], monitoring["comments"])
            )
            monitoring["id"] = cur.lastrowid
            cur.close()
        conn.commit()
        return monitoring

    def _delete(self, monitoring_id: int) -> None:
        conn = get_connection()
        conn.execute(
            self.cache.load("monitoring/delete.sql"),
            (monitoring_id,)
        )
        conn.commit()

    def _delete_by_study_id(self, study_id: int) -> None:
        conn = get_connection()
        conn.execute(
            self.cache.load("monitoring/delete_by_study_id.sql"),
            (study_id,)
        )
        conn.commit()

    async def get(self, monitoring_id: int) -> dict | None:
        return await asyncio.to_thread(self._get_by_id, monitoring_id)

    async def get_by_study_id(self, study_id: int) -> List[dict]:
        return await asyncio.to_thread(self._get_by_study_id, study_id)

    async def save(self, monitoring: dict) -> dict:
        return await asyncio.to_thread(self._save, monitoring)

    async def delete(self, monitoring_id: int) -> None:
        await asyncio.to_thread(self._delete, monitoring_id)

    async def delete_by_study_id(self, study_id: int) -> None:
        await asyncio.to_thread(self._delete_by_study_id, study_id)
