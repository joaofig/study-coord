SELECT      sr.id
,           sr.study_id
,           sr.researcher_id
,           sr.role
,           sr.study_comments
,           r.number
,           r.name
,           r.phone
,           r.email
FROM        study_researcher sr
INNER JOIN  researcher r on r.id = sr.researcher_id
WHERE       sr.study_id = ?;