INSERT INTO study_researcher
    (study_id, researcher_id, role, study_comments)
VALUES
    (?, ?, ?, ?)
RETURNING id;