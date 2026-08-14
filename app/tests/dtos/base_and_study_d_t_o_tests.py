from datetime import date, datetime

from src.dtos.adverse_event import AdverseEventDTO
from src.dtos.base import BaseDTO
from src.dtos.milestone import Milestone
from src.dtos.monitorization import MonitorizationDTO
from src.dtos.patient import PatientDTO, patient_status_name
from src.dtos.protocol import ProtocolDTO
from src.dtos.researcher import (
    ResearcherDTO,
    StudyResearcherDTO,
    StudyResearcherRow,
    study_researcher_role_name,
)
from src.dtos.study import StudyDTO, StudyRowDTO
from src.dtos.user import UserDTO, hash_password
from src.dtos.visit import VisitDTO


def test_base_dto_to_dict_serializes_audit_fields():
    dto = BaseDTO(
        created_at=datetime(2024, 1, 1, 10, 30),
        created_by="creator",
        updated_at=datetime(2024, 1, 2, 11, 45),
        updated_by="updater",
    )

    assert dto.to_dict() == {
        "created_at": "2024-01-01T10:30:00",
        "created_by": "creator",
        "updated_at": "2024-01-02T11:45:00",
        "updated_by": "updater",
    }


def test_study_dto_from_dict_and_to_dict():
    dto = StudyDTO.from_dict(
        {
            "id": 10,
            "protocol": "PROT-10",
            "name": "Cardiology Study",
            "sponsor": "Acme Pharma",
            "start_date": "2024-01-01",
            "end_date": "2024-12-31",
            "proto_visits": 6,
            "comments": "Important study",
            "created_at": "2024-01-01T10:00:00",
            "created_by": "admin",
            "updated_at": "2024-01-02T10:00:00",
            "updated_by": "reviewer",
        }
    )

    assert dto.study_id == 10
    assert dto.protocol == "PROT-10"
    assert dto.start_date == date(2024, 1, 1)
    assert dto.end_date == date(2024, 12, 31)
    assert dto.protocol_visits == 6

    assert dto.to_dict() == {
        "study_id": 10,
        "protocol": "PROT-10",
        "name": "Cardiology Study",
        "sponsor": "Acme Pharma",
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "protocol_visits": 6,
        "comments": "Important study",
        "created_at": "2024-01-01T10:00:00",
        "created_by": "admin",
        "updated_at": "2024-01-02T10:00:00",
        "updated_by": "reviewer",
    }


def test_study_row_dto_from_dict_and_to_dict():
    dto = StudyRowDTO.from_dict(
        {
            "id": 11,
            "protocol": "PROT-11",
            "name": "Oncology Study",
            "sponsor": "Health Inc",
            "start_date": "2024-02-01",
            "end_date": "2024-11-30",
            "protocol_visits": 4,
            "comments": "Row comments",
            "patients": 12,
            "visits": 48,
            "researchers": 3,
            "events": 2,
        }
    )

    assert dto.to_dict() == {
        "study_id": 11,
        "protocol": "PROT-11",
        "name": "Oncology Study",
        "sponsor": "Health Inc",
        "start_date": "2024-02-01",
        "end_date": "2024-11-30",
        "protocol_visits": 4,
        "comments": "Row comments",
        "patients": 12,
        "visits": 48,
        "researchers": 3,
        "events": 2,
    }


def test_patient_dto_from_dict_to_dict_and_to_grid():
    dto = PatientDTO.from_dict(
        {
            "patient_id": 20,
            "study_id": 10,
            "number": "P001",
            "name": "Jane Doe",
            "start_date": "2024-03-01",
            "exit_date": "2024-09-01",
            "status": "completed",
            "comments": "Completed protocol",
            "created_at": "2024-03-01T09:00:00",
            "created_by": "admin",
            "updated_at": "2024-09-01T17:00:00",
            "updated_by": "nurse",
        }
    )

    assert dto.start_date == date(2024, 3, 1)
    assert dto.exit_date == date(2024, 9, 1)

    assert dto.to_dict()["status"] == "completed"
    assert dto.to_dict()["exit_date"] == "2024-09-01"

    grid = dto.to_grid()
    assert grid["patient_id"] == 20
    assert grid["status_text"] == "Completed"


def test_patient_status_name_returns_known_and_unknown_labels():
    assert patient_status_name("active") == "Active"
    assert patient_status_name("missing") == "Unknown"


def test_visit_dto_from_dict_and_to_dict():
    dto = VisitDTO.from_dict(
        {
            "visit_id": 30,
            "study_id": 10,
            "patient_id": 20,
            "visit_date": "2024-04-15",
            "visit_type": "screening",
            "comments": "Initial visit",
            "created_at": "2024-04-15T08:00:00",
            "created_by": "admin",
            "updated_at": "2024-04-15T09:00:00",
            "updated_by": "coordinator",
        }
    )

    assert dto.visit_date == date(2024, 4, 15)
    assert dto.to_dict()["visit_date"] == "2024-04-15"
    assert dto.to_dict()["visit_type"] == "screening"


