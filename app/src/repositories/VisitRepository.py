from abc import ABC, abstractmethod
from typing import List


class VisitRepository(ABC):

    @abstractmethod
    async def get(self, visit_id: int) -> dict | None:
        return None

    @abstractmethod
    async def get_by_study_id(self, study_id: int) -> List[dict]:
        return []

    @abstractmethod
    async def get_by_study_id_and_patient_id(self, study_id: int, patient_id: int) -> List[dict]:
        return []

    @abstractmethod
    async def save(self, visit: dict) -> dict:
        return {}

    @abstractmethod
    async def delete(self, visit_id: int) -> None:
        return None

    @abstractmethod
    async def delete_by_study_id(self, study_id: int) -> None:
        return None
