from dataclasses import dataclass


@dataclass
class Patient:
    id: int
    study_id: int
    study_name: str
    study_sponsor: str
    number: str
    start_date: str
    exit_date: str
    status: str = "active"
    comments: str = ""