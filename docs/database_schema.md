# Database Schema

This document describes the current database schema for the `study-coord` application and explains the purpose of each table, relationship, and index.

## Purpose of the Database

The database supports coordination and tracking of clinical or research studies. It stores studies, patients enrolled in studies, researchers participating in studies, visits performed by patients, and adverse events associated with studies.

The schema is centered around the `study` table. Most other records either belong directly to a study or are linked to a study through another entity.

---

## Entity Overview

The current schema contains the following tables:

| Table | Purpose |
|---|---|
| `study` | Stores the main study/protocol information. |
| `patient` | Stores patients enrolled in a study. |
| `researcher` | Stores researcher records. |
| `study_researcher` | Links researchers to studies and records their study-specific role. |
| `visit` | Stores patient visits for a study. |
| `adverse_event` | Stores adverse events reported for a study. |

---

## Tables

## `study`

Stores the main information for each study.

### Columns

| Column | Type | Required | Description |
|---|---:|---:|---|
| `id` | `INTEGER PRIMARY KEY` | Yes | Unique identifier for the study. |
| `name` | `TEXT` | Yes | Study name. |
| `sponsor` | `TEXT` | No | Sponsor of the study. |
| `start_date` | `TEXT` | Yes | Study start date. |
| `end_date` | `TEXT` | No | Study end date, if applicable. |
| `protocol_visits` | `INTEGER` | Yes | Number of planned protocol visits. Defaults to `0`. |
| `comments` | `TEXT` | No | Free-form notes about the study. |

### Purpose

The `study` table is the central table in the schema. Patients, visits, adverse events, and study researcher assignments are connected to a study.

---

## `patient`

Stores patients associated with a study.

### Columns

| Column | Type | Required | Description |
|---|---:|---:|---|
| `id` | `INTEGER PRIMARY KEY` | Yes | Unique identifier for the patient. |
| `study_id` | `INTEGER` | No | Study the patient belongs to. References `study(id)`. |
| `number` | `TEXT` | Yes | Patient number or study-specific patient code. |
| `name` | `TEXT` | No | Patient name. |
| `start_date` | `TEXT` | No | Patient enrollment/start date. |
| `exit_date` | `TEXT` | No | Patient exit date, if applicable. |
| `status` | `TEXT` | No | Current patient status. |
| `comments` | `TEXT` | No | Free-form notes about the patient. |

### Foreign Keys

| Column | References |
|---|---|
| `study_id` | `study(id)` |

### Purpose

The `patient` table tracks participants enrolled in studies. Each patient can optionally be linked to a study.

---

## `researcher`

Stores researcher information.

### Columns

| Column | Type | Required | Description |
|---|---:|---:|---|
| `id` | `INTEGER PRIMARY KEY` | Yes | Unique identifier for the researcher. |
| `number` | `TEXT` | Yes | Researcher number or identifier. |
| `name` | `TEXT` | No | Researcher name. |
| `comments` | `TEXT` | No | Free-form notes about the researcher. |

### Purpose

The `researcher` table stores reusable researcher records. Researchers can be assigned to studies through the `study_researcher` table.

---

## `study_researcher`

Links researchers to studies.

### Columns

| Column | Type | Required | Description |
|---|---:|---:|---|
| `id` | `INTEGER PRIMARY KEY` | Yes | Unique identifier for the study-researcher assignment. |
| `study_id` | `INTEGER` | Yes | Study being assigned to. References `study(id)`. |
| `researcher_id` | `INTEGER` | Yes | Researcher assigned to the study. References `researcher(id)`. |
| `role` | `TEXT` | Yes | Researcher's role in the study. |
| `study_comments` | `TEXT` | No | Study-specific comments about the researcher assignment. |

### Foreign Keys

| Column | References |
|---|---|
| `study_id` | `study(id)` |
| `researcher_id` | `researcher(id)` |

### Purpose

This is a junction table for the many-to-many relationship between studies and researchers.

A study can have many researchers, and a researcher can participate in many studies.

---

## `visit`

Stores visits performed by patients as part of a study.

### Columns

| Column | Type | Required | Description |
|---|---:|---:|---|
| `id` | `INTEGER PRIMARY KEY` | Yes | Unique identifier for the visit. |
| `study_id` | `INTEGER` | Yes | Study associated with the visit. References `study(id)`. |
| `patient_id` | `INTEGER` | Yes | Patient associated with the visit. References `patient(id)`. |
| `visit_date` | `DATE` | Yes | Date of the visit. |
| `visit_type` | `TEXT` | Yes | Type or name of the visit. |
| `comments` | `TEXT` | No | Free-form notes about the visit. |

### Foreign Keys

| Column | References |
|---|---|
| `study_id` | `study(id)` |
| `patient_id` | `patient(id)` |

### Purpose

The `visit` table tracks scheduled or completed visits for patients in a study.

Each visit belongs to both a study and a patient.

---

## `adverse_event`

Stores adverse events related to a study.

### Columns

| Column | Type | Required | Description |
|---|---:|---:|---|
| `id` | `INTEGER PRIMARY KEY` | Yes | Unique identifier for the adverse event. |
| `study_id` | `INTEGER` | Yes | Study associated with the adverse event. References `study(id)`. |
| `date` | `TEXT` | Yes | Date the adverse event occurred or was reported. |
| `event_type` | `TEXT` | Yes | Type/category of adverse event. |
| `description` | `TEXT` | Yes | Description of the adverse event. |
| `comments` | `TEXT` | No | Additional notes. |

