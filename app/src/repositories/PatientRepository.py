from abc import ABC, abstractmethod
from typing import List


class PatientRepository(ABC):

    @abstractmethod
    async def get(self, patient_id: int) -> dict | None:
        return None

    @abstractmethod
    async def load_from_study(self, study_id: int) -> List[dict]:
        return []

    @abstractmethod
    async def save(self, patient: dict) -> dict:
        return {}

    @abstractmethod
    async def delete(self, patient_id: int) -> None:
        return None

    @abstractmethod
    async def delete_by_study_id(self, study_id: int) -> None:
        return None
