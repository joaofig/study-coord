import builtins

from src.dtos.adverse_event import AdverseEventDTO
from src.repositories.postgres.base import PostgresRepository

TABLE = "adverse_event"


class AdverseEventRepository(PostgresRepository):
    def __init__(self):
        super().__init__()

    async def load(self, adverse_event_id: int) -> AdverseEventDTO | None:
        sql = f'SELECT * FROM "{TABLE}" WHERE adverse_event_id = %s'
        result = await self.execute_query(sql, (adverse_event_id,))
        if result:
            return AdverseEventDTO.from_dict(result[0])
        return None

    async def list(
        self, *, study_id: int, patient_id: int = 0
    ) -> builtins.list[AdverseEventDTO]:
        if patient_id:
            sql = f'SELECT * FROM "{TABLE}" WHERE study_id = %s AND patient_id = %s'
            result = await self.execute_query(sql, (study_id, patient_id))
        else:
            sql = f'SELECT * FROM "{TABLE}" WHERE study_id = %s'
            result = await self.execute_query(sql, (study_id,))
        return [AdverseEventDTO.from_dict(m) for m in result]

    async def save(self, event: AdverseEventDTO) -> dict:
        return await self.insert_or_update(TABLE, event.to_dict())

    async def delete(self, *, study_id: int = 0, adverse_event_id: int = 0) -> None:
        if study_id:
            sql = f'DELETE FROM "{TABLE}" WHERE study_id = %s'
            await self.execute_query(sql, (study_id,))
        else:
            sql = f'DELETE FROM "{TABLE}" WHERE adverse_event_id = %s'
            await self.execute_query(sql, (adverse_event_id,))
