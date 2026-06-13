import sqlite3
from pathlib import Path

from .config import load_database_config


def get_connection(database_path: Path | None = None) -> sqlite3.Connection:
    if database_path is None:
        database_path = load_database_config().path

    database_path.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(str(database_path))


def initialize_database(database_path: Path | None = None) -> None:
    with get_connection(database_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS location (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                address_1 TEXT,
                address_2 TEXT
            )
            """
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS researcher (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                location_id INTEGER NOT NULL,
                FOREIGN KEY (location_id) REFERENCES location (id)
            )
            """
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS study (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                sponsor TEXT,
                location_id INTEGER NOT NULL,
                start_date TEXT NOT NULL,
                FOREIGN KEY (location_id) REFERENCES location (id)
            )
            """
        )
