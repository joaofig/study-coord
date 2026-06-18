SELECT  s.id
,       s.name
,       s.sponsor
,       s.start_date
,       s.end_date
,       s.protocol_visits
,       s.comments
,       (SELECT count(0) FROM patient p WHERE p.study_id = s.id) AS num_patients
,       (SELECT count(0) FROM study_researcher sr WHERE sr.study_id = s.id) AS num_researchers
,       (SELECT count(0) FROM visit v WHERE v.study_id = s.id) AS num_visits
,       (SELECT count(0) FROM adverse_event ae WHERE ae.study_id = s.id) AS num_adverse_events
FROM    study s
