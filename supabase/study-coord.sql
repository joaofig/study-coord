CREATE TABLE IF NOT EXISTS monitoring (
    id          INTEGER PRIMARY KEY,
    study_id    INTEGER NOT NULL,
    date        TEXT NOT NULL,
    monitor     TEXT NOT NULL,
    comments    TEXT,
    FOREIGN KEY(study_id) REFERENCES study(id)
);

CREATE TABLE IF NOT EXISTS patient (
    id          INTEGER PRIMARY KEY,
    study_id    INTEGER,
    number      TEXT NOT NULL,
    name        TEXT,
    start_date  TEXT,
    exit_date   TEXT,
    status      TEXT,
    comments    TEXT,
    FOREIGN KEY (study_id) REFERENCES study(id)
);

CREATE TABLE IF NOT EXISTS protocol (
    id          INTEGER PRIMARY KEY,
    study_id    INTEGER NOT NULL,
    title       TEXT NOT NULL,
    date        TEXT,
    description TEXT,
    FOREIGN KEY (study_id) REFERENCES study(id)
);

CREATE TABLE IF NOT EXISTS researcher (
    id          INTEGER PRIMARY KEY,
    number      TEXT NOT NULL,
    name        TEXT,
    phone       TEXT,
    email       TEXT,
    comments    TEXT
);

CREATE TABLE IF NOT EXISTS study_researcher (
    id              INTEGER PRIMARY KEY,
    study_id        INTEGER NOT NULL,
    researcher_id   INTEGER NOT NULL,
    role            TEXT NOT NULL,
    study_comments  TEXT,
    FOREIGN KEY(study_id) REFERENCES study(id),
    FOREIGN KEY(researcher_id) REFERENCES researcher(id)
);

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

CREATE TABLE IF NOT EXISTS event (
    id          INTEGER PRIMARY KEY,
    study_id    INTEGER NOT NULL,
    patient_id  INTEGER NOT NULL,
    date        TEXT NOT NULL,
    event_type  TEXT NOT NULL,
    description TEXT NOT NULL,
    comments    TEXT,
    FOREIGN KEY(study_id) REFERENCES study(id),
    FOREIGN KEY(patient_id) REFERENCES patient(id)
);


CREATE INDEX IF NOT EXISTS patient_study_idx on patient (study_id);
CREATE INDEX IF NOT EXISTS protocol_study_idx ON visit (study_id);
CREATE INDEX IF NOT EXISTS researcher_number_idx on researcher(number);
CREATE INDEX IF NOT EXISTS study_researcher_study_idx ON study_researcher(study_id);
CREATE INDEX IF NOT EXISTS visit_patient_idx ON visit (patient_id);
CREATE INDEX IF NOT EXISTS visit_study_idx ON visit (study_id);


GRANT SELECT, INSERT, UPDATE, DELETE ON public.event to anon;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.monitoring to anon;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.patient to anon;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.protocol to anon;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.researcher to anon;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.study to anon;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.study_researcher to anon;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.visit to anon;


