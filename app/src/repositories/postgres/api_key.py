import builtins
from typing import LiteralString

from src.dtos.api_key import ApiKeyDTO
from src.repositories.postgres.base import PostgresRepository


class ApiKeyRepository(PostgresRepository):
    def __init__(self):
        super().__init__()

    async def load(self, api_key_id: int) -> ApiKeyDTO | None:
        sql: LiteralString = """
        SELECT  api_key_id
        ,       user_name
        ,       api_key
        ,       key_name
        ,       key_description
        ,       valid_until
        ,       created_at
        ,       created_by
        ,       updated_at
        ,       updated_by
        FROM    api_key
        WHERE   api_key_id = %s
        """
        result = await self.execute_query(sql, (api_key_id,))
        if result:
            return ApiKeyDTO.from_dict(result[0])
        return None

    async def load_key(self, api_key: str) -> ApiKeyDTO | None:
        sql: LiteralString = """
        SELECT  api_key_id
        ,       user_name
        ,       api_key
        ,       key_name
        ,       key_description
        ,       valid_until
        ,       created_at
        ,       created_by
        ,       updated_at
        ,       updated_by
        FROM    api_key
        WHERE   api_key = %s
        """
        result = await self.execute_query(sql, (api_key,))
        if result:
            return ApiKeyDTO.from_dict(result[0])
        return None

    async def list(self, user_name: str) -> builtins.list[ApiKeyDTO]:
        # We are reading from a view, not a table
        sql: LiteralString = """
        SELECT  api_key_id
        ,       user_name
        ,       api_key
        ,       key_name
        ,       key_description
        ,       valid_until
        ,       created_at
        ,       created_by
        ,       updated_at
        ,       updated_by
        FROM    api_key
        WHERE   user_name = %s
        """
        result = await self.execute_query(sql, (user_name,))
        return [ApiKeyDTO.from_dict(s) for s in result]


    async def save(self, api_key: ApiKeyDTO) -> dict:
        insert: LiteralString = """
        INSERT INTO api_key (
            user_name, 
            api_key,
            key_name, 
            key_description, 
            valid_until, 
            created_at, 
            created_by, 
            updated_at, 
            updated_by
        ) VALUES (
            %(user_name)s, 
            %(api_key)s, 
            %(key_name)s, 
            %(key_description)s, 
            %(valid_until)s, 
            %(created_at)s, 
            %(created_by)s, 
            %(updated_at)s, 
            %(updated_by)s
        )
        RETURNING api_key_id
        """
        update: LiteralString = """
        UPDATE  api_key 
        SET     user_name = %(user_name)s
        ,       api_key = %(api_key)s
        ,       key_name = %(key_name)s
        ,       key_description = %(key_description)s
        ,       valid_until = %(valid_until)s
        ,       created_at = %(created_at)s
        ,       created_by = %(created_by)s
        ,       updated_at = %(updated_at)s
        ,       updated_by = %(updated_by)s
        WHERE   api_key_id = %(api_key_id)s
        """
        return await self.insert_or_update(insert, update, api_key.to_dict())


    async def delete(self, api_key_id: int) -> None:
        sql: LiteralString = """
        DELETE FROM api_key where api_key_id=%s
        """
        await self.execute_query(sql, (api_key_id,))
