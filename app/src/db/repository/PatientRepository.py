import asyncio
from typing import List

from src.db import get_connection
from src.db import SQLCache


class PatientRepository:
    def __init__(self):
        self.cache = SQLCache()

    def _get_by_id(self, patient_id: int) -> dict | None:
        conn = get_connection()
        conn.row_factory = lambda _, row: {
            "id": row[0],
            "study_id": row[1],
            "number": row[2],
            "name": row[3],
            "start_date": row[4],
            "exit_date": row[5],
            "status": row[6],
            "comments": row[7],
        }
        cursor = conn.execute(self.cache.load("patient/get_by_id.sql"), (patient_id,))
        return cursor.fetchone()

    def _get_by_study_id(self, study_id: int) -> List[dict]:
        conn = get_connection()
        conn.row_factory = lambda _, row: {
            "id": row[0],
            "study_id": row[1],
            "number": row[2],
            "name": row[3],
            "start_date": row[4],
            "exit_date": row[5],
            "status": row[6],
            "comments": row[7],
        }
        cursor = conn.execute(self.cache.load("patient/get_by_study_id.sql"), (study_id,))
        return cursor.fetchall()

    def _save(self, patient: dict) -> dict:
        conn = get_connection()
        if patient.get("id", 0) > 0:
            conn.execute(
                self.cache.load("patient/update.sql"),
                (patient["study_id"], patient["number"], patient["name"], patient["start_date"], patient["exit_date"],
                 patient["status"], patient["comments"], patient["id"])
            )

        else:
            cur = conn.execute(
                self.cache.load("patient/save.sql"),
                (patient["study_id"], patient["number"], patient["name"], patient["start_date"],
                 patient["exit_date"], patient["status"],
                 patient["comments"])
            )
            patient["id"] = cur.lastrowid
            cur.close()
        conn.commit()
        return patient

    def _delete(self, patient_id: int) -> None:
        conn = get_connection()
        conn.execute(
            self.cache.load("patient/delete.sql"),
            (patient_id,)
        )
        conn.commit()

    def _delete_by_study_id(self, study_id: int) -> None:
        conn = get_connection()
        conn.execute(
            self.cache.load("patient/delete_by_study_id.sql"),
            (study_id,)
        )
        conn.commit()

    async def get(self, patient_id: int) -> dict | None:
        return await asyncio.to_thread(self._get_by_id, patient_id)

    async def get_by_study_id(self, study_id: int) -> List[dict]:
        return await asyncio.to_thread(self._get_by_study_id, study_id)

    async def save(self, patient: dict) -> dict:
        return await asyncio.to_thread(self._save, patient)

    async def delete(self, patient_id: int) -> None:
        await asyncio.to_thread(self._delete, patient_id)

    async def delete_by_study_id(self, study_id: int) -> None:
        await asyncio.to_thread(self._delete_by_study_id, study_id)
