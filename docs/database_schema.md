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
| `protocol` | Stores protocol events or milestones for a study. |
| `monitoring` | Stores monitoring visits for a study. |
| `adverse_event` | Stores adverse events reported for a study and patient. |
| `user` | Stores user accounts and authentication information. |

---

## Tables

## `study`

Stores the main information for each study.

### Columns

| Column | Type | Required | Description |
|---|---:|---:|---|
| `study_id` | `bigint PRIMARY KEY` | Yes | Unique identifier for the study (identity). |
| `name` | `character varying(128)` | Yes | Study name. Defaults to empty string. |
| `sponsor` | `character varying(128)` | Yes | Sponsor of the study. Defaults to empty string. |
| `start_date` | `date` | Yes | Study start date. Defaults to `now()`. |
| `end_date` | `date` | No | Study end date, if applicable. |
| `protocol_visits` | `integer` | Yes | Number of planned protocol visits. Defaults to `0`. |
| `comments` | `text` | No | Free-form notes about the study. Defaults to empty string. |
| `created_at` | `timestamp` | Yes | Record creation timestamp. |
| `created_by` | `character varying(64)` | Yes | User who created the record. |
| `updated_at` | `timestamp` | Yes | Record last update timestamp. |
| `updated_by` | `character varying(64)` | Yes | User who last updated the record. |

### Purpose

The `study` table is the central table in the schema. Patients, visits, adverse events, and study researcher assignments are connected to a study.

---

## `patient`

Stores patients associated with a study.

### Columns

| Column | Type | Required | Description |
|---|---:|---:|---|
| `patient_id` | `bigint PRIMARY KEY` | Yes | Unique identifier for the patient (identity). |
| `study_id` | `bigint` | No | Study the patient belongs to. References `study(study_id)`. |
| `number` | `text` | Yes | Patient number or study-specific patient code. |
| `name` | `text` | No | Patient name. |
| `start_date` | `text` | No | Patient enrollment/start date. |
| `exit_date` | `text` | No | Patient exit date, if applicable. |
| `status` | `text` | No | Current patient status. |
| `comments` | `text` | No | Free-form notes about the patient. |
| `created_at` | `timestamp` | Yes | Record creation timestamp. |
| `created_by` | `character varying(64)` | Yes | User who created the record. |
| `updated_at` | `timestamp` | Yes | Record last update timestamp. |
| `updated_by` | `character varying(64)` | Yes | User who last updated the record. |

### Foreign Keys

| Column | References |
|---|---|
| `study_id` | `study(study_id)` |

### Purpose

The `patient` table tracks participants enrolled in studies. Each patient can optionally be linked to a study.

---

## `researcher`

Stores researcher information.

### Columns

| Column | Type | Required | Description |
|---|---:|---:|---|
| `researcher_id` | `bigint PRIMARY KEY` | Yes | Unique identifier for the researcher (identity). |
| `number` | `character varying(64)` | Yes | Researcher number or identifier. |
| `name` | `character varying(128)` | No | Researcher name. |
| `phone` | `character varying(64)` | No | Researcher phone number. |
| `email` | `character varying(128)` | No | Researcher email address. |
| `comments` | `text` | No | Free-form notes about the researcher. |
| `created_at` | `timestamp` | Yes | Record creation timestamp. |
| `created_by` | `character varying(64)` | Yes | User who created the record. |
| `updated_at` | `timestamp` | Yes | Record last update timestamp. |
| `updated_by` | `character varying(64)` | Yes | User who last updated the record. |

### Purpose

The `researcher` table stores reusable researcher records. Researchers can be assigned to studies through the `study_researcher` table.

---

## `study_researcher`

Links researchers to studies.

### Columns

