import asyncio
from typing import List

from src.db import SQLCache, get_connection


class EventRepository:
    def __init__(self):
        self.cache = SQLCache()

    def _get_by_id(self, event_id: int) -> dict | None:
        conn = get_connection()
        conn.row_factory = lambda _, row: {
            "id": row[0],
            "study_id": row[1],
            "patient_id": row[2],
            "patient_number": row[3],
            "patient_name": row[4],
            "date": row[5],
            "event_type": row[6],
            "description": row[7],
            "comments": row[8]
        }
        cursor = conn.execute(self.cache.get("event/get_by_id.sql"), (event_id,))
        return cursor.fetchone()

    def _get_by_study_and_patient(self, study_id: int, patient_id: int) -> List[dict]:
        conn = get_connection()
        conn.row_factory = lambda _, row: {
            "id": row[0],
            "study_id": row[1],
            "patient_id": row[2],
            "patient_number": row[3],
            "patient_name": row[4],
            "date": row[5],
            "event_type": row[6],
            "description": row[7],
            "comments": row[8]
        }
        cursor = conn.execute(self.cache.get("event/get_by_study_and_patient.sql"), (study_id, patient_id))
        return cursor.fetchall()

    def _save(self, event: dict) -> dict:
        conn = get_connection()
        if event.get("id", 0) > 0:
            conn.execute(
                self.cache.get("event/update.sql"),
                (
                    event["study_id"],
                    event["patient_id"],
                    event["date"],
                    event["event_type"],
                    event["description"],
                    event["comments"],
                    event["id"]
                )
            )
        else:
            cur = conn.execute(
                self.cache.get("event/save.sql"),
                (
                    event["study_id"],
                    event["patient_id"],
                    event["date"],
                    event["event_type"],
                    event["description"],
                    event["comments"]
                )
            )
            # Since save.sql uses RETURNING id, we fetch it
            result = cur.fetchone()
            if result:
                event["id"] = result[0]
            cur.close()
        conn.commit()
        return event

    def _delete(self, event_id: int) -> None:
        conn = get_connection()
        conn.execute(
            self.cache.get("event/delete.sql"),
            (event_id,)
        )
        conn.commit()

    def _delete_by_study_id(self, study_id: int) -> None:
        conn = get_connection()
        conn.execute(
            self.cache.get("event/delete_by_study_id.sql"),
            (study_id,)
        )
        conn.commit()

    async def get(self, event_id: int) -> dict | None:
        return await asyncio.to_thread(self._get_by_id, event_id)

    async def get_by_study_and_patient(self, study_id: int, patient_id: int) -> List[dict]:
        return await asyncio.to_thread(self._get_by_study_and_patient, study_id, patient_id)

    async def save(self, event: dict) -> dict:
        return await asyncio.to_thread(self._save, event)

    async def delete(self, event_id: int) -> None:
        await asyncio.to_thread(self._delete, event_id)

    async def delete_by_study_id(self, study_id: int) -> None:
        await asyncio.to_thread(self._delete_by_study_id, study_id)
