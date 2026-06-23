CREATE TABLE IF NOT EXISTS researcher (
    id          INTEGER PRIMARY KEY,
    number      TEXT NOT NULL,
    name        TEXT,
    comments    TEXT,
    role        TEXT
);