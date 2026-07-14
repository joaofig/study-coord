SELECT      p.id
,           p.study_id
,           p.number
,           p.name
,           p.start_date
,           p.exit_date
,           p.status
,           p.comments
FROM        patient p
ORDER BY    p.number;