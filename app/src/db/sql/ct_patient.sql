CREATE TABLE IF NOT EXISTS patient (
    id          INTEGER PRIMARY KEY,
    study_id    INTEGER,
    number      TEXT NOT NULL,
    name        TEXT,
    start_date  TEXT,
    exit_date   TEXT,
    status      TEXT,
    comments    TEXT,
    FOREIGN KEY (study_id) REFERENCES study(id)
);