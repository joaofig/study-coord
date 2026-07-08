SELECT
    id
,   study_id
,   title
,   date
,   description
FROM protocol
WHERE study_id = ?
