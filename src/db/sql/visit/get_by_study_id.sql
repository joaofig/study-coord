SELECT      v.id,
            v.study_id,
            v.patient_id,
            p.number AS patient_number,
            p.name AS patient_name,
            v.visit_date,
            v.visit_type,
            v.comments
FROM        visit v
INNER JOIN  patient p ON v.patient_id = p.id
WHERE       v.study_id = ?;
