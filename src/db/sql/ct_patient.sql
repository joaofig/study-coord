CREATE TABLE IF NOT EXISTS patient (
    id          INTEGER PRIMARY KEY,
    study_id    INTEGER,
    name        TEXT,
    start_date  TEXT,
    status      TEXT,
    FOREIGN KEY (study_id) REFERENCES study(id)
);