INSERT INTO visit
    (study_id, patient_id, visit_date, visit_type, comments)
VALUES
    (?, ?, ?, ?, ?)
RETURNING id;
