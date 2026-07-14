CREATE TABLE IF NOT EXISTS study_researcher (
    id              INTEGER PRIMARY KEY,
    study_id        INTEGER NOT NULL,
    researcher_id   INTEGER NOT NULL,
    role            TEXT NOT NULL,
    study_comments  TEXT,
    FOREIGN KEY(study_id) REFERENCES study(id),
    FOREIGN KEY(researcher_id) REFERENCES researcher(id)
)