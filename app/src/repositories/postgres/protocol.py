import builtins

from src.dtos.protocol import ProtocolDTO
from src.repositories.postgres.base import PostgresRepository

TABLE = "protocol"


class ProtocolRepository(PostgresRepository):
    def __init__(self):
        super().__init__()

    async def load(self, protocol_id: int) -> ProtocolDTO | None:
        sql = "SELECT * FROM protocol WHERE protocol_id = %s"
        result = await self.execute_query(sql, (protocol_id,))
        if result:
            return ProtocolDTO.from_dict(result[0])
        return None

    async def list(self, study_id: int) -> builtins.list[ProtocolDTO]:
        sql = "SELECT * FROM protocol WHERE study_id = %s"
        result = await self.execute_query(sql, (study_id,))
        return [ProtocolDTO.from_dict(p) for p in result]

    async def save(self, protocol: ProtocolDTO) -> dict:
        insert = """
        INSERT INTO protocol (study_id, title, event_date, description,
                              created_at, created_by, updated_at, updated_by) 
        VALUES (%(study_id)s, %(title)s, %(event_date)s, %(description)s, 
                %(created_at)s, %(created_by)s, %(updated_at)s, %(updated_by)s)
        """
        update = """
        UPDATE protocol SET study_id = %(study_id)s, title = %(title)s, event_date = %(event_date)s, 
                            description = %(description)s, 
                            updated_at = %(updated_at)s, updated_by = %(updated_by)s
        WHERE protocol_id = %(protocol_id)s
        """
        return await self.insert_or_update(insert, update, protocol.to_dict())

    async def delete(self, *, study_id=0, protocol_id: int = 0) -> None:
        if study_id:
            sql = "DELETE FROM protocol WHERE study_id = %s"
            await self.execute_query(sql, (study_id,))
        else:
            sql = "DELETE FROM protocol WHERE protocol_id = %s"
            await self.execute_query(sql, (protocol_id,))
