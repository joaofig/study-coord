import asyncio
from typing import List

from src.db import get_connection, SQLCache


class ResearcherRepository:
    def __init__(self):
        self.cache = SQLCache()

    def _get_all(self) -> List[dict]:
        conn = get_connection()
        conn.row_factory = lambda _, row: {
            "id": row[0],
            "number": row[1],
            "name": row[2],
            "phone": row[3],
            "email": row[4],
            "comments": row[5],
            "study_count": row[6],
        }
        sql = self.cache.get("researcher/get_all.sql")
        return conn.execute(sql).fetchall()

    def _get_by_id(self, researcher_id: int) -> dict | None:
        conn = get_connection()
        conn.row_factory = lambda _, row: {
            "id": row[0],
            "number": row[1],
            "name": row[2],
            "phone": row[3],
            "email": row[4],
            "comments": row[5],
            "study_count": row[6],
        }
        sql = self.cache.get("researcher/get_by_id.sql")
        return conn.execute(sql, (researcher_id,)).fetchone()

    def _get_by_number(self, researcher_number: str) -> dict | None:
        conn = get_connection()
        conn.row_factory = lambda _, row: {
            "id": row[0],
            "number": row[1],
            "name": row[2],
            "phone": row[3],
            "email": row[4],
            "comments": row[5],
        }
        sql = self.cache.get("researcher/get_by_number.sql")
        return conn.execute(sql, (researcher_number,)).fetchone()

    def _save(self, researcher: dict) -> dict:
        conn = get_connection()
        if researcher["id"] == 0:
            sql = self.cache.get("researcher/save.sql")
            cur = conn.execute(
                sql,
                (researcher["number"], researcher["name"], researcher["phone"], researcher["email"], researcher["comments"])
            )
            researcher["id"] = cur.lastrowid
            cur.close()
        else:
            conn.execute(self.cache.get("researcher/update.sql"),
                         (researcher["number"], researcher["name"],
                          researcher["phone"], researcher["email"],
                          researcher["comments"], researcher["id"]))
        conn.commit()
        return researcher

    def _delete(self, researcher_id: int) -> None:
        conn = get_connection()
        conn.execute(self.cache.get("researcher/delete_studies.sql"), (researcher_id,))
        conn.execute(self.cache.get("researcher/delete.sql"), (researcher_id,))
        conn.commit()

    async def list(self) -> List[dict]:
        return await asyncio.to_thread(self._get_all)

    async def get(self, researcher_id: int) -> dict | None:
        return await asyncio.to_thread(self._get_by_id, researcher_id)

    async def save(self, researcher: dict) -> dict:
        return await asyncio.to_thread(self._save, researcher)

    async def delete(self, researcher_id: int) -> None:
        await asyncio.to_thread(self._delete, researcher_id)
