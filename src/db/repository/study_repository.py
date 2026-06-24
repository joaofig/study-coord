import asyncio
from typing import List

from src.db.sqlite import get_connection
from src.db import SQLCache


class StudyRepository:
    def __init__(self):
        self.cache = SQLCache()

    def _get_all(self) -> list[dict]:
        conn = get_connection()
        conn.row_factory = lambda _, row: {
            "id": row[0],
            "name": row[1],
            "sponsor": row[2],
            "start_date": row[3],
            "end_date": row[4],
            "proto_visits": row[5],
            "comments": row[6],
            "patients": row[7],
            "visits": row[8],
            "researchers": row[9],
            "adverse_events": row[10],
        }
        cursor = conn.execute(self.cache.get("study/get_all.sql"))
        return cursor.fetchall()

    def _get_by_id(self, study_id: int) -> dict | None:
        conn = get_connection()
        conn.row_factory = lambda _, row: {
            "id": row[0],
            "name": row[1],
            "sponsor": row[2],
            "start_date": row[3],
            "end_date": row[4],
            "proto_visits": row[5],
            "comments": row[6],
        }
        cursor = conn.execute(
            self.cache.get("study/get_by_id.sql"),
            (study_id,),
        )
        return cursor.fetchone()

    def _save(self, study: dict) -> dict:
        conn = get_connection()

        if study["id"] == 0:
            sql = self.cache.get("study/save.sql")
            cur = conn.execute(
                sql,
                (study["name"], study["sponsor"], study["start_date"], study["end_date"], study["proto_visits"],
                 study["comments"]),
            )
            study["id"] = cur.lastrowid
            cur.close()
        else:
            sql = self.cache.get("study/update.sql")
            conn.execute(
                sql,
                (study["name"], study["sponsor"], study["start_date"], study["end_date"], study["proto_visits"],
                 study["comments"], study["id"]),
            )
        conn.commit()
        return study

    def _delete(self, study_id: int) -> None:
        conn = get_connection()
        conn.execute(
            self.cache.get("study/delete.sql"),
            (study_id,),
        )
        conn.commit()

    async def list(self) -> List[dict]:
        return await asyncio.to_thread(self._get_all)

    async def get(self, study_id: int) -> dict | None:
        return await asyncio.to_thread(self._get_by_id, study_id)

    async def save(self, study: dict) -> dict:
        return await asyncio.to_thread(self._save, study)

    async def delete(self, study_id: int) -> None:
        await asyncio.to_thread(self._delete, study_id)
