import asyncio
from typing import List

from db import get_connection
from src.db import SQLCache


class ProtocolRepository:
    def __init__(self):
        self.cache = SQLCache()

    def _get_by_id(self, protocol_id: int) -> dict | None:
        conn = get_connection()
        conn.row_factory = lambda _, row: {
            "id": row[0],
            "study_id": row[1],
            "title": row[2],
            "date": row[3],
            "description": row[4],
        }
        cursor = conn.execute(self.cache.get("protocol/get_by_id.sql"), (protocol_id,))
        return cursor.fetchone()

    def _get_by_study_id(self, study_id: int) -> List[dict]:
        conn = get_connection()
        conn.row_factory = lambda _, row: {
            "id": row[0],
            "study_id": row[1],
            "title": row[2],
            "date": row[3],
            "description": row[4],
        }
        cursor = conn.execute(self.cache.get("protocol/get_by_study_id.sql"), (study_id,))
        return cursor.fetchall()

    def _save(self, protocol: dict) -> dict:
        conn = get_connection()
        if protocol.get("id", 0) > 0:
            conn.execute(
                self.cache.get("protocol/update.sql"),
                (protocol["study_id"], protocol["title"], protocol["date"], protocol["description"], protocol["id"])
            )

        else:
            cur = conn.execute(
                self.cache.get("protocol/save.sql"),
                (protocol["study_id"], protocol["title"], protocol["date"], protocol["description"])
            )
            protocol["id"] = cur.lastrowid
            cur.close()
        conn.commit()
        return protocol

    def _delete(self, protocol_id: int) -> None:
        conn = get_connection()
        conn.execute(
            self.cache.get("protocol/delete.sql"),
            (protocol_id,)
        )
        conn.commit()

    def _delete_by_study_id(self, study_id: int) -> None:
        conn = get_connection()
        conn.execute(
            self.cache.get("protocol/delete_by_study_id.sql"),
            (study_id,)
        )
        conn.commit()

    async def get(self, protocol_id: int) -> dict | None:
        return await asyncio.to_thread(self._get_by_id, protocol_id)

    async def get_by_study_id(self, study_id: int) -> List[dict]:
        return await asyncio.to_thread(self._get_by_study_id, study_id)

    async def save(self, protocol: dict) -> dict:
        return await asyncio.to_thread(self._save, protocol)

    async def delete(self, protocol_id: int) -> None:
        await asyncio.to_thread(self._delete, protocol_id)

    async def delete_by_study_id(self, study_id: int) -> None:
        await asyncio.to_thread(self._delete_by_study_id, study_id)
