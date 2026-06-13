CREATE TABLE IF NOT EXISTS study_researcher (
    id              INTEGER PRIMARY KEY,
    study_id        INTEGER NOT NULL,
    researcher_id   INTEGER NOT NULL,
    start_date      TEXT NOT NULL,
    is_principal    BOOLEAN NOT NULL,
    FOREIGN KEY(study_id) REFERENCES study(id),
    FOREIGN KEY(researcher_id) REFERENCES researcher(id)
)