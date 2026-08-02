import builtins
from typing import LiteralString

from src.dtos.study import StudyDTO, StudyRowDTO
from src.repositories.postgres.base import PostgresRepository


class StudyRepository(PostgresRepository):
    def __init__(self):
        super().__init__()

    async def study_exists(self, name: str) -> bool:
        sql: LiteralString = """
        SELECT  study_id
        FROM    study
        WHERE   name = %s
        """
        result = await self.execute_query(sql, (name,))
        return bool(result)

    async def list(self) -> builtins.list[StudyRowDTO]:
        # We are reading from a view, not a table
        sql: LiteralString = """
            SELECT  study_id, name, sponsor, start_date, end_date, protocol_visits, comments,
                    ( SELECT count(0) AS count
                           FROM patient p
                          WHERE p.study_id = s.study_id) AS patients,
                    ( SELECT count(0) AS count
                           FROM visit v
                          WHERE v.study_id = s.study_id) AS visits,
                    ( SELECT count(0) AS count
                           FROM study_researcher sr
                          WHERE sr.study_id = s.study_id) AS researchers,
                    ( SELECT count(0) AS count
                           FROM adverse_event ae
                          WHERE ae.study_id = s.study_id) AS events
            FROM study s;
        """
        result = await self.execute_query(sql)
        return [StudyRowDTO.from_dict(s) for s in result]

    async def load(self, study_id: int) -> StudyDTO | None:
        sql: LiteralString = """
        SELECT  study_id
        ,       name
        ,       sponsor
        ,       start_date
        ,       end_date
        ,       protocol_visits
        ,       comments
        ,       created_at
        ,       created_by
        ,       updated_at
        ,       updated_by
        FROM    study
        WHERE   study_id = %s
        """
        result = await self.execute_query(sql, (study_id,))
        if result:
            return StudyDTO.from_dict(result[0])
        return None

    async def save(self, study: StudyDTO) -> dict:
        insert: LiteralString = """
        INSERT INTO study (name, sponsor, start_date, end_date, protocol_visits, comments, 
                           created_at, created_by, updated_at, updated_by) 
        VALUES (%(name)s, %(sponsor)s, %(start_date)s, %(end_date)s, %(protocol_visits)s, %(comments)s, 
                %(created_at)s, %(created_by)s, %(updated_at)s, %(updated_by)s)
        RETURNING study_id
        """
        update: LiteralString = """
        UPDATE study 
        SET     name = %(name)s, 
                sponsor = %(sponsor)s, 
                start_date = %(start_date)s, 
                end_date = %(end_date)s, 
                protocol_visits = %(protocol_visits)s, 
                comments = %(comments)s, 
                updated_at = %(updated_at)s, 
                updated_by = %(updated_by)s
        WHERE   study_id = %(study_id)s
        """
        return await self.insert_or_update(insert, update, study.to_dict())

    async def delete(self, study_id: int) -> None:
        sql: LiteralString = """
        DELETE FROM study where study_id=%s
        """
        await self.execute_query(sql, (study_id,))
