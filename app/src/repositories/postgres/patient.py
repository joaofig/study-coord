import builtins
from typing import LiteralString

from src.dtos.patient import PatientDTO
from src.repositories.postgres.base import PostgresRepository


class PatientRepository(PostgresRepository):
    def __init__(self):
        super().__init__()

    async def patient_number_exists(self, study_id: int, patient_number: str) -> bool:
        sql: LiteralString = """
        SELECT  patient_id
        FROM    patient 
        WHERE   study_id = %s AND "number" = %s
        """
        result = await self.execute_query(sql, (study_id, patient_number))
        return len(result) > 0

    async def load(self, patient_id: int) -> PatientDTO | None:
        sql: LiteralString = """
        SELECT  *
        FROM    patient 
        WHERE   patient_id = %s
        """
        result = await self.execute_query(sql, (patient_id,))
        if result:
            return PatientDTO.from_dict(result[0])
        return None

    async def list(self, study_id: int) -> builtins.list[PatientDTO]:
        sql: LiteralString = """
        SELECT  *
        FROM    patient 
        WHERE   study_id = %s
        """
        result = await self.execute_query(sql, (study_id,))
        return [PatientDTO.from_dict(p) for p in result]

    async def save(self, patient: PatientDTO) -> dict:
        insert: LiteralString = """
        INSERT INTO patient (
            study_id, number, name, start_date, exit_date, status, comments,
            created_at, created_by, updated_at, updated_by)
        VALUES (%(study_id)s, %(number)s, %(name)s, %(start_date)s, %(exit_date)s, %(status)s, %(comments)s, 
                %(created_at)s, %(created_by)s, %(updated_at)s, %(updated_by)s)
        RETURNING patient_id
        """
        update: LiteralString = """
        UPDATE patient
        SET study_id = %(study_id)s, number = %(number)s, name = %(name)s, start_date = %(start_date)s, 
            exit_date = %(exit_date)s, status = %(status)s, comments = %(comments)s, 
            created_at = %(created_at)s, created_by = %(created_by)s, updated_at = %(updated_at)s, 
            updated_by = %(updated_by)s
        WHERE patient_id = %(patient_id)s
        RETURNING patient_id
        """
        return await self.insert_or_update(insert, update, patient.to_dict())

    async def delete(self, *, patient_id: int = 0, study_id: int = 0) -> None:
        if study_id:
            sql = "DELETE FROM patient WHERE study_id = %s"
            await self.execute_query(sql, (study_id,))
        else:
            sql = "DELETE FROM patient WHERE patient_id = %s"
            await self.execute_query(sql, (patient_id,))
