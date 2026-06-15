INSERT INTO researcher (id, name, type)
VALUES (?, ?, ?)
ON CONFLICT (id)
DO UPDATE SET
    name = excluded.name;
