import asyncio

from src.db.sqlite import get_script
from src.models.study import Study
from sqlite3 import Connection


def get_all(conn: Connection) -> list[Study]:
    conn.row_factory = lambda _, row: Study(
        id=row[0],
        name=row[1],
        sponsor=row[2],
        start_date=row[3],
        end_date=row[4],
    )
    cursor = conn.execute(
        "SELECT id, name, sponsor, start_date, end_date FROM study ORDER BY name"
    )
    return cursor.fetchall()


def get(conn: Connection, study_id: int) -> Study | None:
    conn.row_factory = lambda _, row: Study(
        id=row[0],
        name=row[1],
        sponsor=row[2],
        start_date=row[3],
        end_date=row[4],
    )
    cursor = conn.execute(
        "SELECT id, name, sponsor, start_date, end_date FROM study WHERE id = ?",
        (study_id,),
    )
    return cursor.fetchone()


def save(conn: Connection, study: Study) -> None:
    conn.execute(
        get_script("study/save.sql"),
        (study.name, study.sponsor, study.start_date, study.end_date)
    )


def delete(conn: Connection, study_id: int) -> None:
    conn.execute(
        "DELETE FROM study WHERE id = ?",
        (study_id,),
    )


class StudyRepository:
    def __init__(self, conn: Connection):
        self.conn: Connection = conn

    async def list(self):
        return await asyncio.to_thread(get_all, self.conn)

    async def get(self, study_id: int) -> Study | None:
        return await asyncio.to_thread(get, self.conn, study_id)

    async def save(self, study: Study) -> None:
        await asyncio.to_thread(save, self.conn, study)

    async def delete(self, study_id: int) -> None:
        await asyncio.to_thread(delete, self.conn, study_id)
