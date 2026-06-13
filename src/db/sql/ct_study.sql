CREATE TABLE IF NOT EXISTS study (
    id              INTEGER PRIMARY KEY,
    name            TEXT NOT NULL,
    sponsor         TEXT,
    location_id     INTEGER NOT NULL,
    start_date      TEXT NOT NULL,
    end_date        TEXT,
    protocol_visits INTEGER NOT NULL DEFAULT 0  -- Number of patient visits in the protocol
);
