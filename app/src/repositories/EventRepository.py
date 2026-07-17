from abc import ABC, abstractmethod


class EventRepository(ABC):

    @abstractmethod
    async def get(self, event_id: int) -> dict | None:
        return {}

    @abstractmethod
    async def get_by_study_and_patient(self, study_id: int, patient_id: int) -> list[dict]:
        return []

    @abstractmethod
    async def save(self, event: dict) -> dict:
        return {}

    @abstractmethod
    async def delete(self, event_id: int) -> None:
        return None

    @abstractmethod
    async def delete_by_study_id(self, study_id: int) -> None:
        return None
