INSERT INTO event (
    study_id
,   patient_id
,   date
,   event_type
,   description
,   comments
) VALUES (?, ?, ?, ?, ?, ?)
RETURNING id;
