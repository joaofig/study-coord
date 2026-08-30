# ViewModels

This folder contains the ViewModel objects that form the core of the application's MVVM (Model-View-ViewModel) architecture. ViewModels act as an intermediary between the UI (Views) and the data orchestration layer (Models), managing state, handling user actions, and facilitating communication via a decoupled messenger system.

## Base Architecture
- **ViewModel** (`view_model.py`): The abstract base class for all ViewModels. It provides a centralized messaging system (`broadcast`, `subscribe`) for cross-component communication and standardized methods for property management (`get`, `set`) and UI-triggered actions (`call`).

## Study & Protocol Management
- **Study Management**:
    - `StudyViewModel` (`study.py`): Manages the state and validation for creating or editing individual clinical studies.
    - `StudyListViewModel` (`study_list.py`): Manages the master list of all studies, handling data loading into `GridList` and selection logic.
- **Protocol Management**:
    - `ProtocolViewModel` (`protocol.py`): Handles study-specific protocol data and version tracking.
    - `ProtocolListViewModel` (`protocol_list.py`): Manages the collection of protocols associated with a specific study.

## Participant & Clinical Event Management
- **Patient Tracking**:
    - `PatientViewModel` (`patient.py`): Manages enrollment details, status updates, and demographic information for study participants.
    - `PatientListViewModel` (`patient_list.py`): Handles the display and selection of patients within a study.
- **Clinical Visits**:
    - `VisitViewModel` (`visit.py`): Records individual patient visits, including date and type tracking.
    - `VisitListViewModel` (`visit_list.py`): Manages the history of visits, with filtering by study and patient.
- **Safety Reporting**:
    - `AdverseEventViewModel` (`adverse_event.py`): Documents reported safety incidents and adverse events for trial participants.
    - `AdverseEventListViewModel` (`adverse_event_list.py`): Manages the collection of adverse events for monitoring and review.

## Staff & Role Management
- **Researcher Directory**:
    - `ResearcherViewModel` (`researcher/researcher.py`): Manages global profiles and contact information for clinical staff.
    - `ResearcherListViewModel` (`researcher/researcher_list.py`): Displays the directory of all researchers in the system.
- **Study Assignments**:
    - `StudyResearcherViewModel` (`study_researcher.py`): Manages the specific assignment of a researcher to a study, including role definitions.
    - `StudyResearcherListViewModel` (`study_researcher_list.py`): Shows the team of researchers assigned to a particular study.

## Oversight & Reporting
- **Site Monitoring**:
    - `MonitorizationViewModel` (`monitorization.py`): Tracks individual site monitoring visits and compliance reviews.
    - `MonitoringListViewModel` (`monitorization_list.py`): Manages the log of monitoring activities for a study.
- **Dashboard & Visualization**:
    - `ReportViewModel` (`report.py`): Aggregates key performance indicators (KPIs) and counts for dashboarding and high-level oversight.
    - `TimelineViewModel` (`timeline.py`): Generates a chronological view of study milestones, collecting data from across the system for visualization.

## System Administration
- **User & Security**:
    - `UserViewModel` (`user.py`): Manages application user accounts, role assignments, and secure password handling.
    - `UserListViewModel` (`user_list.py`): Handles the administrative list of all application users.
    - `ApiKeyListViewModel` (`api_key_list.py`): Manages API keys, including user-specific key listing, selection, and deletion.
- **Database Management**:
    - `SQLViewModel` (`sql.py`): Manages direct database SQL query execution, handling query state, schema structure, error messages, and tabular result data.
