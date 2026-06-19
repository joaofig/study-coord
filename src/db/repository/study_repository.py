import asyncio

from src.db.sqlite import get_connection
from src.db import SQLCache
from src.models.study import Study, StudyRow


def get_all() -> list[StudyRow]:
    conn = get_connection()
    conn.row_factory = lambda _, row: StudyRow(
        id=row[0],
        name=row[1],
        sponsor=row[2],
        start_date=row[3],
        end_date=row[4],
        proto_visits=row[5],
        comments=row[6],
        patients=row[7],
        visits=row[8],
        researchers=row[9],
        adverse_events=row[10],
    )
    cache = SQLCache()
    cursor = conn.execute(cache.get("study/get_all.sql"))
    return cursor.fetchall()


def get(study_id: int) -> Study | None:
    conn = get_connection()
    conn.row_factory = lambda _, row: Study(
        id=row[0],
        name=row[1],
        sponsor=row[2],
        start_date=row[3],
        end_date=row[4],
        proto_visits=row[5],
        comments=row[6]
    )
    cache = SQLCache()
    cursor = conn.execute(
        cache.get("study/get.sql"),
        (study_id,),
    )
    return cursor.fetchone()


def save(study: Study) -> None:
    conn = get_connection()
    cache = SQLCache()

    if study.id == 0:
        sql = cache.get("study/save.sql")
        cur = conn.execute(
            sql,
            (study.name, study.sponsor, study.start_date, study.end_date, study.proto_visits, study.comments),
        )
        study.id = cur.lastrowid
        cur.close()
    else:
        sql = cache.get("study/update.sql")
        conn.execute(
            sql,
            (study.name, study.sponsor, study.start_date, study.end_date, study.proto_visits, study.comments, study.id),
        )
    conn.commit()


def delete(study_id: int) -> None:
    conn = get_connection()
    cache = SQLCache()
    conn.execute(
        cache.get("study/delete.sql"),
        (study_id,),
    )
    conn.commit()


class StudyRepository:
    async def list(self):
        return await asyncio.to_thread(get_all)

    async def get(self, study_id: int) -> Study | None:
        return await asyncio.to_thread(get, study_id)

    async def save(self, study: Study) -> None:
        await asyncio.to_thread(save, study)

    async def delete(self, study_id: int) -> None:
        await asyncio.to_thread(delete, study_id)
