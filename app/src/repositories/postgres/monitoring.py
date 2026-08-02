import builtins

from src.dtos.monitoring import MonitoringDTO
from src.repositories.postgres.base import PostgresRepository

TABLE = "monitoring"


class MonitoringRepository(PostgresRepository):
    def __init__(self):
        super().__init__()

    async def load(self, monitoring_id: int) -> MonitoringDTO | None:
        sql = f'SELECT * FROM "{TABLE}" WHERE monitoring_id = %s'
        result = await self.execute_query(sql, (monitoring_id,))
        if result:
            return MonitoringDTO.from_dict(result[0])
        return None

    async def list(self, study_id: int) -> builtins.list[MonitoringDTO]:
        sql = f'SELECT * FROM "{TABLE}" WHERE study_id = %s'
        result = await self.execute_query(sql, (study_id,))
        return [MonitoringDTO.from_dict(m) for m in result]

    async def save(self, monitoring: MonitoringDTO) -> dict:
        return await self.insert_or_update(TABLE, monitoring.to_dict())

    async def delete(self, *, monitoring_id: int = 0, study_id: int = 0) -> None:
        if monitoring_id:
            sql = f'DELETE FROM "{TABLE}" WHERE monitoring_id = %s'
            await self.execute_query(sql, (monitoring_id,))
        elif study_id:
            sql = f'DELETE FROM "{TABLE}" WHERE study_id = %s'
            await self.execute_query(sql, (study_id,))
