import builtins

from src.dtos.patient import PatientDTO
from src.repositories.postgres.base import PostgresRepository

TABLE = "patient"


class PatientRepository(PostgresRepository):
    def __init__(self):
        super().__init__()

    async def patient_number_exists(self, study_id: int, patient_number: str) -> bool:
        sql = f'SELECT * FROM "{TABLE}" WHERE study_id = %s AND "number" = %s'
        result = await self.execute_query(sql, (study_id, patient_number))
        return len(result) > 0

    async def load(self, patient_id: int) -> PatientDTO | None:
        sql = f'SELECT * FROM "{TABLE}" WHERE patient_id = %s'
        result = await self.execute_query(sql, (patient_id,))
        if result:
            return PatientDTO.from_dict(result[0])
        return None

    async def list(self, study_id: int) -> builtins.list[PatientDTO]:
        sql = f'SELECT * FROM "{TABLE}" WHERE study_id = %s'
        result = await self.execute_query(sql, (study_id,))
        return [PatientDTO.from_dict(p) for p in result]

    async def save(self, patient: PatientDTO) -> dict:
        return await self.insert_or_update(TABLE, patient.to_dict())

    async def delete(self, *, patient_id: int = 0, study_id: int = 0) -> None:
        if study_id:
            sql = f'DELETE FROM "{TABLE}" WHERE study_id = %s'
            await self.execute_query(sql, (study_id,))
        else:
            sql = f'DELETE FROM "{TABLE}" WHERE patient_id = %s'
            await self.execute_query(sql, (patient_id,))
