from datetime import datetime

from pydantic import BaseModel


class BaseDTO(BaseModel):
    created_at: datetime = datetime.now()
    created_by: str = ""
    updated_at: datetime = datetime.now()
    updated_by: str = ""

    def to_dict(self) -> dict:
        return {
            "created_at": self.created_at.isoformat(),
            "created_by": self.created_by,
            "updated_at": self.updated_at.isoformat(),
            "updated_by": self.updated_by,
        }