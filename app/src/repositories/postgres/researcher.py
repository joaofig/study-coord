import builtins

from src.dtos.researcher import ResearcherDTO
from src.repositories.postgres.base import PostgresRepository

TABLE = "researcher"


class ResearcherRepository(PostgresRepository):
    def __init__(self):
        super().__init__()

    async def number_exists(self, number: str) -> bool:
        sql = "SELECT * FROM researcher WHERE number=%s"
        result = await self.execute_query(sql, (number,))
        return bool(result)

    async def load(self, researcher_id: int) -> ResearcherDTO | None:
        sql = "SELECT * FROM researcher WHERE researcher_id=%s"
        result = await self.execute_query(sql, (researcher_id,))
        if result:
            return ResearcherDTO.from_dict(result[0])
        return None

    async def save(self, researcher: ResearcherDTO) -> dict:
        insert = """
        INSERT INTO researcher (number, name, phone, email, comments, created_at, created_by, updated_at, updated_by)
            VALUES (%(number)s, %(name)s, %(phone)s, %(email)s, %(comments)s, 
                    %(created_at)s, %(created_by)s, %(updated_at)s, %(updated_by)s)
        """
        update = """
        UPDATE researcher SET number = %(number)s, name = %(name)s, phone = %(phone)s, email = %(email)s, 
                              comments = %(comments)s, 
                              updated_at = %(updated_at)s, updated_by = %(updated_by)s
        WHERE researcher_id=%(researcher_id)s
        """
        return await self.insert_or_update(insert, update, researcher.to_dict())

    async def delete(self, researcher_id: int):
        sql = "DELETE FROM researcher WHERE researcher_id=%s"
        await self.execute_query(sql, (researcher_id,))

    async def list(self) -> builtins.list[ResearcherDTO]:
        sql = """
        SELECT  researcher_id, number, name, phone, email, comments,
                ( SELECT count(0) AS count
                       FROM study_researcher sr
                      WHERE sr.researcher_id = r.researcher_id) AS study_count,
                created_at, created_by, updated_at, updated_by
                FROM researcher r;
        """
        result = await self.execute_query(sql)
        return [ResearcherDTO.from_dict(r) for r in result]
