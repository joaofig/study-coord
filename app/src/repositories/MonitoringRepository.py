from abc import ABC, abstractmethod


class MonitoringRepository(ABC):

    @abstractmethod
    async def get(self, monitoring_id: int) -> dict | None:
        return {}

    @abstractmethod
    async def get_by_study_id(self, study_id: int) -> list[dict]:
        return []

    @abstractmethod
    async def save(self, monitoring: dict) -> dict:
        return {}

    @abstractmethod
    async def delete(self, monitoring_id: int) -> None:
        pass

    @abstractmethod
    async def delete_by_study_id(self, study_id: int) -> None:
        pass
