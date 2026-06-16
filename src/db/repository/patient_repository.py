import asyncio
from sqlite3 import Connection

from src.db import SQLCache
from models import Patient


def get_all(conn: Connection) -> list[Patient]:
    sql_cache = SQLCache()
    conn.row_factory = lambda _, row: Patient(
        id=row[0],
        study_id=row[1],
        study_name=row[2],
        study_sponsor=row[3],
        number=row[4],
        start_date=row[5],
        exit_date=row[6],
        status=row[7],
        comments=row[8],
    )
    cursor = conn.execute(sql_cache.get("patient/get_all.sql"))
    return cursor.fetchall()


def get(conn: Connection, patient_id: int) -> Patient | None:
    sql_cache = SQLCache()
    conn.row_factory = lambda _, row: Patient(
        id=row[0],
        study_id=row[1],
        study_name=row[2],
        study_sponsor=row[3],
        number=row[4],
        start_date=row[5],
        exit_date=row[6],
        status=row[7],
    )
    cursor = conn.execute(sql_cache.get("patient/get_all.sql"), (patient_id,))
    return cursor.fetchone()


def save(conn: Connection, patient: Patient) -> None:
    sql_cache = SQLCache()
    conn.execute(
        sql_cache.get("patient/save.sql"),
        (patient.study_id, patient.number, patient.start_date, patient.exit_date, patient.status, patient.comments)
    )

def delete(conn: Connection, patient_id: int) -> None:
    sql_cache = SQLCache()
    conn.execute(
        sql_cache.get("patient/delete.sql"),
        (patient_id,)
    )


class PatientRepository:
    def __init__(self, conn: Connection) -> None:
        self.conn: Connection = conn

    async def list(self, patient_id: int | None = None) -> list[Patient]:
        if patient_id:
            return await asyncio.to_thread(get, self.conn, patient_id)
        else:
            return await asyncio.to_thread(get_all, self.conn)

    async def get(self, patient_id: int) -> Patient | None:
        return await asyncio.to_thread(get, self.conn, patient_id)

    async def save(self, patient: Patient) -> None:
        await asyncio.to_thread(save, self.conn, patient)

    async def delete(self, patient_id: int) -> None:
        await asyncio.to_thread(delete, self.conn, patient_id)
