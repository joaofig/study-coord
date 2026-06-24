import asyncio
from typing import List

from db import get_connection
from src.db import SQLCache


class PatientRepository:
    def __init__(self):
        self.cache = SQLCache()

    def _get_all(self) -> List[dict]:
        conn = get_connection()
        conn.row_factory = lambda _, row: {
            "id": row[0],
            "study_id": row[1],
            "study_name": row[2],
            "study_sponsor": row[3],
            "number": row[4],
            "start_date": row[5],
            "exit_date": row[6],
            "status": row[7],
            "comments": row[8],
        }
        cursor = conn.execute(self.cache.get("patient/get_all.sql"))
        return cursor.fetchall()

    def _get_by_id(self, patient_id: int) -> dict | None:
        conn = get_connection()
        conn.row_factory = lambda _, row: {
            "id": row[0],
            "study_id": row[1],
            "study_name": row[2],
            "study_sponsor": row[3],
            "number": row[4],
            "start_date": row[5],
            "exit_date": row[6],
            "status": row[7],
        }
        cursor = conn.execute(self.cache.get("patient/get_by_id.sql"), (patient_id,))
        return cursor.fetchone()

    def _get_by_study_id(self, study_id: int) -> List[dict]:
        conn = get_connection()
        conn.row_factory = lambda _, row: {
            "id": row[0],
            "study_id": row[1],
            "study_name": row[2],
            "study_sponsor": row[3],
            "number": row[4],
            "start_date": row[5],
            "exit_date": row[6],
            "status": row[7],
            "comments": row[8],
        }
        cursor = conn.execute(self.cache.get("patient/get_by_study_id.sql"), (study_id,))
        return cursor.fetchall()

    def _save(self, patient: dict) -> dict:
        conn = get_connection()
        if patient.get("id") is not None:
            cur = conn.execute(
                self.cache.get("patient/update.sql"),
                (patient["study_id"], patient["number"], patient["start_date"], patient["exit_date"],
                 patient["status"], patient["comments"], patient["id"])
            )
            patient["id"] = cur.lastrowid
            cur.close()
        else:
            conn.execute(
                self.cache.get("patient/save.sql"),
                (patient["study_id"], patient["number"], patient["start_date"], patient["exit_date"], patient["status"],
                 patient["comments"])
            )
        conn.commit()
        return patient

    def _delete(self, patient_id: int) -> None:
        conn = get_connection()
        conn.execute(
            self.cache.get("patient/delete.sql"),
            (patient_id,)
        )

    async def list(self) -> List[dict]:
        return await asyncio.to_thread(self._get_all)

    async def get(self, patient_id: int) -> dict | None:
        return await asyncio.to_thread(self._get_by_id, patient_id)

    async def get_by_study_id(self, study_id: int) -> List[dict]:
        return await asyncio.to_thread(self._get_by_study_id, study_id)

    async def save(self, patient: dict) -> dict:
        await asyncio.to_thread(self._save, patient)

    async def delete(self, patient_id: int) -> None:
        await asyncio.to_thread(self._delete, patient_id)
