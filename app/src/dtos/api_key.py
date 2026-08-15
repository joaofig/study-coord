from datetime import datetime
from typing import Any, Self

from src.dtos.base import BaseDTO


class ApiKeyDTO(BaseDTO):
    api_key_id: int
    user_name: str
    api_key: str
    key_name: str
    key_description: str
    valid_until: datetime

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            api_key_id=data["api_key_id"],
            user_name=data["user_name"],
            api_key=data["api_key"],
            key_name=data["key_name"],
            key_description=data["key_description"],
            valid_until=data["valid_until"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "api_key_id": self.api_key_id,
            "user_name": self.user_name,
            "api_key": self.api_key,
            "key_name": self.key_name,
            "key_description": self.key_description,
            "valid_until": self.valid_until,
        } | super().to_dict()
