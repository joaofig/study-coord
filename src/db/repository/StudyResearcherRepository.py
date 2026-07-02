import asyncio
from typing import List

from db import SQLCache, get_connection


class StudyResearcherRepository:
    def __init__(self):
        self.cache = SQLCache()

    def _get_by_study_id(self, study_id: int) -> List[dict]:
        conn = get_connection()
        conn.row_factory = lambda _, row: {
            "id": row[0],
            "study_id": row[1],
            "researcher_id": row[2],
            "role": row[3],
            "study_comments": row[4],
            "number": row[5],
            "name": row[6],
            "phone": row[7],
            "email": row[8],
        }
        sql = self.cache.get("study_researcher/get_by_study_id.sql")
        return conn.execute(sql, (study_id,)).fetchall()

    def _get_by_id(self, sr_id: int) -> dict | None:
        conn = get_connection()
        conn.row_factory = lambda _, row: {
            "id": row[0],
            "study_id": row[1],
            "researcher_id": row[2],
            "role": row[3],
            "study_comments": row[4],
            "number": row[5],
            "name": row[6],
            "phone": row[7],
            "email": row[8],
        }
        sql = self.cache.get("study_researcher/get_by_id.sql")
        return conn.execute(sql, (sr_id,)).fetchone()

    def _save(self, researcher: dict) -> dict:
        conn = get_connection()
        if researcher["id"] == 0:
            sql = self.cache.get("study_researcher/save.sql")
            cur = conn.execute(
                sql,
                (researcher["study_id"],
                    researcher["researcher_id"], researcher["role"], researcher["study_comments"])
            )
            researcher["id"] = cur.lastrowid
            cur.close()
        else:
            conn.execute(self.cache.get("study_researcher/update.sql"),
                         (researcher["researcher_id"], researcher["role"],
                          researcher["study_comments"], researcher["id"]))
        conn.commit()
        return researcher

    def _delete(self, researcher_id: int) -> None:
        conn = get_connection()
        conn.execute(self.cache.get("study_researcher/delete.sql"), (researcher_id,))
        conn.commit()

    async def list(self, study_id: int) -> List[dict]:
        return await asyncio.to_thread(self._get_by_study_id, study_id=study_id)

    async def get(self, researcher_id: int) -> dict | None:
        return await asyncio.to_thread(self._get_by_id, researcher_id)

    async def save(self, researcher: dict) -> dict:
        return await asyncio.to_thread(self._save, researcher)

    async def delete(self, researcher_id: int) -> None:
        await asyncio.to_thread(self._delete, researcher_id)
