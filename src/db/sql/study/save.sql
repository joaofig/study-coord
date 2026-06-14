INSERT INTO study (id, name, sponsor, start_date, end_date)
VALUES (?, ?, ?, ?, ?)
ON CONFLICT (id)
DO UPDATE SET
    name = excluded.name
,   sponsor = excluded.sponsor
,   start_date = excluded.start_date
,   end_date = excluded.end_date;
