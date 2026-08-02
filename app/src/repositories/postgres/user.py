import builtins

from src.dtos.user import UserDTO
from src.repositories.postgres.base import PostgresRepository

TABLE = "user"


class UserRepository(PostgresRepository):
    def __init__(self):
        super().__init__()

    async def get_user(self, user_name: str, pass_hash: str) -> UserDTO | None:
        sql = f'SELECT * FROM "{TABLE}" WHERE user_name = %s AND pass_hash = %s'
        result = await self.execute_query(sql, (user_name, pass_hash))
        if result:
            return UserDTO.from_dict(result[0])
        return None

    async def list(self) -> builtins.list[UserDTO]:
        sql = f'SELECT * FROM "{TABLE}"'
        result = await self.execute_query(sql)
        return [UserDTO.from_dict(s) for s in result]

    async def load(self, user_id: int) -> UserDTO | None:
        sql = f'SELECT * FROM "{TABLE}" WHERE user_id = %s'
        result = await self.execute_query(sql, (user_id,))
        if result:
            return UserDTO.from_dict(result[0])
        return None

    async def save(self, user: UserDTO) -> dict:
        return await self.insert_or_update(TABLE, user.to_dict())

    async def delete(self, user_id: int) -> None:
        sql = f'DELETE FROM "{TABLE}" WHERE user_id = %s'
        await self.execute_query(sql, (user_id,))
