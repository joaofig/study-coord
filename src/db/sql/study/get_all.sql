SELECT  s.id
,       s.name
,       s.sponsor
,       s.start_date
,       s.end_date
,       (SELECT count(0) FROM patient p WHERE p.study_id = s.id) AS num_patients
,       (SELECT count(0) FROM study_researcher sr WHERE sr.study_id = s.id) AS num_researchers
FROM    study s
