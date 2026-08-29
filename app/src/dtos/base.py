from datetime import datetime

from pydantic import BaseModel
from nicemvvm.tools.user import get_user_name


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

    def log_change(self, own_id: int):
        self.updated_at = datetime.now()
        self.updated_by = get_user_name()

        if own_id == 0:
            self.created_at = self.updated_at
            self.created_by = self.updated_by
