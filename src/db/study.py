from pathlib import Path

from models.study import Study
from .sqlite import get_connection


def get_all_studies(database_path: Path | None = None) -> list[Study]:
    with get_connection(database_path) as conn:
        conn.row_factory = lambda _, row: Study(
            id=row[0],
            name=row[1],
            sponsor=row[2],
            location_id=row[3],
            start_date=row[4],
        )
        cursor = conn.execute(
            "SELECT id, name, sponsor, location_id, start_date FROM study ORDER BY name"
        )
        return cursor.fetchall()


def get_study(study_id: int, database_path: Path | None = None) -> Study | None:
    with get_connection(database_path) as conn:
        conn.row_factory = lambda _, row: Study(
            id=row[0],
            name=row[1],
            sponsor=row[2],
            location_id=row[3],
            start_date=row[4],
        )
        cursor = conn.execute(
            "SELECT id, name, sponsor, location_id, start_date FROM study WHERE id = ?",
            (study_id,),
        )
        return cursor.fetchone()


def create_study(study: Study, database_path: Path | None = None) -> Study:
    with get_connection(database_path) as conn:
        cursor = conn.execute(
            "INSERT INTO study (name, sponsor, location_id, start_date) VALUES (?, ?, ?, ?)",
            (study.name, study.sponsor, study.location_id, study.start_date),
        )
        return Study(
            id=cursor.lastrowid,
            name=study.name,
            sponsor=study.sponsor,
            location_id=study.location_id,
            start_date=study.start_date,
        )


def update_study(study: Study, database_path: Path | None = None) -> None:
    with get_connection(database_path) as conn:
        conn.execute(
            "UPDATE study SET name = ?, sponsor = ?, location_id = ?, start_date = ? WHERE id = ?",
            (study.name, study.sponsor, study.location_id, study.start_date, study.id),
        )


def delete_study(study_id: int, database_path: Path | None = None) -> None:
    with get_connection(database_path) as conn:
        conn.execute("DELETE FROM study WHERE id = ?", (study_id,))
