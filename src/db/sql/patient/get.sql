SELECT      p.id
,           p.study_id
,           s.name
,           s.sponsor
,           p.number
,           p.start_date
,           p.exit_date
,           p.status
,           p.comments
FROM        patient p
INNER JOIN  study s ON p.study_id = s.id
WHERE       p.id = ?;