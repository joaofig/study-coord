CREATE TABLE IF NOT EXISTS adverse_event (
    id          INTEGER PRIMARY KEY,
    study_id    INTEGER NOT NULL,
    date        TEXT NOT NULL,
    event_type  TEXT NOT NULL,
    description TEXT NOT NULL,
    comments    TEXT,
    FOREIGN KEY(study_id) REFERENCES study(id)
);