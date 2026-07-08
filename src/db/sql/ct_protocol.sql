CREATE TABLE IF NOT EXISTS protocol (
    id          INTEGER PRIMARY KEY,
    study_id    INTEGER,
    title       TEXT NOT NULL,
    date        TEXT,
    description TEXT,
    FOREIGN KEY (study_id) REFERENCES study(id)
);
