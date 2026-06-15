import asyncio
from sqlite3 import Connection

from db.sqlite import get_script
from models import Researcher


def get_all(conn: Connection) -> list[Researcher]:
    conn.row_factory = lambda _, row: Researcher(
        id=row[0],
        name=row[1],
    )
    sql = get_script("researcher/get_all.sql")
    return conn.execute(sql).fetchall()


def get(conn: Connection, researcher_id: int) -> Researcher | None:
    conn.row_factory = lambda _, row: Researcher(
        id=row[0],
        name=row[1],
    )
    sql = get_script("researcher/get.sql")
    return conn.execute(sql, (researcher_id,)).fetchone()


def save(conn: Connection, researcher: Researcher) -> None:
    conn.execute(get_script("researcher/save.sql"), (researcher.name,))


def delete(conn: Connection, researcher_id: int) -> None:
    conn.execute(get_script("researcher/delete.sql"), (researcher_id,))


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
