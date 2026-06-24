import asyncio
from typing import List

from src.db import get_connection, SQLCache
from src.models import Researcher


class ResearcherRepository:
    def __init__(self):
        self.cache = SQLCache()

    def get_all(self) -> list[Researcher]:
        conn = get_connection()
        conn.row_factory = lambda _, row: Researcher(
            id=row[0],
            number=row[1],
            name=row[2],
            comments=row[3],
        )
        sql = self.cache.get("researcher/get_all.sql")
        return conn.execute(sql).fetchall()

    def get_by_id(self, researcher_id: int) -> Researcher | None:
        conn = get_connection()
        conn.row_factory = lambda _, row: Researcher(
            id=row[0],
            number=row[1],
            name=row[2],
            comments=row[3],
        )
        sql = self.cache.get("researcher/get_by_id.sql")
        return conn.execute(sql, (researcher_id,)).fetchone()

    def get_by_number(self, researcher_number: str) -> Researcher | None:
        conn = get_connection()
        conn.row_factory = lambda _, row: Researcher(
            id=row[0],
            number=row[1],
            name=row[2],
            comments=row[3],
        )
        sql = self.cache.get("researcher/get_by_number.sql")
        return conn.execute(sql, (researcher_number,)).fetchone()

    def _save(self, researcher: dict) -> dict:
        conn = get_connection()
        if researcher["id"] is None:
            sql = self.cache.get("researcher/save.sql")
            cur = conn.execute(
                sql,
                (researcher["number"], researcher["name"], researcher["comments"])
            )
            researcher["id"] = cur.lastrowid
            cur.close()
        else:
            conn.execute(self.cache.get("researcher/update.sql"),
                         (researcher["number"], researcher["name"], researcher["comments"], researcher["id"]))
        conn.commit()
        return researcher

    def _delete(self, researcher_id: int) -> None:
        conn = get_connection()
        conn.execute(self.cache.get("researcher/delete.sql"), (researcher_id,))

    async def list(self) -> List[Researcher]:
        return await asyncio.to_thread(self.get_all)

    async def get(self, researcher_id: int) -> Researcher | None:
        return await asyncio.to_thread(self.get_by_id, researcher_id)

    async def save(self, researcher: Researcher) -> None:
        await asyncio.to_thread(self._save, researcher.to_dict())

    async def delete(self, researcher_id: int) -> None:
        await asyncio.to_thread(self._delete, researcher_id)



class StudyResearcherRepository:
    def __init__(self):
        self.cache = SQLCache()

