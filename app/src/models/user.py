from typing import List

from src.dtos.user import UserDTO
from src.repositories.supabase.user import UserRepository


class UserModel:
    repo = UserRepository()

    @classmethod
    def empty(cls) -> UserDTO:
        return UserDTO(
            user_id=0,
            user_name="",
            pass_hash="",
            user_role="User",
            created_by="",
            updated_by=""
        )

    async def save(self, dto: UserDTO):
        user = await self.repo.save(dto)
        dto.user_id = user["user_id"]

    async def delete(self, user_id: int):
        await self.repo.delete(user_id)

    async def load(self, user_id: int) -> UserDTO | None:
        return await self.repo.load(user_id)

    async def list(self) -> List[UserDTO]:
        return await self.repo.list()

    async def get_user(self, user_name: str, pass_hash: str) -> UserDTO | None:
        return await self.repo.get_user(user_name, pass_hash)
