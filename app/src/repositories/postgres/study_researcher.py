import builtins

from src.dtos.researcher import StudyResearcherDTO, StudyResearcherRow
from src.repositories.postgres.base import PostgresRepository

TABLE = "study_researcher"


class StudyResearcherRepository(PostgresRepository):
    def __init__(self):
        super().__init__()

    async def load(self, sr_id: int) -> StudyResearcherDTO | None:
        sql = f'SELECT * FROM "{TABLE}" WHERE sr_id = %s'
        result = await self.execute_query(sql, (sr_id,))
        if result:
            return StudyResearcherDTO.from_dict(result[0])
        return None

    async def list(self, study_id: int) -> builtins.list[StudyResearcherRow]:
        sql = 'SELECT * FROM "study_researcher_list" WHERE study_id = %s'
        result = await self.execute_query(sql, (study_id,))
        return [StudyResearcherRow.from_dict(sr) for sr in result]

    async def delete(self, researcher_id: int) -> None:
        sql = f'DELETE FROM "{TABLE}" WHERE researcher_id = %s'
        await self.execute_query(sql, (researcher_id,))

    async def save(self, sr: StudyResearcherDTO) -> None:
        await self.insert_or_update(TABLE, sr.to_dict())

    async def delete_by_study(self, study_id: int) -> None:
        sql = f'DELETE FROM "{TABLE}" WHERE study_id = %s'
        await self.execute_query(sql, (study_id,))
