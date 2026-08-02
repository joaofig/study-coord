import builtins
from typing import LiteralString

from src.dtos.adverse_event import AdverseEventDTO
from src.repositories.postgres.base import PostgresRepository


class AdverseEventRepository(PostgresRepository):
    def __init__(self):
        super().__init__()

    async def load(self, adverse_event_id: int) -> AdverseEventDTO | None:
        sql: LiteralString = """
        SELECT  *
        FROM    adverse_event
        WHERE   adverse_event_id = %s"""
        result = await self.execute_query(sql, (adverse_event_id,))
        if result:
            return AdverseEventDTO.from_dict(result[0])
        return None

    async def list(
        self, *, study_id: int, patient_id: int = 0
    ) -> builtins.list[AdverseEventDTO]:
        if patient_id:
            sql = "SELECT * FROM adverse_event WHERE study_id = %s AND patient_id = %s"
            result = await self.execute_query(sql, (study_id, patient_id))
        else:
            sql = "SELECT * FROM adverse_event WHERE study_id = %s"
            result = await self.execute_query(sql, (study_id,))
        return [AdverseEventDTO.from_dict(m) for m in result]

    async def save(self, event: AdverseEventDTO) -> dict:
        insert = """
        INSERT INTO adverse_event (study_id, patient_id, event_date, event_type, description, comments, 
                                   created_at, created_by, updated_at, updated_by) 
        VALUES (%(study_id)s, %(patient_id)s, %(event_date)s, %(event_type)s, %(description)s, %(comments)s, 
                %(created_at)s, %(created_by)s, %(updated_at)s, %(updated_by)s)
        """
        update = """
        UPDATE adverse_event SET
        study_id = %(study_id)s,
        patient_id = %(patient_id)s,
        event_date = %(event_date)s,
        event_type = %(event_type)s,
        description = %(description)s,
        comments = %(comments)s,
        updated_at = %(updated_at)s,
        updated_by = %(updated_by)s
        WHERE adverse_event_id = %(adverse_event_id)s
        """
        return await self.insert_or_update(insert, update, event.to_dict())

    async def delete(self, *, study_id: int = 0, adverse_event_id: int = 0) -> None:
        if study_id:
            sql = "DELETE FROM adverse_event WHERE study_id = %s"
            await self.execute_query(sql, (study_id,))
        else:
            sql = "DELETE FROM adverse_event WHERE adverse_event_id = %s"
            await self.execute_query(sql, (adverse_event_id,))
