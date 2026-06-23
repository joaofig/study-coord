INSERT INTO researcher
    (number, name, comments)
VALUES
    (?, ?, ?)
RETURNING id;