| Column | Type | Required | Description |
|---|---:|---:|---|
| `sr_id` | `bigint PRIMARY KEY` | Yes | Unique identifier for the assignment (identity). |
| `study_id` | `bigint` | Yes | Study being assigned to. References `study(study_id)`. |
| `researcher_id` | `bigint` | Yes | Researcher assigned to the study. References `researcher(researcher_id)`. |
| `role` | `character varying(64)` | Yes | Researcher's role in the study. |
| `study_comments` | `text` | No | Study-specific comments about the researcher assignment. |
| `created_at` | `timestamp` | Yes | Record creation timestamp. |
| `created_by` | `character varying(64)` | Yes | User who created the record. |
| `updated_at` | `timestamp` | Yes | Record last update timestamp. |
| `updated_by` | `character varying(64)` | Yes | User who last updated the record. |

### Foreign Keys

| Column | References |
|---|---|
| `study_id` | `study(study_id)` |
| `researcher_id` | `researcher(researcher_id)` |

### Purpose

This is a junction table for the many-to-many relationship between studies and researchers.

A study can have many researchers, and a researcher can participate in many studies.

---

## `visit`

Stores visits performed by patients as part of a study.

### Columns

| Column | Type | Required | Description |
|---|---:|---:|---|
| `visit_id` | `bigint PRIMARY KEY` | Yes | Unique identifier for the visit (identity). |
| `study_id` | `bigint` | Yes | Study associated with the visit. References `study(study_id)`. |
| `patient_id` | `bigint` | Yes | Patient associated with the visit. References `patient(patient_id)`. |
| `visit_date` | `date` | Yes | Date of the visit. |
| `visit_type` | `character varying(128)` | Yes | Type or name of the visit. |
| `comments` | `text` | No | Free-form notes about the visit. |
| `created_at` | `timestamp` | Yes | Record creation timestamp. |
| `created_by` | `character varying(64)` | Yes | User who created the record. |
| `updated_at` | `timestamp` | Yes | Record last update timestamp. |
| `updated_by` | `character varying(64)` | Yes | User who last updated the record. |

### Foreign Keys

| Column | References |
|---|---|
| `study_id` | `study(study_id)` |
| `patient_id` | `patient(patient_id)` |

### Purpose

The `visit` table tracks scheduled or completed visits for patients in a study.

Each visit belongs to both a study and a patient.

---

## `protocol`

Stores protocol events or milestones for a study.

### Columns

| Column | Type | Required | Description |
|---|---:|---:|---|
| `protocol_id` | `bigint PRIMARY KEY` | Yes | Unique identifier for the protocol entry (identity). |
| `study_id` | `bigint` | Yes | Study associated with the protocol entry. References `study(study_id)`. |
| `title` | `text` | Yes | Title of the protocol event. |
| `event_date` | `timestamp with time zone` | Yes | Date and time of the event. |
| `description` | `text` | No | Description of the event. |
| `created_at` | `timestamp` | Yes | Record creation timestamp. |
| `created_by` | `character varying(64)` | Yes | User who created the record. |
| `updated_at` | `timestamp` | Yes | Record last update timestamp. |
| `updated_by` | `character varying(64)` | Yes | User who last updated the record. |

### Foreign Keys

| Column | References |
|---|---|
| `study_id` | `study(study_id)` |

---

## `monitoring`

Stores monitoring visits for a study.

### Columns

| Column | Type | Required | Description |
|---|---:|---:|---|
| `monitoring_id` | `bigint PRIMARY KEY` | Yes | Unique identifier for the monitoring visit (identity). |
| `study_id` | `bigint` | Yes | Study associated with the monitoring visit. References `study(study_id)`. |
| `meeting_date` | `date` | Yes | Date of the monitoring visit. |
| `monitor` | `character varying(128)` | Yes | Name of the monitor. |
| `comments` | `text` | No | Free-form notes about the monitoring visit. |
| `created_at` | `timestamp` | Yes | Record creation timestamp. |
| `created_by` | `character varying(64)` | Yes | User who created the record. |
| `updated_at` | `timestamp` | Yes | Record last update timestamp. |
| `updated_by` | `character varying(64)` | Yes | User who last updated the record. |

