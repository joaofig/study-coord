INSERT INTO researcher
    (number, name, comments, role)
VALUES
    (?, ?, ?, ?)
RETURNING id;
