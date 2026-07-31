import hashlib
from datetime import date
from typing_extensions import Self

from pydantic import BaseModel

from src.tools.user import dict_to_datetime


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


class UserDTO(BaseModel):
    user_id: int
    user_name: str
    pass_hash: str
    user_role: str
    change_pass: bool = False
    created_at: date = date.today()
    created_by: str
    updated_at: date = date.today()
    updated_by: str

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(
            user_id=data.get("user_id", 0),
            user_name=data.get("user_name", ""),
            pass_hash=data.get("pass_hash", ""),
            user_role=data.get("user_role", ""),
            change_pass=data.get("change_pass", False),
            created_at=dict_to_datetime(data, "created_at"),
            created_by=data.get("created_by", ""),
            updated_at=dict_to_datetime(data, "updated_at"),
            updated_by=data.get("updated_by", ""),
        )

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "pass_hash": self.pass_hash,
            "user_role": self.user_role,
            "created_at": self.created_at.isoformat(),
            "created_by": self.created_by,
            "updated_at": self.updated_at.isoformat(),
            "updated_by": self.updated_by,
            "change_pass": self.change_pass,
        }
