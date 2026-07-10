SELECT  r.id
,       r.number
,       r.name
,       r.phone
,       r.email
,       r.comments
,       (SELECT COUNT(study_id) from study_researcher where researcher_id = r.id) as study_count
FROM    researcher r
WHERE   r.id=?