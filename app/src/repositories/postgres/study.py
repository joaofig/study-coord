import builtins
from src.dtos.study import StudyDTO, StudyRowDTO
from src.repositories.postgres.base import PostgresRepository

TABLE = "study"

class StudyRepository(PostgresRepository):
    def __init__(self):
        super().__init__()

    async def study_exists(self, name: str) -> bool:
        sql = f'SELECT * FROM "{TABLE}" WHERE name = %s'
        result = await self.execute_query(sql, (name,))
        return bool(result)

    async def list(self) -> builtins.list[StudyRowDTO]:
        # We are reading from a view, not a table
        sql = 'SELECT * FROM "study_list"'
        result = await self.execute_query(sql)
        return [StudyRowDTO.from_dict(s) for s in result]

    async def load(self, study_id: int) -> StudyDTO | None:
        sql = f'SELECT * FROM "{TABLE}" WHERE study_id = %s'
        result = await self.execute_query(sql, (study_id,))
        if result:
            return StudyDTO.from_dict(result[0])
        return None

    async def save(self, study: StudyDTO) -> dict:
        return await self.insert_or_update(TABLE, study.to_dict())

    async def delete(self, study_id: int) -> None:
        sql = f'DELETE FROM "{TABLE}" WHERE study_id = %s'
        await self.execute_query(sql, (study_id,))
