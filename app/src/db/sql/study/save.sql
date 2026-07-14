INSERT INTO study (name, sponsor, start_date, end_date, protocol_visits, comments)
VALUES (?, ?, ?, ?, ?, ?)
RETURNING id;
