# SQL DML Style and Organization

SQL files are stored in `src/db/sql/<entity>/`. This keeps the database logic separated from the Python code and makes it easy to maintain.

## File Naming Convention

Each entity directory should contain at least:
- `save.sql`: Insert a new record. Use `RETURNING id` if supported and needed.
- `update.sql`: Update an existing record by ID.
- `delete.sql`: Delete a record by ID.
- `get_by_id.sql`: Retrieve a single record by ID, often with JOINs for related data (e.g., patient name).
- `get_by_<parent>_id.sql`: Retrieve a list of records for a specific parent entity (e.g., `get_by_study_id.sql`).

## SQL Coding Style

- **Comma-first**: Start each new column in a SELECT or INSERT with a comma.
- **Table Aliases**: Always use short, descriptive aliases for tables (e.g., `v` for `visit`, `p` for `patient`).
- **Indentation**: Use spaces for indentation, aligning keywords like `FROM`, `INNER JOIN`, `WHERE`.
- **Joins**: Prefer explicit `INNER JOIN` or `LEFT JOIN` over implicit joins.

### Example: `get_by_id.sql`

```sql
SELECT      v.id
,           v.study_id
,           v.patient_id
,           p.number AS patient_number
,           p.name AS patient_name
,           v.visit_date
,           v.visit_type
,           v.comments
FROM        visit v
INNER JOIN  patient p ON v.patient_id = p.id
WHERE       v.id = ?;
```

### Example: `save.sql`

```sql
INSERT INTO visit (
    study_id
,   patient_id
,   visit_date
,   visit_type
,   comments
) VALUES (?, ?, ?, ?, ?)
RETURNING id;
```
