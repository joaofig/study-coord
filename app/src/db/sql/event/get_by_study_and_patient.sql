SELECT      e.id,
            e.study_id,
            e.patient_id,
            p.number AS patient_number,
            p.name AS patient_name,
            e.date,
            e.event_type,
            e.description,
            e.comments
FROM        event e
INNER JOIN  patient p ON e.patient_id = p.id
WHERE       e.study_id = ? AND e.patient_id = ?;