### Foreign Keys

| Column | References |
|---|---|
| `study_id` | `study(id)` |

### Purpose

The `adverse_event` table records safety or incident events connected to a study.

Currently, adverse events are linked directly to a study, not to a specific patient.

---

## Indexes

The schema defines the following indexes:

| Index | Table | Column(s) | Purpose |
|---|---|---|---|
| `patient_study_idx` | `patient` | `study_id` | Speeds up loading patients for a study. |
| `researcher_number_idx` | `researcher` | `number` | Speeds up lookup of researchers by researcher number. |
| `visit_patient_idx` | `visit` | `patient_id` | Speeds up loading visits for a patient. |
| `visit_study_idx` | `visit` | `study_id` | Speeds up loading visits for a study. |

---

## Relationships
```
text
study
 ├── patient
 │    └── visit
 ├── visit
 ├── adverse_event
 └── study_researcher
      └── researcher
```
### Relationship Details

| Relationship | Type | Description |
|---|---|---|
| `study` → `patient` | One-to-many | A study can have many patients. |
| `study` → `visit` | One-to-many | A study can have many visits. |
| `patient` → `visit` | One-to-many | A patient can have many visits. |
| `study` → `adverse_event` | One-to-many | A study can have many adverse events. |
| `study` → `study_researcher` | One-to-many | A study can have many researcher assignments. |
| `researcher` → `study_researcher` | One-to-many | A researcher can be assigned to many studies. |
| `study` ↔ `researcher` | Many-to-many | Implemented through `study_researcher`. |

---

## Notes and Observations

### Date Storage

Most date fields are stored as `TEXT`, except `visit.visit_date`, which is declared as `DATE`.

SQLite does not enforce a strict native date type, so date values should be stored consistently, preferably using ISO format:
```
text
YYYY-MM-DD
```
### Optional Patient Study Link

`patient.study_id` is nullable. This means a patient can exist without being assigned to a study.

If every patient must always belong to a study, this column should eventually be changed to:
```
sql
study_id INTEGER NOT NULL
```
### Adverse Events Are Study-Level

The `adverse_event` table currently references only `study(id)`.

If adverse events need to be tracked for individual patients, a future schema update could add:
```
sql
patient_id INTEGER
```
with a foreign key to `patient(id)`.

### Researcher Number Is Indexed But Not Unique

The `researcher.number` column is indexed, but the schema does not currently enforce uniqueness.

If researcher numbers must be unique, consider adding a unique constraint or unique index in a future migration.

---

## Current Schema SQL
```sql
CREATE TABLE IF NOT EXISTS study (
    id              INTEGER PRIMARY KEY,
    name            TEXT NOT NULL,
    sponsor         TEXT,
    start_date      TEXT NOT NULL,
    end_date        TEXT,
    protocol_visits INTEGER NOT NULL DEFAULT 0,
    comments        TEXT
);

CREATE TABLE IF NOT EXISTS patient (
    id          INTEGER PRIMARY KEY,
    study_id    INTEGER,
    number      TEXT NOT NULL,
    name        TEXT,
    start_date  TEXT,
    exit_date   TEXT,
    status      TEXT,
    comments    TEXT,
    FOREIGN KEY (study_id) REFERENCES study(id)
);

CREATE TABLE IF NOT EXISTS researcher (
    id          INTEGER PRIMARY KEY,
    number      TEXT NOT NULL,
    name        TEXT,
    comments    TEXT
);

CREATE TABLE IF NOT EXISTS study_researcher (
    id              INTEGER PRIMARY KEY,
    study_id        INTEGER NOT NULL,
    researcher_id   INTEGER NOT NULL,
    role            TEXT NOT NULL,
    study_comments  TEXT,
    FOREIGN KEY(study_id) REFERENCES study(id),
    FOREIGN KEY(researcher_id) REFERENCES researcher(id)
);

CREATE TABLE IF NOT EXISTS visit (
    id          INTEGER PRIMARY KEY,
    study_id    INTEGER NOT NULL,
    patient_id  INTEGER NOT NULL,
    visit_date  DATE NOT NULL,
    visit_type  TEXT NOT NULL,
    comments    TEXT,
    FOREIGN KEY(study_id) REFERENCES study(id),
    FOREIGN KEY(patient_id) REFERENCES patient(id)
);

CREATE TABLE IF NOT EXISTS adverse_event (
    id          INTEGER PRIMARY KEY,
    study_id    INTEGER NOT NULL,
    date        TEXT NOT NULL,
    event_type  TEXT NOT NULL,
    description TEXT NOT NULL,
    comments    TEXT,
    FOREIGN KEY(study_id) REFERENCES study(id)
);

CREATE INDEX IF NOT EXISTS patient_study_idx ON patient (study_id);

CREATE INDEX IF NOT EXISTS researcher_number_idx ON researcher(number);

CREATE INDEX IF NOT EXISTS visit_patient_idx ON visit (patient_id);

CREATE INDEX IF NOT EXISTS visit_study_idx ON visit (study_id);
```


You can create it from the project root with:

```bash
mkdir -p doc
cat > doc/database-schema.md <<'EOF'
# Database Schema

This document describes the current database schema for the `study-coord` application and explains the purpose of each table, relationship, and index.

See the generated schema documentation content above.
EOF
```