def test_protocol_dto_from_dict_and_to_dict():
    dto = ProtocolDTO.from_dict(
        {
            "protocol_id": 40,
            "study_id": 10,
            "title": "Baseline Assessment",
            "event_date": "2024-05-01",
            "description": "Collect baseline data",
            "created_at": "2024-05-01T08:00:00",
            "created_by": "admin",
            "updated_at": "2024-05-02T08:00:00",
            "updated_by": "reviewer",
        }
    )

    assert dto.event_date == date(2024, 5, 1)
    assert dto.to_dict()["event_date"] == "2024-05-01"


def test_monitoring_dto_from_dict_and_to_dict():
    dto = MonitorizationDTO.from_dict(
        {
            "monitoring_id": 50,
            "study_id": 10,
            "meeting_date": "2024-06-01",
            "monitor": "Monitor One",
            "comments": "No findings",
            "created_at": "2024-06-01T10:00:00",
            "created_by": "admin",
            "updated_at": "2024-06-01T11:00:00",
            "updated_by": "monitor",
        }
    )

    assert dto.meeting_date == date(2024, 6, 1)
    assert dto.to_dict()["meeting_date"] == "2024-06-01"
    assert dto.to_dict()["monitor"] == "Monitor One"


def test_adverse_event_dto_from_dict_and_to_dict():
    dto = AdverseEventDTO.from_dict(
        {
            "selected_id": 60,
            "study_id": 10,
            "patient_id": 20,
            "event_date": "2024-07-01",
            "event_type": "SAE",
            "description": "Serious event",
            "comments": "Reported immediately",
            "patient_number": "P001",
            "patient_name": "Jane Doe",
            "created_at": "2024-07-01T12:00:00",
            "created_by": "admin",
            "updated_at": "2024-07-01T13:00:00",
            "updated_by": "doctor",
        }
    )

    assert dto.adverse_event_id == 60
    assert dto.event_date == date(2024, 7, 1)
    assert dto.to_dict()["selected_id"] == 60
    assert dto.to_dict()["patient_number"] == "P001"


def test_researcher_dto_from_dict_and_to_dict():
    dto = ResearcherDTO.from_dict(
        {
            "id": 70,
            "number": "R001",
            "name": "Dr Smith",
            "phone": "555-0100",
            "email": "smith@example.com",
            "comments": "Principal investigator",
            "study_count": 2,
            "created_at": "2024-08-01T08:00:00",
            "created_by": "admin",
            "updated_at": "2024-08-01T09:00:00",
            "updated_by": "admin",
        }
    )

    assert dto.researcher_id == 70
    assert dto.study_count == 2
    assert dto.to_dict()["email"] == "smith@example.com"


def test_study_researcher_row_from_dict_and_to_dict():
    dto = StudyResearcherRow.from_dict(
        {
            "id": 80,
            "study_id": 10,
            "researcher_id": 70,
            "role": "principal",
            "study_comments": "Lead researcher",
            "number": "R001",
            "name": "Dr Smith",
            "phone": "555-0100",
            "email": "smith@example.com",
        }
    )

    data = dto.to_dict()

    assert data["sr_id"] == 80
    assert data["role"] == "principal"
    assert data["role_text"] == "Principal Researcher"


def test_study_researcher_dto_from_dict_and_to_dict():
    dto = StudyResearcherDTO.from_dict(
        {
            "id": 90,
            "study_id": 10,
            "researcher_id": 70,
            "role": "standard",
            "study_comments": "Sub-investigator",
            "created_at": "2024-09-01T10:00:00",
            "created_by": "admin",
            "updated_at": "2024-09-01T11:00:00",
            "updated_by": "admin",
        }
    )

    assert dto.sr_id == 90
    assert dto.role == "standard"
    assert dto.to_dict()["study_comments"] == "Sub-investigator"


def test_study_researcher_role_name_returns_known_and_unknown_labels():
    assert study_researcher_role_name("standard") == "Standard Researcher"
    assert study_researcher_role_name("principal") == "Principal Researcher"
    assert study_researcher_role_name("missing") == "Unknown"


def test_user_dto_from_dict_and_to_dict():
    dto = UserDTO.from_dict(
        {
            "user_id": 100,
            "user_name": "admin",
            "pass_hash": "hashed",
            "user_role": "administrator",
            "change_pass": True,
            "created_at": "2024-10-01T08:00:00",
            "created_by": "system",
            "updated_at": "2024-10-01T09:00:00",
            "updated_by": "system",
        }
    )

    assert dto.user_id == 100
    assert dto.change_pass is True
    assert dto.to_dict()["user_name"] == "admin"


def test_hash_password_returns_sha256_hash():
    assert (
        hash_password("secret")
        == "2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b"
    )


def test_milestone_to_dict():
    milestone = Milestone(
        event_title="First Visit",
        event_date=date(2024, 11, 1),
        event_icon="event",
        description="Patient first visit",
        color="blue",
    )

    assert milestone.to_dict() == {
        "title": "First Visit",
        "subtitle": "2024-11-01",
        "icon": "event",
        "description": "Patient first visit",
        "color": "blue",
    }
