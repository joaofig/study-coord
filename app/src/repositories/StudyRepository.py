from abc import abstractmethod, ABC
from typing import List


class StudyRepository(ABC):

    @abstractmethod
    async def list(self) -> List[dict]:
        return []

    @abstractmethod
    async def get(self, study_id: int) -> dict | None:
        return None

    @abstractmethod
    async def save(self, study: dict) -> dict:
        return {}

    @abstractmethod
    async def delete(self, study_id: int) -> None:
        return None