### Foreign Keys

| Column | References |
|---|---|
| `study_id` | `study(study_id)` |

### Purpose

The `monitoring` table tracks visits performed by monitors to ensure study compliance.

---

## `adverse_event`

Stores adverse events related to a study and patient.

### Columns

| Column | Type | Required | Description |
|---|---:|---:|---|
| `adverse_event_id` | `bigint PRIMARY KEY` | Yes | Unique identifier for the adverse event (identity). |
| `study_id` | `integer` | Yes | Study associated with the adverse event. References `study(study_id)`. |
| `patient_id` | `bigint` | Yes | Patient associated with the adverse event. References `patient(patient_id)`. |
| `event_date` | `date` | Yes | Date the adverse event occurred or was reported. |
| `event_type` | `character varying(64)` | Yes | Type/category of adverse event. |
| `description` | `character varying(256)` | Yes | Description of the adverse event. |
| `comments` | `text` | No | Additional notes. |
| `created_at` | `timestamp` | Yes | Record creation timestamp. |
| `created_by` | `character varying(64)` | Yes | User who created the record. |
| `updated_at` | `timestamp` | Yes | Record last update timestamp. |
| `updated_by` | `character varying(64)` | Yes | User who last updated the record. |

### Foreign Keys

| Column | References |
|---|---|
| `study_id` | `study(study_id)` |
| `patient_id` | `patient(patient_id)` |

### Purpose

The `adverse_event` table records safety or incident events connected to a study and a specific patient.

---

## `user`

Stores user accounts and authentication information.

### Columns

| Column | Type | Required | Description |
|---|---:|---:|---|
| `user_id` | `bigint PRIMARY KEY` | Yes | Unique identifier for the user (identity). |
| `user_name` | `character varying(64)` | Yes | Username for login. |
| `pass_hash` | `character varying(256)` | Yes | Hashed password. |
| `user_role` | `character varying(64)` | Yes | User's role (e.g., admin, researcher). |
| `change_pass` | `boolean` | Yes | Flag indicating if the user must change their password. Defaults to `false`. |
| `created_at` | `timestamp` | Yes | Record creation timestamp. |
| `created_by` | `character varying(64)` | Yes | User who created the record. |
| `updated_at` | `timestamp` | Yes | Record last update timestamp. |
| `updated_by` | `character varying(64)` | Yes | User who last updated the record. |

### Purpose

The `user` table stores authentication and authorization details for the application users.

---

## Indexes

The schema defines the following indexes:

| Index | Table | Column(s) | Purpose |
|---|---|---|---|
| `patient_study_idx` | `patient` | `study_id` | Speeds up loading patients for a study. |
| `researcher_number_idx` | `researcher` | `number` | Speeds up lookup of researchers by researcher number. |
| `study_researcher_study_idx` | `study_researcher` | `study_id` | Speeds up loading researchers for a study. |
| `visit_patient_idx` | `visit` | `patient_id` | Speeds up loading visits for a patient. |
| `visit_study_idx` | `visit` | `study_id` | Speeds up loading visits for a study. |

---

