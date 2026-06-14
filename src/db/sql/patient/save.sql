INSERT INTO patient (id, study_id, number, start_date, end_date, status, comments)
VALUES (?, ?, ?, ?, ?, ?, ?)
ON CONFLICT (id)
DO UPDATE SET
    study_id = excluded.study_id
,   number = excluded.number
,   start_date = excluded.start_date
,   end_date = excluded.end_date
,   status = excluded.status
,   comments = excluded.comments;

