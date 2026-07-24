from typing import List

from src.dtos.user import UserDTO
from src.repositories.supabase.base import SupabaseRepository


TABLE = "user"


class UserRepository(SupabaseRepository):
    def __init__(self):
        super().__init__()

    async def get_user(self, user_name: str, pass_hash: str) -> UserDTO | None:
        await self.connect()
        if self.supabase:
            result = (
                await self.supabase.table(TABLE)
                .select("*")
                .eq("user_name", user_name)
                .eq("pass_hash", pass_hash)
                .execute()
            ).data
            if result:
                return UserDTO.from_dict(result[0])
        return None

    async def list(self) -> List[UserDTO]:
        await self.connect()
        if self.supabase:
            result = (await self.supabase.table(TABLE).select("*").execute()).data
            return [UserDTO.from_dict(s) for s in result]
        return []

    async def load(self, user_id: int) -> UserDTO | None:
        await self.connect()
        if self.supabase:
            result = (
                await self.supabase.table(TABLE)
                .select("*")
                .eq("user_id", user_id)
                .execute()
            ).data
            if result:
                return UserDTO.from_dict(result[0])
        return None

    async def save(self, user: UserDTO) -> dict:
        return await self.insert_or_update(TABLE, user.to_dict())

    async def delete(self, user_id: int) -> None:
        await self.connect()
        if self.supabase:
            await self.supabase.table(TABLE).delete().eq("user_id", user_id).execute()
        return None
