CREATE TABLE IF NOT EXISTS screening (
    id          INTEGER PRIMARY KEY,
    patient_id  INTEGER NOT NULL,
    status      TEXT,
    date        TEXT,
    comment     TEXT,
    FOREIGN KEY (patient_id) REFERENCES patient(id)
);