import builtins

from src.dtos.visit import VisitDTO
from src.repositories.postgres.base import PostgresRepository
from src.repositories.postgres.patient import PatientRepository


class VisitRepository(PostgresRepository):
    def __init__(self):
        super().__init__()

    async def load(self, visit_id: int) -> VisitDTO | None:
        sql = "SELECT * FROM visit WHERE visit_id = %s"
        result = await self.execute_query(sql, (visit_id,))
        if result:
            visit = VisitDTO.from_dict(result[0])
            repo = PatientRepository()
            visit.patient = await repo.load(visit.patient_id)
            return visit
        return None

    async def list(self, study_id: int, patient_id: int = 0) -> builtins.list[VisitDTO]:
        if patient_id == 0:
            sql = """
            SELECT  visit_id
            ,       study_id
            ,       patient_id
            ,       visit_date
            ,       visit_type
            ,       comments
            ,       created_at
            ,       created_by
            ,       updated_at
            ,       updated_by
            FROM    visit 
            WHERE   study_id = %s
            """
            result = await self.execute_query(sql, (study_id,))
        else:
            sql = """
            SELECT  visit_id
            ,       study_id
            ,       patient_id
            ,       visit_date
            ,       visit_type
            ,       comments
            ,       created_at
            ,       created_by
            ,       updated_at
            ,       updated_by
            FROM    visit 
            WHERE   study_id = %s AND patient_id = %s
            """
            result = await self.execute_query(sql, (study_id, patient_id))
        return [VisitDTO.from_dict(v) for v in result]

    async def save(self, visit: VisitDTO) -> dict:
        insert = """
        INSERT INTO visit (study_id, patient_id, visit_date, visit_type, comments, 
                           created_at, created_by, updated_at, updated_by) 
        VALUES (%(study_id)s, %(patient_id)s, %(visit_date)s, %(visit_type)s, %(comments)s, 
                %(created_at)s, %(created_by)s, %(updated_at)s, %(updated_by)s)
        """
        update = """
        UPDATE visit
        SET study_id = %(study_id)s,
            patient_id = %(patient_id)s,
            visit_date = %(visit_date)s,
            visit_type = %(visit_type)s,
            comments = %(comments)s,
            created_at = %(created_at)s,
            created_by = %(created_by)s,
            updated_at = %(updated_at)s,
            updated_by = %(updated_by)s
        WHERE visit_id = %(visit_id)s
        """
        return await self.insert_or_update(insert, update, visit.to_dict())

    async def delete(self, visit_id: int):
        sql = "DELETE FROM visit WHERE visit_id = %s"
        await self.execute_query(sql, (visit_id,))

    async def delete_by_study_id_and_patient_id(self, study_id: int, patient_id: int):
        sql = "DELETE FROM visit WHERE study_id = %s AND patient_id = %s"
        await self.execute_query(sql, (study_id, patient_id))
