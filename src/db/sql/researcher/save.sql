INSERT INTO researcher (id, number, name)
VALUES (?, ?, ?)
ON CONFLICT (id)
DO UPDATE SET
    number = excluded.number,
    name = excluded.name;
