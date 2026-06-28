INSERT INTO researcher
    (number, name, phone, email, comments)
VALUES
    (?, ?, ?, ?, ?)
RETURNING id;
