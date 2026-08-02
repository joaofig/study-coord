import builtins

from src.dtos.monitoring import MonitoringDTO
from src.repositories.postgres.base import PostgresRepository

TABLE = "monitoring"


class MonitoringRepository(PostgresRepository):
    def __init__(self):
        super().__init__()

    async def load(self, monitoring_id: int) -> MonitoringDTO | None:
        sql = "SELECT * FROM monitoring WHERE monitoring_id = %s"
        result = await self.execute_query(sql, (monitoring_id,))
        if result:
            return MonitoringDTO.from_dict(result[0])
        return None

    async def list(self, study_id: int) -> builtins.list[MonitoringDTO]:
        sql = "SELECT * FROM monitoring WHERE study_id = %s"
        result = await self.execute_query(sql, (study_id,))
        return [MonitoringDTO.from_dict(m) for m in result]

    async def save(self, monitoring: MonitoringDTO) -> dict:
        insert = """
        INSERT INTO monitoring (study_id, meeting_date, monitor, comments, 
                                created_at, created_by, updated_at, updated_by) 
        VALUES (%(study_id)s, %(meeting_date)s, %(monitor)s, %(comments)s, 
                %(created_at)s, %(created_by)s, %(updated_at)s, %(updated_by)s)
        """
        update = """
        UPDATE monitoring SET study_id = %(study_id)s, meeting_date = %(meeting_date)s, monitor = %(monitor)s, 
                              comments = %(comments)s, created_at = %(created_at)s, created_by = %(created_by)s, 
                              updated_at = %(updated_at)s, updated_by = %(updated_by)s
        WHERE monitoring_id = %(monitoring_id)s
        """
        return await self.insert_or_update(insert, update, monitoring.to_dict())

    async def delete(self, *, monitoring_id: int = 0, study_id: int = 0) -> None:
        if monitoring_id:
            sql = "DELETE FROM monitoring WHERE monitoring_id = %s"
            await self.execute_query(sql, (monitoring_id,))
        elif study_id:
            sql = "DELETE FROM monitoring WHERE study_id = %s"
            await self.execute_query(sql, (study_id,))
