import builtins

from src.dtos.api_key import ApiKeyDTO
from src.repositories.postgres.api_key import ApiKeyRepository


class ApiKeyModel:
    repo = ApiKeyRepository()

    async def save(self, dto: ApiKeyDTO) -> ApiKeyDTO:
        study: dict = await self.repo.save(dto)
        return ApiKeyDTO.from_dict(study)

    async def load(self, api_key_id: int) -> ApiKeyDTO | None:
        return await self.repo.load(api_key_id)

    async def delete(self, api_key_id: int):
        await self.repo.delete(api_key_id)

    async def list(self, user_name: str) -> builtins.list[ApiKeyDTO]:
        return await self.repo.list(user_name)
