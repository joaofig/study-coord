import builtins

from src.dtos.protocol import ProtocolDTO
from src.repositories.postgres.base import PostgresRepository

TABLE = "protocol"


class ProtocolRepository(PostgresRepository):
    def __init__(self):
        super().__init__()

    async def load(self, protocol_id: int) -> ProtocolDTO | None:
        sql = f'SELECT * FROM "{TABLE}" WHERE protocol_id = %s'
        result = await self.execute_query(sql, (protocol_id,))
        if result:
            return ProtocolDTO.from_dict(result[0])
        return None

    async def list(self, study_id: int) -> builtins.list[ProtocolDTO]:
        sql = f'SELECT * FROM "{TABLE}" WHERE study_id = %s'
        result = await self.execute_query(sql, (study_id,))
        return [ProtocolDTO.from_dict(p) for p in result]

    async def save(self, protocol: ProtocolDTO) -> dict:
        return await self.insert_or_update(TABLE, protocol.to_dict())

    async def delete(self, *, study_id=0, protocol_id: int = 0) -> None:
        if study_id:
            sql = f'DELETE FROM "{TABLE}" WHERE study_id = %s'
            await self.execute_query(sql, (study_id,))
        else:
            sql = f'DELETE FROM "{TABLE}" WHERE protocol_id = %s'
            await self.execute_query(sql, (protocol_id,))
