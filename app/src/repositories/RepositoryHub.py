import os
from typing import Any

from dotenv import load_dotenv

from src.repositories.supabase.Monitoring import MonitoringRepoSupabase
from src.repositories.supabase.Event import EventRepoSupabase
from src.repositories.supabase.Patient import PatientRepoSupabase
from src.repositories.supabase.Study import StudyRepoSupabase
from src.tools import singleton

DATABASE_ENV_VAR = "DATABASE"


@singleton
class RepositoryHub:
    def __init__(self):
        load_dotenv()
        self.database_type = os.getenv(DATABASE_ENV_VAR, "local")

    def get_study_repository(self) -> Any:
        match self.database_type:
            case "supabase":
                return StudyRepoSupabase()
            case _:
                raise ValueError(f"Invalid database type: {self.database_type}")

    def get_patient_repository(self) -> Any:
        match self.database_type:
            case "supabase":
                return PatientRepoSupabase()
            case _:
                raise ValueError(f"Invalid database type: {self.database_type}")

    def get_event_repository(self) -> Any:
        match self.database_type:
            case "supabase":
                return EventRepoSupabase()
            case _:
                raise ValueError(f"Invalid database type: {self.database_type}")

    def get_monitoring_repository(self) -> Any:
        match self.database_type:
            case "supabase":
                return MonitoringRepoSupabase()
            case _:
                raise ValueError(f"Invalid database type: {self.database_type}")
