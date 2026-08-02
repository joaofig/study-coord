import builtins

from src.dtos.researcher import StudyResearcherDTO, StudyResearcherRow
from src.repositories.postgres.base import PostgresRepository


class StudyResearcherRepository(PostgresRepository):
    def __init__(self):
        super().__init__()

    async def load(self, sr_id: int) -> StudyResearcherDTO | None:
        sql = "SELECT * FROM study_researcher WHERE sr_id = %s"
        result = await self.execute_query(sql, (sr_id,))
        if result:
            return StudyResearcherDTO.from_dict(result[0])
        return None

    async def list(self, study_id: int) -> builtins.list[StudyResearcherRow]:
        sql = """
        SELECT  sr.sr_id, sr.study_id, sr.researcher_id,
                r.number, r.name, r.phone, r.email,
                sr.role, sr.study_comments,
                sr.created_at, sr.created_by, sr.updated_at, sr.updated_by
        FROM study_researcher sr JOIN researcher r ON sr.researcher_id = r.researcher_id;
        """
        result = await self.execute_query(sql, (study_id,))
        return [StudyResearcherRow.from_dict(sr) for sr in result]

    async def delete(self, researcher_id: int) -> None:
        sql = "DELETE FROM study_researcher WHERE researcher_id = %s"
        await self.execute_query(sql, (researcher_id,))

    async def save(self, sr: StudyResearcherDTO) -> None:
        insert = """
        INSERT INTO study_researcher (
            study_id, researcher_id, role, study_comments,
            created_at, created_by, updated_at, updated_by
        ) VALUES (
            %(study_id)s, %(researcher_id)s, %(role)s, %(study_comments)s,
            %(created_at)s, %(created_by)s, %(updated_at)s, %(updated_by)s
        )
        """
        update = """
        UPDATE study_researcher SET
            study_id = %(study_id)s, researcher_id = %(researcher_id)s,
            role = %(role)s, study_comments = %(study_comments)s,
            created_at = %(created_at)s, created_by = %(created_by)s,
            updated_at = %(updated_at)s, updated_by = %(updated_by)s
        WHERE sr_id = %(sr_id)s
        """
        await self.insert_or_update(insert, update, sr.to_dict())

    async def delete_by_study(self, study_id: int) -> None:
        sql = "DELETE FROM study_researcher WHERE study_id = %s"
        await self.execute_query(sql, (study_id,))
