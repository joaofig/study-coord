import builtins

from src.dtos.researcher import ResearcherDTO
from src.repositories.postgres.base import PostgresRepository

TABLE = "researcher"


class ResearcherRepository(PostgresRepository):
    def __init__(self):
        super().__init__()

    async def number_exists(self, number: str) -> bool:
        sql = f'SELECT * FROM "{TABLE}" WHERE "number" = %s'
        result = await self.execute_query(sql, (number,))
        return bool(result)

    async def load(self, researcher_id: int) -> ResearcherDTO | None:
        sql = f'SELECT * FROM "{TABLE}" WHERE researcher_id = %s'
        result = await self.execute_query(sql, (researcher_id,))
        if result:
            return ResearcherDTO.from_dict(result[0])
        return None

    async def save(self, researcher: ResearcherDTO) -> dict:
        d = researcher.to_dict()
        del d["study_count"]
        return await self.insert_or_update(TABLE, d)

    async def delete(self, researcher_id: int):
        sql = f'DELETE FROM "{TABLE}" WHERE researcher_id = %s'
        await self.execute_query(sql, (researcher_id,))

    async def list(self) -> builtins.list[ResearcherDTO]:
        sql = 'SELECT * FROM "researcher_list"'
        result = await self.execute_query(sql)
        return [ResearcherDTO.from_dict(r) for r in result]
