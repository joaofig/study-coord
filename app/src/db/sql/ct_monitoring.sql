CREATE TABLE IF NOT EXISTS monitoring (
    id          INTEGER PRIMARY KEY,
    study_id    INTEGER NOT NULL,
    date        TEXT NOT NULL,
    monitor     TEXT NOT NULL,
    comments    TEXT,
    FOREIGN KEY(study_id) REFERENCES study(id)
);