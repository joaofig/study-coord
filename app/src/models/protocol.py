from dataclasses import dataclass
from typing import List

from src.db.repository.ProtocolRepository import ProtocolRepository


@dataclass
class Protocol:
    id: int = 0
    study_id: int = 0
    title: str = ""
    date: str = ""
    description: str = ""

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "study_id": self.study_id,
            "title": self.title,
            "date": self.date,
            "description": self.description,
        }

    async def save(self):
        repo = ProtocolRepository()
        result = await repo.save(self.to_dict())
        self.id = result["id"]

    @classmethod
    async def load(cls, protocol_id: int) -> 'Protocol':
        repo = ProtocolRepository()
        protocol = await repo.get(protocol_id)
        if protocol:
            return Protocol(**protocol)
        return None

class ProtocolList:
    protocols: list[Protocol] = []

    async def load_from_study(self, study_id: int) -> List[Protocol]:
        repo = ProtocolRepository()
        self.protocols = [Protocol(**p) for p in await repo.get_by_study_id(study_id)]
        return self.protocols

    @classmethod
    async def delete(cls, protocol_id: int):
        repo = ProtocolRepository()
        await repo.delete(protocol_id)
