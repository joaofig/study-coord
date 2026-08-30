import builtins

from src.dtos.researcher import ResearcherStudyDTO
from src.repositories.postgres.base import PostgresRepository


class ResearcherStudyRepository(PostgresRepository):
    def __init__(self):
        super().__init__()

    async def list(self, researcher_id: int) -> builtins.list[ResearcherStudyDTO]:
        sql = """
              SELECT sr.sr_id, 
                     sr.study_id, 
                     sr.researcher_id,
                     s.protocol,
                     s.name, 
                     s.sponsor, 
                     s.start_date, 
                     s.end_date
              FROM study_researcher sr 
                       INNER JOIN study s ON sr.study_id = s.study_id
              WHERE sr.researcher_id = %s;
              """
        result = await self.execute_query(sql, (researcher_id,))
        return [ResearcherStudyDTO.from_dict(sr) for sr in result]
