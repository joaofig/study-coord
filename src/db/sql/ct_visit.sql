CREATE TABLE IF NOT EXISTS visit (
    id          INTEGER PRIMARY KEY,
    study_id    INTEGER NOT NULL,
    patient_id  INTEGER NOT NULL,
    visit_date  DATE NOT NULL,
    visit_type  TEXT NOT NULL,
    comments    TEXT,
    FOREIGN KEY(study_id) REFERENCES study(id),
    FOREIGN KEY(patient_id) REFERENCES patient(id)
);