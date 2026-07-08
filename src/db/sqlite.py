import sqlite3
from pathlib import Path

from .config import load_database_config


def get_connection(database_path: Path | None = None) -> sqlite3.Connection:
    if database_path is None:
        database_path = load_database_config().path

    database_path.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(str(database_path))


def get_script(script_name: str) -> str:
    path = Path("src/db/sql") / script_name
    return path.read_text(
        encoding="utf-8"
    )


def initialize_database(database_path: Path | None = None) -> None:
    # The `ct` prefix stands for "create table".
    # The `ci` prefix stands for "create index".
    script_files = [
        "ct_study.sql",
        "ct_researcher.sql",
        "ct_patient.sql",
        "ct_study_researcher.sql",
        "ct_visit.sql",
        "ct_event.sql",
        "ct_monitoring.sql",
        "ct_protocol.sql",

        "ci_patient_study.sql",
        "ci_researcher_number.sql",
        "ci_visit_patient.sql",
        "ci_visit_study.sql",
    ]

    with get_connection(database_path) as connection:
        for script_file in script_files:
            connection.execute(
                get_script(script_file)
            )
