import os
from typing import Any

from src.repositories.supabase.EventRepository import EventRepoSupabase
from src.repositories.supabase.PatientRepository import PatientRepoSupabase
from src.repositories.supabase.StudyRepository import StudyRepoSupabase
from src.tools import singleton

DATABASE_ENV_VAR = "DATABASE"
SUPABASE = "supabase"
POSTGRES = "postgres"
SQLITE = "sqlite"


@singleton
class RepositoryHub:
    def __init__(self):
        self.database_type = os.getenv(DATABASE_ENV_VAR, SUPABASE)
        self._study_repository_factories = {
            SUPABASE: StudyRepoSupabase,
        }
        self._patient_repository_factories = {
            SUPABASE: PatientRepoSupabase,
        }
        self._event_repository_factories = {
            SUPABASE: EventRepoSupabase,
        }

    def get_study_repository(self) -> Any:
        repository_factory = self._study_repository_factories.get(self.database_type)

        if repository_factory is None:
            raise ValueError(f"Invalid database type: {self.database_type}")

        return repository_factory()

    def get_patient_repository(self) -> Any:
        repository_factory = self._patient_repository_factories.get(self.database_type)

        if repository_factory is None:
            raise ValueError(f"Invalid database type: {self.database_type}")

        return repository_factory()

    def get_event_repository(self) -> Any:
        repository_factory = self._event_repository_factories.get(self.database_type)

        if repository_factory is None:
            raise ValueError(f"Invalid database type: {self.database_type}")

        return repository_factory()
