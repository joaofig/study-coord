UPDATE visit SET
    study_id = ?,
    patient_id = ?,
    visit_date = ?,
    visit_type = ?,
    comments = ?
WHERE id = ?;
