# Data Transfer Objects (DTOs)

This folder contains data transfer objects (DTOs) used for data exchange between different components of the application. 
DTOs are lightweight objects that carry data between layers of an application, such as between the view and the view model, or between the view model and the repository.

## Available DTOs

### Base DTO
- **BaseDTO** (`base.py`): The base class for most DTOs in the system. It provides standard audit fields: `created_at`, `created_by`, `updated_at`, and `updated_by`.

### User Management
- **UserDTO** (`user.py`): Transfers user information, including credentials (`user_name`, `pass_hash`), `user_role`, and account status flags.

### Study Management
- **StudyDTO** (`study.py`): Represents core clinical study data, including `protocol` identifier, `name`, `sponsor`, and scheduled dates.
- **StudyRowDTO** (`study.py`): Optimized for grid displays, providing a summary of a study along with aggregated counts of patients, visits, researchers, and events.
- **ProtocolDTO** (`protocol.py`): Tracks protocol-related events or version updates for a study.
- **MonitoringDTO** (`monitoring.py`): Records monitoring visits or meetings, including the `meeting_date` and `monitor` details.

### Patient & Visit Tracking
- **PatientDTO** (`patient.py`): Captures patient enrollment details, including their `number`, `name`, and current `status` (Active, Completed, Withdrawn, etc.).
- **VisitDTO** (`visit.py`): Represents a patient visit within a study, tracking the `visit_date` and `visit_type`.
- **AdverseEventDTO** (`adverse_event.py`): Transports data regarding reported adverse events, linking them to specific patients and studies.

### Researcher Management
- **ResearcherDTO** (`researcher.py`): Contains contact information and profile details for researchers.
- **StudyResearcherDTO** / **StudyResearcherRow** (`researcher.py`): Manages the association between researchers and studies, defining their specific `role` (Standard or Principal Researcher).

### UI Helpers
- **Milestone** (`milestone.py`): A lightweight object used for UI components like timelines to represent significant events with titles, icons, and colors.