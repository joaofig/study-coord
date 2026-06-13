CREATE TABLE IF NOT EXISTS visit (
    id          INTEGER PRIMARY KEY,
    patient_id  INTEGER NOT NULL,
    visit_date  DATE NOT NULL,
    FOREIGN KEY(patient_id) REFERENCES patient(id)
);