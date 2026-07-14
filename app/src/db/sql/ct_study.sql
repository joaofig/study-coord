CREATE TABLE IF NOT EXISTS study (
    id              INTEGER PRIMARY KEY,
    name            TEXT NOT NULL,
    sponsor         TEXT,
    start_date      TEXT NOT NULL,
    end_date        TEXT,
    protocol_visits INTEGER NOT NULL DEFAULT 0,
    comments        TEXT
);