## Relationships
```
text
study
 ├── patient
 │    ├── visit
 │    └── adverse_event
 ├── visit
 ├── protocol
 ├── monitoring
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
| `study` → `protocol` | One-to-many | A study can have many protocol events. |
| `study` → `monitoring` | One-to-many | A study can have many monitoring visits. |
| `study` → `adverse_event` | One-to-many | A study can have many adverse events. |
| `patient` → `adverse_event` | One-to-many | An adverse event is linked to a specific patient. |
| `study` → `study_researcher` | One-to-many | A study can have many researcher assignments. |
| `researcher` → `study_researcher` | One-to-many | A researcher can be assigned to many studies. |
| `study` ↔ `researcher` | Many-to-many | Implemented through `study_researcher`. |

---

## Notes and Observations

### Date Storage

Dates are stored using Postgres `date` or `timestamp` types. Timestamps are generally stored without time zone, except for `protocol.event_date`.

### Audit Columns

All tables include the following audit columns:
- `created_at`: `timestamp` (defaults to `now()`)
- `created_by`: `character varying(64)`
- `updated_at`: `timestamp` (defaults to `now()`)
- `updated_by`: `character varying(64)`

### Views

The schema includes views to simplify data access:
- `study_list`: Provides a summary of studies including counts of patients, visits, researchers, and events.
- `study_researcher_list`: Joins `study_researcher` with `researcher` to provide full researcher details for each assignment.

---

## Current Schema SQL

```sql
--
-- Table: public.study
--
CREATE TABLE IF NOT EXISTS public.study
(
    study_id bigint NOT NULL GENERATED BY DEFAULT AS IDENTITY,
    name character varying(128) NOT NULL DEFAULT '',
    sponsor character varying(128) NOT NULL DEFAULT '',
    start_date date NOT NULL DEFAULT now(),
    end_date date,
    protocol_visits integer NOT NULL DEFAULT 0,
    comments text DEFAULT '',
    created_at timestamp without time zone NOT NULL DEFAULT now(),
    created_by character varying(64) NOT NULL,
    updated_at timestamp without time zone NOT NULL DEFAULT now(),
    updated_by character varying(64) NOT NULL,
    CONSTRAINT study_pkey PRIMARY KEY (study_id)
);

--
-- Table: public.patient
--
CREATE TABLE IF NOT EXISTS public.patient
(
    patient_id bigint NOT NULL GENERATED BY DEFAULT AS IDENTITY,
    study_id bigint,
    "number" text NOT NULL,
    name text,
    start_date text,
    exit_date text,
    status text,
    comments text,
    created_at timestamp without time zone NOT NULL DEFAULT now(),
    created_by character varying(64) NOT NULL,
    updated_at timestamp without time zone NOT NULL DEFAULT now(),
    updated_by character varying(64) NOT NULL,
    CONSTRAINT patient_pkey PRIMARY KEY (patient_id)
);

--
-- Table: public.researcher
--
CREATE TABLE IF NOT EXISTS public.researcher
(
    researcher_id bigint NOT NULL GENERATED BY DEFAULT AS IDENTITY,
    "number" character varying(64) NOT NULL,
    name character varying(128),
    phone character varying(64),
    email character varying(128),
    comments text,
    created_at timestamp without time zone NOT NULL DEFAULT now(),
    created_by character varying(64) NOT NULL,
    updated_at timestamp without time zone NOT NULL DEFAULT now(),
    updated_by character varying(64) NOT NULL,
    CONSTRAINT researcher_pkey PRIMARY KEY (researcher_id)
);

--
-- Table: public.study_researcher
--
CREATE TABLE IF NOT EXISTS public.study_researcher
(
    sr_id bigint NOT NULL GENERATED BY DEFAULT AS IDENTITY,
    study_id bigint NOT NULL,
    researcher_id bigint NOT NULL,
    role character varying(64) NOT NULL,
    study_comments text,
    created_at timestamp without time zone NOT NULL DEFAULT now(),
    created_by character varying(64) NOT NULL,
    updated_at timestamp without time zone NOT NULL DEFAULT now(),
    updated_by character varying(64) NOT NULL,
    CONSTRAINT study_researcher_pkey PRIMARY KEY (sr_id)
);

