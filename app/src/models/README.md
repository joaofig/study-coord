# Models

This folder contains the models for the application. 
The models are used to represent the data in the application, and also contain the associated business logic.

Models in this folder act as services that orchestrate data operations between ViewModels and Repositories. For data exchange between layers, the application uses DTOs located in the `app/src/dtos` directory.

## Available Models

### Study Management
- **StudyModel** (`study.py`): The primary service for managing clinical study metadata. It handles saving, loading, listing, and basic validation (e.g., checking for unique study names) for studies.
- **ProtocolModel** (`protocol.py`): Manages protocol-related events and violations within a study.
- **MonitoringModel** (`monitorization.py`): Handles the recording and management of monitoring visits and logs.
- **TimelineModel** (`timeline.py`): An aggregator model that builds a chronological view of a study's progress by collecting milestones from patients, visits, protocols, and adverse events.

### Participant & Event Tracking
- **PatientModel** (`patient.py`): Manages patient enrollment, status updates, and ensures patient number uniqueness within a study.
- **VisitModel** (`visit.py`): Tracks scheduled and completed patient visits.
- **AdverseEventModel** (`adverse_event.py`): Handles the recording and management of adverse events reported for patients.

### Researcher Management
- **ResearcherModel** (`researcher.py`): Manages profile data and contact information for researchers in the system.
- **StudyResearcherModel** (`study_researcher.py`): Orchestrates the association between researchers and the studies they are assigned to, including their specific roles.

### Security & Access
- **UserModel** (`user.py`): Manages application users, account details, roles, and provides authentication services.
