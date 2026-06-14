import asyncio
from sqlite3 import Connection

from models import Researcher


def get_all(conn: Connection) -> list[Researcher]:
    conn.row_factory = lambda _, row: Researcher(
        id=row[0],
        name=row[1],
        type=row[2],
    )
    return conn.execute("SELECT id, name, type FROM researcher").fetchall()


def get(conn: Connection, researcher_id: int) -> Researcher | None:
    conn.row_factory = lambda _, row: Researcher(
        id=row[0],
        name=row[1],
        type=row[2],
    )
    return conn.execute("SELECT id, name, type FROM researcher WHERE id=?", (researcher_id,)).fetchone()


def save(conn: Connection, researcher: Researcher) -> None:
    conn.execute(
        "INSERT INTO researcher (name, type) VALUES (?, ?)",
        (researcher.name, researcher.type),
    )


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
