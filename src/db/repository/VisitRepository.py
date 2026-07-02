from typing import List

from db import SQLCache, get_connection


class VisitRepository:
    def __init__(self):
        self.cache = SQLCache()

    def _get_by_id(self, visit_id: int) -> dict | None:
        conn = get_connection()
        conn.row_factory = lambda _, row: {
            "id": row[0],
            "study_id": row[1],
            "patient_id": row[2],
            "patient_number": row[3],
            "patient_name": row[4],
            "visit_date": row[5],
            "visit_type": row[6],
            "comments": row[7]
        }
        cursor = conn.execute(self.cache.get("visit/get_by_id.sql"), (visit_id,))
        return cursor.fetchone()

    def _get_by_study_id(self, study_id: int) -> List[dict] | None:
        conn = get_connection()
        conn.row_factory = lambda _, row: {
            "id": row[0],
            "study_id": row[1],
            "patient_id": row[2],
            "patient_number": row[3],
            "patient_name": row[4],
            "visit_date": row[5],
            "visit_type": row[6],
            "comments": row[7]
        }
        cursor = conn.execute(self.cache.get("visit/get_by_study_id.sql"), (study_id,))
        return cursor.fetchall()

    def _save(self, visit: dict) -> dict:
        conn = get_connection()
        if visit.get("id", 0) > 0:
            conn.execute(
                self.cache.get("visit/update.sql"),
                (visit["study_id"], visit["patient_id"], visit["visit_date"], visit["visit_type"], visit["comments"], visit["id"])
            )

        else:
            cur = conn.execute(
                self.cache.get("visit/save.sql"),
                (visit["study_id"], visit["patient_id"], visit["visit_date"], visit["visit_type"], visit["comments"])
            )
            visit["id"] = cur.lastrowid
            cur.close()
        conn.commit()
        return visit

    def _delete(self, visit_id: int) -> None:
        conn = get_connection()
        conn.execute(
            self.cache.get("visit/delete.sql"),
            (visit_id,)
        )
        conn.commit()
