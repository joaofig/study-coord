import asyncio
from sqlite3 import Connection

from src.db import SQLCache
from models import Researcher


def get_all(conn: Connection) -> list[Researcher]:
    conn.row_factory = lambda _, row: Researcher(
        id=row[0],
        number=row[1],
        name=row[2],
    )
    cache = SQLCache()
    sql = cache.get("researcher/get_all.sql")
    return conn.execute(sql).fetchall()


def get(conn: Connection, researcher_id: int) -> Researcher | None:
    conn.row_factory = lambda _, row: Researcher(
        id=row[0],
        number=row[1],
        name=row[2],
    )
    cache = SQLCache()
    sql = cache.get("researcher/get.sql")
    return conn.execute(sql, (researcher_id,)).fetchone()


def get_by_number(conn: Connection, researcher_number: str) -> Researcher | None:
    conn.row_factory = lambda _, row: Researcher(
        id=row[0],
        number=row[1],
        name=row[2],
    )
    cache = SQLCache()
    sql = cache.get("researcher/get_by_number.sql")
    return conn.execute(sql, (researcher_number,)).fetchone()


def save(conn: Connection, researcher: Researcher) -> None:
    cache = SQLCache()
    conn.execute(cache.get("researcher/save.sql"), (researcher.name,))


def delete(conn: Connection, researcher_id: int) -> None:
    cache = SQLCache()
    conn.execute(cache.get("researcher/delete.sql"), (researcher_id,))


class ResearcherRepository:
    def __init__(self, conn: Connection) -> None:
        self.conn: Connection = conn

    async def list(self) -> list[Researcher]:
        return await asyncio.to_thread(get_all, self.conn)

    async def get(self, researcher_id: int) -> Researcher | None:
        return await asyncio.to_thread(get, self.conn, researcher_id)

    async def save(self, researcher: Researcher) -> None:
        await asyncio.to_thread(save, self.conn, researcher)

    async def delete(self, researcher_id: int) -> None:
        await asyncio.to_thread(delete, self.conn, researcher_id)
