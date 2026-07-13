CREATE TABLE IF NOT EXISTS patient_history (
    id          INTEGER PRIMARY KEY,
    patient_id  INTEGER NOT NULL,
    study_id    INTEGER,
    timestamp   TEXT NOT NULL,
    
    number      TEXT NOT NULL,
    name        TEXT,
    start_date  TEXT,
    exit_date   TEXT,
    status      TEXT,
    comments    TEXT,
    FOREIGN KEY (study_id) REFERENCES study(id),
    FOREIGN KEY (patient_id) REFERENCES patient(id)
);