--
-- Table: public.adverse_event
--
CREATE TABLE IF NOT EXISTS public.adverse_event
(
    adverse_event_id bigint NOT NULL GENERATED BY DEFAULT AS IDENTITY,
    study_id integer NOT NULL,
    patient_id bigint NOT NULL,
    event_date date NOT NULL DEFAULT now(),
    event_type character varying(64) NOT NULL,
    description character varying(256) NOT NULL,
    comments text,
    created_at timestamp without time zone NOT NULL DEFAULT now(),
    created_by character varying(64) NOT NULL,
    updated_at timestamp without time zone NOT NULL DEFAULT now(),
    updated_by character varying(64) NOT NULL,
    CONSTRAINT event_pkey PRIMARY KEY (adverse_event_id),
    CONSTRAINT event_patient_id_fkey FOREIGN KEY (patient_id)
        REFERENCES public.patient (patient_id)
);

--
-- Table: public.visit
--
CREATE TABLE IF NOT EXISTS public.visit
(
    visit_id bigint NOT NULL GENERATED BY DEFAULT AS IDENTITY,
    study_id bigint NOT NULL,
    patient_id bigint NOT NULL,
    visit_date date NOT NULL,
    visit_type character varying(128) NOT NULL,
    comments text,
    created_at timestamp without time zone NOT NULL DEFAULT now(),
    created_by character varying(64) NOT NULL,
    updated_at timestamp without time zone NOT NULL DEFAULT now(),
    updated_by character varying(64) NOT NULL,
    CONSTRAINT visit_pkey PRIMARY KEY (visit_id),
    CONSTRAINT visit_patient_id_fkey FOREIGN KEY (patient_id)
        REFERENCES public.patient (patient_id)
);

--
-- Table: public.protocol
--
CREATE TABLE IF NOT EXISTS public.protocol
(
    protocol_id bigint NOT NULL GENERATED BY DEFAULT AS IDENTITY,
    study_id bigint NOT NULL,
    title text NOT NULL,
    event_date timestamp with time zone NOT NULL,
    description text,
    created_at timestamp without time zone NOT NULL DEFAULT now(),
    created_by character varying(64) NOT NULL,
    updated_at timestamp without time zone NOT NULL DEFAULT now(),
    updated_by character varying(64) NOT NULL,
    CONSTRAINT protocol_pkey PRIMARY KEY (protocol_id)
);

--
-- Table: public.monitoring
--
CREATE TABLE IF NOT EXISTS public.monitoring
(
    monitoring_id bigint NOT NULL GENERATED BY DEFAULT AS IDENTITY,
    study_id bigint NOT NULL,
    meeting_date date NOT NULL,
    monitor character varying(128) NOT NULL,
    comments text,
    created_at timestamp without time zone NOT NULL DEFAULT now(),
    created_by character varying(64) NOT NULL,
    updated_at timestamp without time zone NOT NULL DEFAULT now(),
    updated_by character varying(64) NOT NULL,
    CONSTRAINT monitoring_pkey PRIMARY KEY (monitoring_id)
);

--
-- Table: public.user
--
CREATE TABLE IF NOT EXISTS public."user"
(
    user_id bigint NOT NULL GENERATED BY DEFAULT AS IDENTITY,
    user_name character varying(64) NOT NULL,
    pass_hash character varying(256) NOT NULL,
    user_role character varying(64) NOT NULL,
    change_pass boolean NOT NULL DEFAULT false,
    created_at timestamp without time zone NOT NULL DEFAULT now(),
    created_by character varying(64) NOT NULL,
    updated_at timestamp without time zone NOT NULL DEFAULT now(),
    updated_by character varying(64) NOT NULL,
    CONSTRAINT user_pkey PRIMARY KEY (user_id)
);

--
-- Indexes
--
CREATE INDEX IF NOT EXISTS patient_study_idx ON public.patient (study_id);
CREATE INDEX IF NOT EXISTS researcher_number_idx ON public.researcher (number);
CREATE INDEX IF NOT EXISTS study_researcher_study_idx ON public.study_researcher (study_id);
CREATE INDEX IF NOT EXISTS visit_patient_idx ON public.visit (patient_id);
CREATE INDEX IF NOT EXISTS visit_study_idx ON public.visit (study_id);
```

